from passlib.hash import bcrypt_sha256


def get_password(password):
    return bcrypt_sha256.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_sha256.verify(plain_password, hashed_password)
   