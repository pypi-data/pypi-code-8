#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from logging import config as logging_config

from alembic import context
from neutron.db import model_base
from oslo.config import cfg
from oslo.db.sqlalchemy import session
import sqlalchemy as sa
from sqlalchemy import event

from gbpservice.neutron.db.migration.models import head  # noqa

# Mirror of the Neutron's env, plus some tweaks in order to set cross DB
# FKs.

MYSQL_ENGINE = None
GBP_VERSION_TABLE = 'gbp_alembic_version'
config = context.config
neutron_config = config.neutron_config
logging_config.fileConfig(config.config_file_name)
target_metadata = model_base.BASEV2.metadata


def set_mysql_engine():
    try:
        mysql_engine = neutron_config.command.mysql_engine
    except cfg.NoSuchOptError:
        mysql_engine = None

    global MYSQL_ENGINE
    MYSQL_ENGINE = (mysql_engine or
                    model_base.BASEV2.__table_args__['mysql_engine'])


def run_migrations_offline():
    set_mysql_engine()

    kwargs = dict()
    if neutron_config.database.connection:
        kwargs['url'] = neutron_config.database.connection
    else:
        kwargs['dialect_name'] = neutron_config.database.engine
    kwargs['version_table'] = GBP_VERSION_TABLE
    context.configure(**kwargs)

    with context.begin_transaction():
        context.run_migrations()


@event.listens_for(sa.Table, 'after_parent_attach')
def set_storage_engine(target, parent):
    if MYSQL_ENGINE:
        target.kwargs['mysql_engine'] = MYSQL_ENGINE


def run_migrations_online():
    set_mysql_engine()
    engine = session.create_engine(neutron_config.database.connection)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table=GBP_VERSION_TABLE
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()
        engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
