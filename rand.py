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

    def next_u32(self):
        t = self.state[3]
        s = self.state[0]

        self.state[3] = self.state[2]
        self.state[2] = self.state[1]
        self.state[1] = s

        t = (t << 11) & MASK
        t ^= t >> 8
        self.state[0] = (t ^ s ^ (s >> 19)) & MASK

        return self.state[0]

    def next(self):
        self.next_u32() / MASK


def prandom(seed):
    rand = XorShift(seed=seed)
    return rand.next()


def test():
    rand = XorShift(seed="wohoo")
    assert rand.next_u32() == 3709882355
    assert rand.next_u32() == 3406141351
    assert rand.next_u32() == 2220835615
    assert rand.next_u32() == 1978561524
    assert rand.next_u32() == 2006162129
    assert rand.next_u32() == 1526862107
    assert rand.next_u32() == 2715875971
    assert rand.next_u32() == 3524055327
    assert rand.next_u32() == 1313248726
    assert rand.next_u32() == 1591659718


if __name__ == '__main__':
    test()
