import hashlib
import os
import uuid

from fs.mountfs import MountFS
from fs.multifs import MultiFS
from fs.osfs import OSFS
from fs.s3fs import S3FS

import sqlalchemy as sa
import sqlalchemy.orm as saorm

from mythicals import db, config

from . import Persisted


companies = sa.Table(
    'companies',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('updated_at', sa.DateTime, nullable=False, onupdate=sa.func.clock_timestamp(), server_default=sa.text('now()')),
    sa.Column('name', sa.Unicode, nullable=False, unique=True, index=True),
)


passwords = sa.Table(
    'passwords',
    db.meta_data,
    sa.Column('id', db.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    sa.Column('company_id', db.UUID, sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True),
    sa.Column('hashed', sa.Unicode, nullable=False),
)


class Company(Persisted):

    __table__ = companies

    passwords = saorm.relationship(
        'Password', lazy='dynamic', backref='company', cascade='all, delete-orphan'
    )

    credit_card_ops = saorm.relationship(
        'CreditCardOp', lazy='dynamic', cascade='all, delete-orphan'
    )

    credit_card_submissions = saorm.relationship(
        'CreditCardSubmission', lazy='dynamic', cascade='all, delete-orphan'
    )

    bank_account_ops = saorm.relationship(
        'BankAccountOp', lazy='dynamic', cascade='all, delete-orphan'
    )

    bank_account_submissions = saorm.relationship(
        'BankAccountSubmission', lazy='dynamic', cascade='all, delete-orphan'
    )

    merchant_ops = saorm.relationship(
        'MerchantOp', lazy='dynamic', cascade='all, delete-orphan'
    )

    merchant_submissions = saorm.relationship(
        'MerchantSubmission', lazy='dynamic', cascade='all, delete-orphan'
    )

    @classmethod
    def create(cls, name):
        instance = cls(name=name)
        db.Session.add(instance)
        return instance

    def add_password(self, text):
        return Password.create(company=self, text=text)

    def generate_password(self):
        text = Password.generate()
        self.add_password(text)
        return text

    def authenticate(self, text):
        return db.Session.query(
            self.passwords
            .filter(Password.hashed == Password.calculate_hash(text))
            .exists()
        ).scalar()

    @property
    def downloads(self):
        if config.DOWNLOADS['use'] == 's3':
            prefix = os.path.join(
                config.DOWNLOADS['s3']['prefix'], self.id.hex
            )
            fs = S3FS(
               bucket=config.DOWNLOADS['s3']['bucket'],
               prefix=prefix,
               aws_access_key=config.DOWNLOADS['s3']['aws_access_key'],
               aws_secret_key=config.DOWNLOADS['s3']['aws_secret_key'],
            )
        elif config.DOWNLOADS['use'] == 'os':
            path = os.path.join(
               config.DOWNLOADS['os']['root'], self.id.hex, 'downloads'
            )
            fs = OSFS(path, create=True)
        else:
            raise ValueError(
                'Unsupported config.DOWNLOADS["use"] = "{0}"'
                .format(config.DOWNLOADS['use'])
            )
        for path in [
                'credit_card/submissions',
                'bank_account/submissions',
                'merchant/submissions',
            ]:
            if not fs.exists(path):
                fs.makedir(path, recursive=True)
        return fs

    @property
    def uploads(self):
        path = os.path.join(config.UPLOADS['root'], self.id.hex, 'uploads')
        fs = OSFS(path, create=True)
        for path in [
                'credit_card',
                'bank_account',
                'merchant',
            ]:
            if not fs.exists(path):
                fs.makedir(path, recursive=True)
        return fs

    @property
    def mount(self):
        fs = MountFS()
        fs.mount('uploads', self.uploads)
        fs.mount('downloads', self.downloads)
        return fs

    @property
    def fs(self):
        fs = MultiFS()
        fs.addfs('root', OSFS('/'), write=False)
        fs.addfs('company', self.mount, write=True)
        return fs


class Password(Persisted):

    __table__ = passwords

    @classmethod
    def generate(cls):
        return uuid.uuid4().hex

    @classmethod
    def calculate_hash(cls,
                       text,
                       version='1',
                       method=hashlib.sha1,
                       encoding='hex',
                       glue='$',
        ):
        hashed = method(text)
        parts = [
            version,
            hashed.name,
            encoding,
            hashed.digest().encode(encoding)
        ]
        result = glue + glue.join(parts)
        if not isinstance(result, unicode):
            result = result.decode('utf-8')
        return result

    @classmethod
    def create(cls, company=None, text=None):
        password = cls(
            company=company,
            hashed=cls.calculate_hash(text or cls.generate()),
        )
        db.Session.add(password)
        return password
