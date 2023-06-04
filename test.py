import jwt
import datetime

expire = datetime.datetime.utcnow()
print(expire.timestamp())
def decode_token(token: str):
    try:
        decode_token = jwt.decode(token, "SECRET", algorithms=['HS256'])
        return decode_token if decode_token['exp'] >= datetime.datetime.utcnow().timestamp() else None
    except:
        return {}


token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiNjIyMzYwYzAtNjA1ZS00ZWM2LWJlYjItNDY3NzJlMTZiMTAzIiwidXNlcm5hbWUiOiJzdHJpbmciLCJleHAiOjE2ODU4NjUzNjh9.LN7BksEnPRep5isB9CBCEjJfStrSKPi_7bVDaWIiWqk'

decode_token1 = decode_token(token)
decode_token = jwt.decode(token, 'SECRET', algorithms=["HS256"])

print(decode_token)
print(decode_token1)