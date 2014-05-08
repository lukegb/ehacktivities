import json

from cryptography.fernet import Fernet


class SessionDataEncryptor(object):
    def __init__(self, key, lifetime=3600):
        self.fernet = Fernet(key)
        self.lifetime = lifetime

    def encode(self, data):
        return self.fernet.encrypt(data)

    def decode(self, data):
        return self.fernet.decrypt(data, ttl=self.lifetime)


class JsonSessionDataEncoder(object):
    def encode(self, data):
        return json.dumps(data)

    def decode(self, data):
        return json.loads(data)


class ChainingEncoder(object):
    def __init__(self, objs):
        self.objs = objs

    def encode(self, data):
        return reduce(lambda y, x: x.encode(y), self.objs, data)

    def decode(self, data):
        return reduce(lambda y, x: x.decode(y), reversed(self.objs), data)
