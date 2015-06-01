# My implementation of a bloom filter

import hashlib

class Bloom:
    def __init__(self, bits=20, hashes=4):
        self.bitsize = bits
        self.size = (1 << bits)
        self.nhashes = hashes
        self.bfilter = bytearray(self.size / 8)
        self.count = 0

    def hash(self, word):
        if type(word) == int: word = str(word)

        val = int(hashlib.sha1(word).hexdigest(), 16)
        ret = []

        for i in xrange(self.nhashes):
            # if we run out of bits, extend the hash with sha1 again
            # not sure how this affects collisions, but it's consistent
            if (val >> self.bitsize) == 0:
                val += int(hashlib.sha1(word).hexdigest(), 16)
            ret.append((val & (self.size - 1)) % self.size)
            val >>= self.bitsize

        return ret

    def set(self, i):
        r = i % 8
        m = i / 8
        self.bfilter[m] |= (1 << (7 - r))

    def check(self, i):
        r = i % 8
        m = i / 8
        res = self.bfilter[m] & (1 << (7 - r))
        res >>= (7 - r)
        if res: return True

    def append(self, word):
        self.count += 1
        for h in self.hash(word): self.set(h)

    def extend(self, words):
        for word in words: self.append(word)

    def __contains__(self, word):
        if all(self.check(h) for h in self.hash(word)): return 1
        return 0

    def __repr__(self):
        return '<Bloom Filter - %s Entries>' % self.count

