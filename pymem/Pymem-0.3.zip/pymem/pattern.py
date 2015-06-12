import pymem.memory


def read_memory(handle, start_address, end_address):
    length = end_address - start_address
    bytes = pymem.memory.read_bytes(handle, start_address, length)
    return bytes


