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
JSON_CARD_SCHEMA = {
    'name': {
        'required': True,
        'type': 'string'
    },
    'tier': {
        'required': True,
        'type': 'integer',
        'min': 0,
    },
    'victory_points': {
        'required': True,
        'type': 'integer',
        'min': 0,
    },
    'discounted_coin_type_name': {
        'required': True,
        'type': 'string'
    },
    'cost': {
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
JSON_CARD_MANAGER_SCHEMA = {
    'cards': {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'dict',
        }
    }
}
JSON_DECK_SCHEMA = {
    'cards': {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'string',
        }
    },
    'tier': {
        'required': True,
        'type': 'integer'
    }
}
JSON_CARD_RESERVE_SCHEMA = {
    "card_manager": {
        'required': True,
        'type': 'dict',
    },
    "number_of_cards_on_sale": {
        'required': True,
        'type': 'integer'
    },
    "decks": {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'dict',
        }
    },
    "tiers": {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'integer',
        }
    },
    "cards_on_sale": {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'string',
        }
    }
}
JSON_SPONSOR_SCHEMA = {
    'name': {
        'required': True,
        'type': 'string'
    },
    'victory_points': {
        'required': True,
        'type': 'integer'
    },
    'cost': {
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
JSON_SPONSOR_MANAGER_SCHEMA = {
    'sponsors': {
        'required': True,
        'type': 'list',
        'minlength': 1,
        'schema': {
            'required': True,
            'type': 'dict'
        }
    },
}
JSON_SPONSOR_RESERVE_SCHEMA = {
    "sponsor_manager": {
        'required': True,
        'type': 'dict',
    },
    "sponsors": {
        'required': True,
        'type': 'list',
        'schema': {
            'required': True,
            'type': 'string',
        }
    }
}
JSON_PLAYER_COIN_INVENTORY = {
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
JSON_PLAYER_CARD_INVENTORY = {
    'max_reserved_cards': {
        'required': True,
        'type': 'integer'
    },
    'reserved_cards': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    },
    'cards': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    }
}
JSON_PLAYER_SPONSOR_INVENTORY = {
    'sponsors': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    }
}
JSON_PLAYER = {
    'name': {
        'required': True,
        'type': 'string'
    },
    'coin_inventory': {
        'required': True,
        'type': 'dict'
    },
    'card_inventory': {
        'required': True,
        'type': 'dict'
    },
    'sponsor_inventory': {
        'required': True,
        'type': 'dict'
    }
}
