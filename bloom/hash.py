# -----------------------------------------------------------
# Hash functions borrowed and modified from:
#  http://www.partow.net/programming/hashfunctions/index.html
#
# Modified to make them a little more pythonic (iterate over
# strings instead of ranges, remove extraneous parens, etc.)
# because that kind of thing bugs me.  Also added a function
# to reduce each hash to a 32 bit value.
# ----------------------------------------------------------

# Reduce the value returned from a hash function.
# Used because there is no 32 bit limit in python, so
# this reduces the value to a 32 bit value.  Set the
# value to 0 to not modify the hash.
def reduce(hash, size):
    if size != 0:
        while hash > size: hash >>= 1
    return int(hash)

def RSHash(data, size):
    a = 63689
    hash = 0
    for letter in data:
        hash = hash * a + ord(letter)
        a = a * 378551
    return reduce(hash, size)

def JSHash(data, size):
    hash = 1315423911
    for letter in data:
        hash ^= (hash << 5) + ord(letter) + (hash >> 2)
    return reduce(hash, size)

def PJWHash(data, size):
    hash = 0
    high_bits = 0xFFFFFFFF << 28
    for letter in data:
        hash = (hash << 4) + ord(letter)
        test = hash & high_bits
        if test: hash = ((hash ^ (test >> 24)) & (~high_bits))
    return reduce(hash & 0x7FFFFFFF, size)

def ELFHash(data, size):
    hash = 0
    for letter in data:
        hash = (hash << 4) + ord(letter)
        x = hash & 0xF0000000
        if x: hash ^= (x >> 24)
        hash &= ~x
    return reduce(hash, size)

def BKDRHash(data, size):
    seed = 131
    hash = 0
    for letter in data:
        hash = (hash * seed) + ord(letter)
    return reduce(hash, size)

def SDBMHash(data, size):
    hash = 0
    for letter in data:
        hash = ord(letter) + (hash << 6) + (hash >> 16) - hash
    return reduce(hash, size)

def DJBHash(data, size):
    hash = 5381
    for letter in data:
        hash = ((hash << 5) + hash) + ord(letter)
    return reduce(hash, size)

def DEKHash(data, size):
    hash = len(data)
    for letter in data:
        hash = ((hash << 5) ^ (hash >> 27)) ^ ord(letter)
    return reduce(hash, size)

def BPHash(data, size):
    hash = 0
    for letter in data:
        hash = hash << 7 ^ ord(letter)
    return reduce(hash, size)

def FNVHash(data, size):
    fnv_prime = 0x811C9DC5
    hash = 0
    for letter in data:
        hash *= fnv_prime
        hash ^= ord(letter)
    return reduce(hash, size)

def APHash(data, size):
    hash = 0xAAAAAAAA
    for i, letter in enumerate(data):
        if (i & 1) == 0: hash ^= (hash << 7) ^ ord(letter) * (hash >> 3)
        else: hash ^= ~((hash << 11) + ord(letter) ^ (hash >> 5))
    return reduce(hash, size)

def hash(data, size=(2**20), functions=[RSHash, JSHash, PJWHash, ELFHash, 
        BKDRHash, SDBMHash, DJBHash, DEKHash, BPHash, FNVHash, APHash]):
    return [f(data, size) for f in functions]
