"""Schemas for structured data."""
from flatland.exc import AdaptationError
from flatland.schema import (
    Array,
    Boolean,
    Compound,
    Constrained,
    Container,
    Date,
    DateTime,
    DateYYYYMMDD,
    Decimal,
    Dict,
    Element,
    Enum,
    Float,
    Form,
    Integer,
    JoinedString,
    List,
    Long,
    Mapping,
    MultiValue,
    Number,
    Properties,
    Ref,
    Scalar,
    Schema,
    Sequence,
    Skip,
    SkipAll,
    SkipAllFalse,
    SparseDict,
    SparseSchema,
    String,
    Time,
    Unevaluated,
    Unset,
    )
from flatland.signals import element_set, validator_validated
from flatland.util import Unspecified, class_cloner


__all__ = [
    'AdaptationError',
    'Array',
    'Boolean',
    'Compound',
    'Constrained',
    'Container',
    'Date',
    'DateTime',
    'DateYYYYMMDD',
    'Decimal',
    'Dict',
    'Element',
    'Enum',
    'Float',
    'Form',
    'Integer',
    'JoinedString',
    'List',
    'Long',
    'Mapping',
    'MultiValue',
    'Number',
    'Properties',
    'Ref',
    'Scalar',
    'Schema',
    'Sequence',
    'Skip',
    'SkipAll',
    'SkipAllFalse',
    'SparseDict',
    'SparseSchema',
    'String',
    'Time',
    'Unevaluated',
    'Unset',
    'Unspecified',
    'class_cloner',
    'element_set',
    'validator_validated',
    ]

__version__ = '0.8'
