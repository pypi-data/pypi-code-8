# Copyright 2015 Diogo Dutra

# This file is part of alquimia.

# alquimia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm import ColumnProperty
from alquimia.model import AlquimiaModel
from alquimia.modelmeta import AlquimiaModelMeta
from alquimia.models_attrs import ModelsAttributes
from alquimia.models_attrs_reflect import ModelsAtrrsReflect
from alquimia import DATA_TYPES


class JoinNotFoundError(Exception):
    def __init__(self, join_name, field):
        message = 'Join %s not found in gived joins for field %s.%s' % \
                                                  (join_name, join_name, field)
        Exception.__init__(self, message)


class AlquimiaModels(dict):
    def __init__(self, db_url, dict_=None, data_types=DATA_TYPES,
                                                 create=False, logger=logging):
        engine = create_engine(db_url)
        base_model = declarative_base(engine, metaclass=AlquimiaModelMeta,
                         cls=AlquimiaModel, constructor=AlquimiaModel.__init__)
        self._session_class = sessionmaker(engine)
        self._session = self._session_class()
        self.metadata = base_model.metadata
        if dict_ is not None:
            attrs = ModelsAttributes(dict_, self.metadata, data_types, logger)
        else:
            attrs = ModelsAtrrsReflect(self.metadata, logger)
        self._build(base_model, attrs)
        if create:
            self.metadata.create_all()

    def _build(self, base_model, models_attrs):
        models = {}
        for model_name, attrs in models_attrs.iteritems():
            attrs.update({'_session': self._session})
            model = type(model_name, (base_model,), attrs)
            models[model_name] = model

        for model in models.values():
            model.__mapper__.relationships
            for attr_name, attr in model.iteritems():
                if isinstance(attr.prop, RelationshipProperty):
                    setattr(attr, 'model', models[attr_name])
                else:
                    model.columns.append(attr_name)

        self.update(models)

    def clean(self):
        self._session.expunge_all()

    def _build_query_func(self, func):
        pass

    def _build_query_fields(self, dict_, joins_names):
        fields = []
        for join_name in joins_names:
            try:
                fields = dict_[join_name]
            except KeyError:
                raise JoinNotFoundError(join_name, field)
            for field in fields:
                fields.append('%s.%s' % (join_name, field))
        fields = fields + [self._build_query_func(dict_.pop(attr)) \
                                         for attr in dict_ if attr not in self]
        for k, v in dict_.iteritems():
            fields.append(self[k][v])
        return fields

    def query(self, dict_):
        filters = utils.parse_filters(dict_.pop('filters', {}))
        group = dict_.pop('group', [])
        group = [group] if not isinstance(group, list) else group
        order = dict_.pop('order', ())
        order = (order, 'asc') if not isinstance(order, tuple) else order
        subqueries = dict_.pop('subqueries', {})
        subqueries = {k: self.query(v).subquery(k) \
                                            for k, v in subqueries.iteritems()}
        fields = self._build_query_fields(dict_, subqueries.keys())
        query = self._session.query()
        return query
