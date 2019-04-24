JSON_COIN_TYPE_SCHEMA = {
    'name': {
        'required': True,
        'type': 'string'
    },
    'total_number': {
        'required': True,
        'type': 'integer'
    }
}
JSON_COIN_TYPE_MANAGER_SCHEMA = {
    'coin_types': {
        'required': True,
        'type': 'list',
        'minlength': 1,
        'schema': {
            'required': True,
            'type': 'dict'
        }
    },
    'coin_equivalents': {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'dict',
            'schema': {
                'coin_name': {
                    'required': True,
                    'type': 'string'
                },
                'equivalent_coins_name': {
                    'required': True,
                    'type': 'string'
                }
            }
        }
    }
}
JSON_COIN_RESERVE_SCHEMA = {
    'coin_type_manager': {
        'required': True,
        'type': 'dict',
    },
    'coin_stocks': {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'dict',
            'schema': {
                'coin_name': {
                    'required': True,
                    'type': 'string'
                },
                'count': {
                    'required': True,
                    'type': 'integer',
                    'min': 0,
                }
            }
        }
    }
}
