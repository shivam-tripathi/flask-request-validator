from flask_request_validator import FlaskRequestValidator, RequestSchema


def apply_args(validator_method, obj, args_param, kwargs_param):
    if len(args_param) != 0 and len(kwargs_param) != 0:
        success, err_msg = validator_method(obj, *args_param, **kwargs_param)
    elif len(args_param) != 0 and len(kwargs_param) == 0:
        success, err_msg = validator_method(obj, *args_param)
    elif len(args_param) == 0 and len(kwargs_param) != 0:
        success, err_msg = validator_method(obj, **kwargs_param)
    else:
        success, err_msg = validator_method(obj)
    return success, f"Validation failed: {err_msg}" if not success else None


def validate_obj(obj, schema):
    request_validator = FlaskRequestValidator.get_instance()
    # Schema is nested
    if type(schema) is dict:
        if type(obj) is not dict:
            return False, f'Should be json but found {type(obj).__name__} for'
        for (inner_key, inner_key_schema) in schema.items():
            success, err_msg = validate_obj(obj.get(inner_key), inner_key_schema)
            return success, f"{err_msg} key {inner_key} in" if not success else None
    # This is the leaf of the schema
    elif type(schema) is RequestSchema:
        # First handle validation for `present`
        if schema.get('present') and obj is None:
            return False, 'Validation failed: Missing'
        for validation_type, validation_args in schema.items():
            if validation_type == 'present':
                continue
            validator_method = request_validator.get_validator(validation_type)
            args_param = validation_args if type(validation_args) is list else []
            kwargs_param = validation_args if type(validation_args) is dict else {}
            if type(validation_args) is tuple:
                for validation_arg in validation_args:
                    if type(validation_arg) is dict:
                        kwargs_param.update(validation_arg)
                    else:
                        args_param.append(validation_arg)
            return apply_args(validator_method, obj, args_param, kwargs_param)
    else:
        raise Exception(f"Invalid schema {schema}")