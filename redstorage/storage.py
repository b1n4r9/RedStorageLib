from redis import Redis, ConnectionError
from os import urandom
import pickledb
import re


class Storage:
    def __new__(cls, host="redis", port=6379, filedb="local.db"):
        r = Redis(host, port)
        try:
            if r.ping():
                return RedisStorage(host, port)
            else:
                return FileStorage(filedb)
        except ConnectionError:
            return FileStorage(filedb)


class RedisStorage(Redis):
    def __init__(self, host="redis", port=6379):
        super().__init__(host, port)
        self.tempkey = urandom(10).hex()

    def add(self, vals, key=None):
        if not key:
            key = self.tempkey
        if type(vals) is list or type(vals) is set:
            for i in vals:
                self.sadd(key, i)
        else:
            self.sadd(key, vals)

    def get(self, key=None, data_type="string"):
        if not key:
            key = self.tempkey
        return {x.decode() if data_type == "string" else x for x in self.smembers(key)}

    def getNew(self, vals, key=None, data_type="string"):
        if not key:
            key = self.tempkey
        if type(vals) is list or type(vals) is set:
            vals = {str(x).encode() if type(x) != bytes else x for x in vals}
        elif type(vals) is bytes:
            vals = set([vals])
        else:
            vals = set([str(vals).encode()])

        oldVals = self.get(key, data_type="bytes")
        newVals = vals.difference(oldVals)
        return {x.decode() if data_type == "string" else x for x in newVals}


class FileStorage:
    def __init__(self, filedb="local.db"):
        self.tempkey = urandom(10).hex()
        self.db = pickledb.load(filedb, True)

    def add(self, vals, key=None):
        if not key:
            key = self.tempkey
        if not self.db.exists(key):
            self.db.lcreate(key)
        if type(vals) is list or type(vals) is set:
            for i in set(vals):
                if type(i) == bytes:
                    i = str(i)
                self.db.ladd(key, i)
        elif type(vals) == bytes:
            self.db.ladd(key, str(vals))
        else:
            self.db.ladd(key, vals)

    def get(self, key=None, data_type="string"):
        if not key:
            key = self.tempkey
        if not self.db.exists(key):
            self.db.lcreate(key)
        return {parse_element(x) for x in self.db.lgetall(key)}

    def getNew(self, vals, key=None, data_type="string"):
        if not key:
            key = self.tempkey
        if type(vals) is list or type(vals) is set:
            vals = {x for x in vals}
        else:
            vals = set([vals])

        oldVals = self.get(key)
        newVals = vals.difference(oldVals)
        return {x for x in newVals}


def parse_element(x):
    if type(x) == int:
        return x
    elif re.findall(r"b'(.+)'", x):
        return re.findall(r"b'(.+)'", x)[0].encode()
    else:
        return x
