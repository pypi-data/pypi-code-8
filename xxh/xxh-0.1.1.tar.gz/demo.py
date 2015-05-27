import numpy as np
import _xxhash as pyxxhash

x = np.arange(1, 9, dtype=np.uint8)
state = pyxxhash.xxh32_init(0)
pyxxhash.xxh32_update(state, x)
print pyxxhash.xxh32_digest(state)

x = bytearray([1, 2, 3, 4, 5, 6, 7, 8])
state = pyxxhash.xxh32_init(0)
pyxxhash.xxh32_update(state, x)
print pyxxhash.xxh32_digest(state)

x = str('\x01\x02\x03\x04\x05\x06\x07\x08')
state = pyxxhash.xxh32_init(0)
pyxxhash.xxh32_update(state, x)
print pyxxhash.xxh32_digest(state)

