from flask import request
from functools import wraps

from flask_request_validator.flask_request_validator import FlaskRequestValidator, create_custom_validator
from flask_request_validator.helpers import validate_obj
from flask_request_validator.request_schema import RequestSchema


def add_validator(name, validator_method, err_msg=None):
    request_validator = FlaskRequestValidator.get_instance()
    if request_validator.custom_validators.get(name) is not None:
        raise Exception(f'Custom validator with {name} already exists')
    request_validator.custom_validators[name] = create_custom_validator(validator_method, err_msg)


def validate_request(validation_schema, opts=None):
    if opts is None:
        opts = {"throws": True}

    def decorator(f):
        @wraps(f)
        def decorated_function():
            for (request_key, schema) in validation_schema.items():
                request_obj = None
                if request_key == 'json':
                    request_obj = request.json
                if request_key == 'args':
                    request_obj = request.args
                if request_key == 'form':
                    request_obj = request.form
                if request_key == 'view_args':
                    request_obj = request.view_args
                success, err_msg = validate_obj(request_obj, schema)
                if not success:
                    if opts.get("throws") is True:
                        raise Exception(f"{err_msg} request {request_key}")
                    return err_msg
            return f()
        return decorated_function
    return decorator
