from __future__ import unicode_literals

import os

import sqlalchemy as sa
import sqlalchemy.orm as saorm
import sqlalchemy.ext.hybrid as sahybrid

from mythicals import form, Form, mime, db, tracer

from . import Persisted, InstrumentType, Confirmation


submissions = sa.Table(
    'submissions',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('_type', InstrumentType, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('location', sa.Unicode, nullable=False),
    sa.Column('mime_type', sa.Text, nullable=False),
    sa.Column('external_id', sa.Unicode, nullable=False),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False),
    sa.Column('confirmation_id', db.UUID, sa.ForeignKey('confirmations.id'), index=True),
    sa.UniqueConstraint('company_id', 'external_id', name='submissions_company_id_external_id_ck')
)


class PublishTallyV1(Form):

    type = form.String('type')

    count = form.Integer('count')

    amount = form.Integer('amount', optional=True)

    currency = form.String('currency', optional=True)


class PublishV1(Form):

    version = form.String().constant('1')

    confirmation_id = form.UUID('confirmation.id')

    submission_id = form.UUID('id')

    external_id = form.String('external_id')

    code = form.String('confirmation.code')

    diagnostics = form.List(form.String(), 'confirmation.diagnostics')

    tally = form.List(form.SubForm(PublishTallyV1), 'tally()')



class Submission(Persisted):

    __table__ = submissions

    __mapper_args__ = {
        'polymorphic_on': submissions.c._type,
    }

    types = db.Enum(InstrumentType)

    company = saorm.relationship('Company')

    confirmation = saorm.relationship(
        'Confirmation', backref=saorm.backref('submission', uselist=False)
    )

    @sahybrid.hybrid_property
    def processed(self):
        return self.confirmation_id != None

    Form = None

    mimes = mime.Selection([mime.json])

    @classmethod
    def create(cls,
               company,
               location,
               external_id,
               mime_type=None,
               id=None,
               trace_id=None,
        ):
        if cls.Form is None:
            raise TypeError('{0}.Form has not been set'.format(cls.__name__))
        if mime_type is None:
            ext = os.path.splitext(location)[1]
            mime = cls.mimes.match_extension(ext)
            if mime is None:
                raise ValueError('Unsupported mime ext "{0}"'.format(ext))
            mime_type = mime.type
        else:
            mime = cls.mimes.match(mime_type)
            if mime is None:
                raise ValueError('Unsupported mime type "{0}"'.format(mime_type))
        submission = cls(
            id=id or cls.generate_id(),
            company=company,
            location=location,
            mime_type=mime_type,
            external_id=external_id,
            trace_id=trace_id,
        )
        db.Session.add(submission)
        return submission

    def reset(self):
        self.confirmation = None

    def open(self):
        return self.company.fs.open(self.location, 'rb')

    @property
    def archive_location(self):
        raise NotImplementedError()

    @property
    def is_archived(self):
        return self.location.endswith(self.archive_location)

    def archive(self):
        if self.is_archived:
            return self.location
        with self.company.fs.open(self.location, 'rb') as sfo, \
             self.company.fs.open(self.archive_location, 'wb+') as dfo:
            dfo.write(sfo.read())
        if os.path.exists(self.location):
            os.remove(self.location)
        self.location = self.archive_location
        return self.location

    def process(self, id_codecs):
        self.archive()

        confirmation = Confirmation.create(
            id=Confirmation.generate_id(),
            company=self.company,
            code=Confirmation.codes.STAGED,
        )

        count = (
            type(self)
            .query
            .filter_by(
                id=self.id,
                confirmation_id=None
            )
            .update(
                values=dict(
                    confirmation_id=confirmation.id
                ),
                synchronize_session='fetch'
            )
        )
        if count != 1:
            raise ValueError(
                '{} has already been processed, reset it if you need to re-process'.format(self)
            )

        with form.ctx(
                 company=self.company,
                 confirmation=confirmation,
                 trace_id=self.trace_id,
                 id_codecs=id_codecs,
             ), self.open() as io:
            encoded = io.read()
            source = self.mimes.match(self.mime_type).source(encoded)
            parser = self.Form()
            db.Session.begin_nested()
            try:
                errors = parser.map(src=source)
                if errors:
                    confirmation.code = Confirmation.codes.MALFORMED
                    confirmation.diagnostics = [
                        unicode(error) for error in errors
                    ]
                else:
                    confirmation.code = Confirmation.codes.ACCEPTED
                db.Session.commit()
            except:
                db.Session.rollback()
                raise

        return confirmation
