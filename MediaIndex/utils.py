import xxhash
def get_str_xxhash(string=""):
    x = xxhash.xxh64()
    x.update(string)
    return x.hexdigest()

def get_xxhash(fname):
    hash64 = xxhash.xxh64()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash64.update(chunk)
    return hash64.hexdigest()
