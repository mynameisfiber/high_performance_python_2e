from itertools import islice


def index_sequence(key, mask=0b111, PERTURB_SHIFT=5):
    perturb = hash(key)
    i = perturb & mask
    yield i
    while True:
        perturb >>= PERTURB_SHIFT
        i = (i * 5 + perturb + 1) & mask
        yield i


class ForceHash(object):
    def __init__(self, force_hash):
        self.force_hash = force_hash

    def __hash__(self):
        return self.force_hash

    def __repr__(self):
        return f"<ForceHash 0b{self.force_hash:08b}>"


def sample_probe(force_hash, num_samples=10):
    probe_values = index_sequence(force_hash)
    indexes = islice(probe_values, num_samples)
    print(f"First {num_samples} samples for hash {force_hash}: {list(indexes)}")


if __name__ == "__main__":
    sample_probe(ForceHash(0b00000111))
    sample_probe(ForceHash(0b11100111))
    sample_probe(ForceHash(0b01110111))
    sample_probe(ForceHash(0b01110001))
    sample_probe(ForceHash(0b01110000))
