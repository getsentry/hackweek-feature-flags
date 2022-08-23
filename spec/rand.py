import hashlib
import struct


MASK = 0xffffffff


class XorShift(object):

    def __init__(self, seed=None):
        self.state = [0] * 4
        if seed is not None:
            self.seed(seed)

    def seed(self, seed):
        bytes = hashlib.sha1(seed.encode("utf-8")).digest()
        # 4 big endian integers, eg:
        #   (x[0] << 24) | (x[1] << 16) | (x[2] << 8) | (x[3])
        self.state[:] = struct.unpack(">IIII", bytes[:16])

    def next(self):
        t = self.state[3]
        s = self.state[0]

        self.state[3] = self.state[2]
        self.state[2] = self.state[1]
        self.state[1] = s

        t = (t << 11) & MASK
        t ^= t >> 8
        self.state[0] = (t ^ s ^ (s >> 19)) & MASK

        return self.state[0] / MASK


def prandom(sticky_id):
    rand = XorShift(seed=sticky_id)
    return rand.next()
