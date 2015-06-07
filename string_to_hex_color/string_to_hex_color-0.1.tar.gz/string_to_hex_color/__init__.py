import hashlib

####################################################

def string_to_hex_color(str, include_hash=0):
    
    hash_object = hashlib.md5(str)

    hex_color = hash_object.hexdigest()
    hex_color = hex_color[:6]

    if (include_hash):
        hex_color = "#" + hex_color
        
    return  hex_color
