import xxhash
def get_xxhash(string=""):
    x = xxhash.xxh64()
    x.update(string)
    return x.hexdigest()