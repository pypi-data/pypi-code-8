from werkzeug.exceptions import (
    NotFound,
    Forbidden,
    BadRequest,
    Unauthorized
)

from mythicals import form, Form, tracer


class Error(Form):

    registry = {
    }

    @classmethod
    def cast(cls, ex):
        if type(ex) not in cls.registry:
            raise LookupError('No error registered for {}'.format(type(ex)))
        return cls.registry[type(ex)](ex)

    _type_ = form.String()

    status_code = form.Integer()

    description = form.String()

    trace_id = form.String(default=lambda: tracer.id)
