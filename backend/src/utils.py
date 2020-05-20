import random
import btree
import json

def random_shuffle(seq):
    l = len(seq)
    for i in range(l):
        j = random.randrange(l)
        seq[i], seq[j] = seq[j], seq[i]

class DB:
    try:
        f = open("settings", "r+b")
    except OSError:
        f = open("settings", "w+b")

    db = btree.open(f)


    if not set(db.keys()) & {b"led", b"state"}:
        db[b"led"] = json.dumps({"r":0, "g":0, "b":0}).encode()
        db[b"first_setup"] = json.dumps({'first_setup': True}).encode()
        db[b"auto_time"] = json.dumps({'auto_time': False}).encode()
        db.flush()

    @classmethod
    def commmit(cls, key, value):
        cls.db[key] = value
        cls.db.flush()

    @classmethod
    def fetch(cls, key):
        return cls.db[key] 

    @classmethod
    def close(cls):
        cls.db.close()
        cls.f.close()
