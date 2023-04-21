import jwt
import datetime


def get_token(usermail):
    payload = {
        'id': usermail,
        'is_staff': False,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret',
                       algorithm='HS256')
    return token
