import time
import jwt
import json


def handler(event, context):
    if "secret" not in event or "kid" not in event or "iss" not in event:
        return {"statusCode": 400, "message": "Invalid token params"}

    secret = event["secret"]
    alg = event["alg"] if "alg" in event else "ES256"
    kid = event["kid"]
    iss = event["iss"]
    iat = event["iat"] if "iat" in event else time.time()
    token = get_jwt(secret, kid, iss, iat, alg)

    return {"token": token}


def get_jwt(secret, kid, iss, iat, alg):
    key = f"""
-----BEGIN PRIVATE KEY-----
{secret}
-----END PRIVATE KEY-----"""
    headers = {"alg": alg, "kid": kid}
    payload = {"iss": iss, "iat": iat}
    token = jwt.encode(payload, key, algorithm=[alg], headers=headers)

    return token
