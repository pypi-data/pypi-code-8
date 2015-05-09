# Copyright (C) 2014-2015, Availab.io(R) Ltd. All rights reserved.
import json
from flask import request
from functools import wraps
from webcommon.utils.consts import Consts
from json_response import json_failed
from jsonschema import validate, ValidationError


def validate_json_request(schema, only_json=True, additional_validator=None, form_key=None):
    """Used as wrapper for request handlers. It validates
    the request against provided schema. Optionally checks
    valid content type

    Args:
        schema - Json schema (v4) dictionary which is used for validation
            of incomming request
        only_json - if true, validation fails in case of mimetype is not
            'application/json'
        additional_validator - Function object which takes output of
            json.get_json() as first argument and raises ValidationError
            in case input structure is "wrong"
        form_key - key of the request.form where is json data


    """

    def wraped(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            is_json = str(request.mimetype).lower() == Consts.MIME_TYPE_APP_JSON

            if only_json and not is_json:
                return json_failed(status_code=Consts.HTTP_CODE_UNSUPPORTED_MEDIA_TYPE,
                                   message='Only application/json supported')
            should_validate = False
            data = None

            if is_json:
                should_validate = True
                data = request.get_json()

            if not only_json and form_key:
                should_validate = True
                data = json.loads(request.form[form_key])

            if should_validate:
                try:
                    validate(data, schema)
                    if additional_validator is not None:
                        additional_validator(data)
                except ValidationError as e:
                    return json_failed(message="Wrong input structure",
                                       status_code=400,
                                       data={
                                           "validated_against": schema,
                                           "error_message": e.message})

            return f(*args, **kwargs)

        return decorated_function

    return wraped