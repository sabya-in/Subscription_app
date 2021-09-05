import secrets

class Config(object):
    SECRET_KEY = secrets.token_hex(16)

    MONGODB_SETTINGS = {
                            'db': 'userdata',
                            'host': '127.0.0.1',
                            'port': 27017,
                            'username':'sabya',
                            'password':'sachi'
                        }