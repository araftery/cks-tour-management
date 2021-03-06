def validator_constructor(coercer, type_name):
    def validator(data):
        try:
            data = coercer(data.strip())
            return {'valid': True, 'value': data, 'errors': []}
        except:
            return {'valid': False, 'value': data, 'errors': ['You must enter a valid {}.'.format(type_name)]}

    return validator


def bool_validator(data):
    try:
        data = data.lower().strip()
        if data in ['true', 'false']:
            if data == 'true':
                data = True
            elif data == 'false':
                data = False

            return {'valid': True, 'value': data, 'errors': []}
        else:
            # it's not true or false or the cleaning operation failed
            raise
    except:
        return {'valid': False, 'value': data, 'errors': ['You must enter either true or false.']}


def semester_or_never_validator(data):
    try:
        data = data.lower().strip()

        if data in ['spring', 'fall', 'both', 'never']:
            return {'valid': True, 'value': data, 'errors': []}
        else:
            # it's not spring, fall, both, or None, or the cleaning operation failed
            raise
    except:
        return {'valid': False, 'value': data, 'errors': ['You must enter either fall, spring, both, or never.']}


def email_validator(data):
    data = data.strip()
    try:
        first, second = data.split('@', 1)
        if '.' not in second:
            raise

        return {'valid': True, 'value': data, 'errors': []}
    except:
        return {'valid': False, 'value': data, 'errors': ['You must enter a valid email address.']}


setting_validators = {
    'int': validator_constructor(int, 'integer'),
    'float': validator_constructor(float, 'floating point number'),
    'string': validator_constructor(unicode, 'string'),
    'bool': bool_validator,
    'semester_or_never': semester_or_never_validator,
    'email': email_validator,
}
