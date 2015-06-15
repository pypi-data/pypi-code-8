import os
import tempfile

import sqlalchemy as sa
import sqlalchemy.orm as saorm

from mythicals import form, Form, mime, db, tracer

from . import Persisted, InstrumentType, Company


settlements = sa.Table(
    'settlements',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('_type', InstrumentType, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('trace_id', sa.Unicode, index=True, default=lambda: tracer.id, nullable=False),
)


class PublishTallyV1(Form):

    type = form.String('type')

    count = form.Integer('count')

    amount = form.Integer('amount', optional=True)

    currency = form.String('currency', optional=True)


class PublishOpV1(Form):

    type = form.String('_type')

    id = form.UUID('id')

    external_id = form.String('external_id')

    state = form.String('state')

    code = form.String('code')

    diagnostics = form.List(form.String())


class PublishV1(Form):

    version = form.String().constant('1')

    settlement_id = form.UUID('id')

    tally = form.List(form.SubForm(PublishTallyV1), 'tally()')

    ops = form.List(form.SubForm(PublishOpV1), 'ops.all()')


class Settlement(Persisted):

    __table__ = settlements

    __mapper_args__ = {
        'polymorphic_on': settlements.c._type,
    }

    types = db.Enum(InstrumentType)

    company = saorm.relationship('Company')

    mimes = mime.Selection([mime.json])

    @classmethod
    def create(cls, query, id=None, trace_id=None):
        query_count = query.count()

        filtered_query = (
            query
            .filter(cls.op_type.settlement_id == None)
            .filter(~cls.op_type.state.in_([
                cls.op_type.states.STAGED, cls.op_type.states.EXECUTING,
            ]))
        )
        filtered_query_count = filtered_query.count()
        if filtered_query_count != query_count:
            raise ValueError('Could only settle {} != {}'.format(
                filtered_query_count, query_count
            ))
        if filtered_query_count == 0:
            raise Exception('Nothing to settle')

        company_ids = (
            filtered_query
            .with_entities(sa.distinct(cls.op_type.company_id))
        ).all()
        if len(company_ids) != 1:
            raise ValueError('Settlement ops must be for the same company')
        company = Company.query.filter(Company.id == company_ids[0][0]).one()

        settlement = cls(
            id=id or cls.generate_id(),
            company=company,
            trace_id=trace_id,
        )
        db.Session.add(settlement)

        filtered_subquery = filtered_query.subquery()
        count = (
            cls.op_type
            .query
            .filter(cls.op_type.id == filtered_subquery.c.id)
            .update(
                values={
                    'settlement_id': settlement.id,
                },
            )
        )
        if count != filtered_query_count:
            raise ValueError('Could only settle {} != {}'.format(
                count, filtered_query_count
            ))

        return settlement

    def tally(self):
        tallies = []
        for type_ in self.op_type.types:
            op_type = saorm.class_mapper(self.op_type).polymorphic_map[type_].class_
            tallies.extend(op_type.tally(self.ops))
        return tallies

    @property
    def publish_path(self):
        raise NotImplementedError()

    def publish(self, mime_type):
        mime = self.mimes.match(mime_type)
        if mime is None:
            raise ValueError('Unsupported mime type "{}"'.format(mime_type))
        publish_path = ''.join([self.publish_path, '.', mime.extension])
        fd, temp_path = tempfile.mkstemp('mythical')
        os.close(fd)
        try:
            with open(publish_path, 'w') as fo:
                mime.encoder(PublishV1(self), fo)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
