'''
LICENSING
-------------------------------------------------

zbg: A python library for zbg encodings.
    Copyright (C) 2014-2015 Nicholas Badger
    badg@muterra.io
    badg@nickbadger.com
    nickbadger.com

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the 
    Free Software Foundation, Inc.,
    51 Franklin Street, 
    Fifth Floor, 
    Boston, MA  02110-1301 USA

------------------------------------------------------
'''

# Core modules
import collections
from math import ceil
# from .encode import *
# from .decode import *

def dump(obj):
    ''' Serializes the object.
    '''
    # In for a penny, in for a pound.
    if isinstance(obj, collections.Mapping):
        # Sort by the big-endian integer representation
        zbg = b'd'
        ordered = sorted(list(obj), key=lambda x: int.from_bytes(x, 'big'))
        for key in ordered:
            zbg += dump(key) + dump(obj[key])
        zbg += b'e'
    elif isinstance(obj, collections.MutableSequence):
        zbg = b'l'
        for value in obj:
            zbg += dump(value)
        zbg += b'e'
    else:
        # Look for the buffer interface to define bytes.
        try:
            memoryview(obj)
            # If that succeeded, it bytes-like, and we can continue
        except TypeError:
            raise TypeError('Object cannot be implicitly converted to a zbg-'
                            'encoded bytestream. Check object typing.')
            
        # How long?
        size = len(obj)
        # Check for 256-bit hash/etc
        if size == 32:
            flag = b'h'
        # Check for 512-bit hash/etc
        elif size == 64:
            flag = b'H'
        # Nope, arbitrary size binary
        else:
            # Start off with the flag
            flag = b':'
            # Figure out how many octets are needed for the object's length
            bytes_for_len = ceil(size.bit_length() / 8)
            # Pack that into the first byte after the flag
            flag += bytes_for_len.to_bytes(1, 'big')
            # Pack the actual length immediately thereafter
            flag += size.to_bytes(bytes_for_len, 'big')
        # Okay, everything has been flagged correctly. Create the serialization
        zbg = flag + obj
        
    # Return.
    return zbg
   
    
def dumpf(obj, f):
    ''' Dumps the object into an open file handle f.
    '''
    f.write(b'zbg0')
    f.write(dump(obj))
    # That was easy
    
    
def load(zbg):
    ''' Loads a zbg.
    '''
    # Do a quick check that it's bytes-like
    try:
        memoryview(zbg)
    except TypeError:
        raise TypeError('All zbg blobs must support the buffer protocol.')
    
    zbg_deque = collections.deque([b.to_bytes(1, 'big') for b in zbg])
    return _deserialize(zbg_deque)
    
    
def _deserialize(b):
    ''' Recursive helper for loading.
    '''
    # The leftmost byte should always be the type flag.
    flag = b.popleft()
    # Handle all lists
    if flag == b'l':
        # Preinitialize
        obj = []
        # Loop until break
        while True:
            # Call recursively over the poplefted obj
            bj = _deserialize(b)
            # Check to see if we reached the end yet
            if bj != None:
                obj.append(bj)
            else:
                break
    # Handle all dictionaries
    elif flag == b'd':
        # Preinitialize
        obj = {}
        # Loop until break
        while True:
            # First field will be the key
            key = _deserialize(b)
            # Make sure we didn't hit the end of the container
            if key == None:
                break
            # Second field will be the value
            value = _deserialize(b)
            # And now add it to obj.
            obj[key] = value
    # 256-bit "hash"
    elif flag == b'h':
        # Predeclare empty bytes
        obj = b''
        # Concatenate the next 32 bytes
        for __ in range(32):
            obj += b.popleft()
    # 512-bit "hash"
    elif flag == b'H':
        # Predeclare empty bytes
        obj = b''
        # Concatenate the next 64 bytes
        for __ in range(64):
            obj += b.popleft()
    # Arbitrary binary
    elif flag == b':':
        # The first byte says how many octets the length description uses
        len_octets = int.from_bytes(b.popleft(), 'big')
        # Get those bytes and convert them to the integer they represent
        blob_len = b''
        for __ in range(len_octets):
            blob_len += b.popleft()
        blob_len = int.from_bytes(blob_len, 'big')
        # Now predeclare the final object
        obj = b''
        # And concatenate the rest of it
        for __ in range(blob_len):
            obj += b.popleft()
    # We've reached the end of a container.
    elif flag == b'e':
        # Return!
        return None
    # Something went wrong.
    else:
        raise ValueError('Improperly-formed zbg.')
        
    # And finally, return the created object.
    return obj
    
    
def loadf(f):
    ''' Reads an object from an open file handle f.
    '''
    f = f.read()
    magic = f[0:4]
    if magic != b'zbg0':
        raise ValueError('File does not appear to be a standalone zbg.')
    zbg = f[4:]
    return load(zbg)
    # That was also easy