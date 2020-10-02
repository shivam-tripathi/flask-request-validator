import validators


def create_custom_validator(validator_method, err_msg=None):
    def custom_validator(*args, **kwargs):
        res = validator_method(*args, **kwargs)
        if type(res) == tuple and type(res[0]) is bool and (type(res[1]) is str or res[1] is None):
            success, custom_err_msg = res
        elif type(res) is bool:
            success, custom_err_msg = res, err_msg
        elif type(res) is validators.ValidationFailure:
            success, custom_err_msg = False, err_msg
        else:
            raise Exception(
                f'Invalid return from validation method: should either be (bool, str) or bool but found {res}')
        return success, custom_err_msg if not success else None

    return custom_validator


class FlaskRequestValidator:
    __instance__ = None

    def __init__(self):
        self.custom_validators = None

        def validate_type(obj, _type):
            if type(obj) is not _type:
                return False, f'Type is not a {_type.__name__} but {type(obj).__name__} for'
            return True, None

        self.add_validator('type', validate_type)

        def validate_list(arr, _type, empty_allowed=True, *args, **kwargs):
            if type(arr) is not list:
                return False, f'Type is not list but {type(arr).__name__} for'
            if not empty_allowed and len(arr) == 0:
                return False, f'Empty list not allowed for'
            for item in arr:
                if type(item) is not _type:
                    return False, f'Items in list should be of type {_type.__name__} but one item is of type {type(item).__name__}'
            return True, None

        self.add_validator('list', validate_list)

    def add_validator(self, name, validator_method, err_msg=None):
        if self.custom_validators.get(name) is not None:
            raise Exception(f'Custom validator with {name} already exists')
        self.custom_validators[name] = create_custom_validator(validator_method, err_msg)

    def get_validator(self, validation_type):
        if self.custom_validators.get(validation_type) is not None:
            return self.custom_validators[validation_type]

        if validators.__dict__.get(validation_type) is not None:
            return create_custom_validator(validators.__dict__[validation_type],
                                           f"Validation failed: {validation_type} for")

        raise Exception(f'Invalid validator {validation_type}')

    @classmethod
    def get_instance(cls):
        if cls.__instance__ is None:
            cls.__instance__ = FlaskRequestValidator()
        return cls.__instance__
