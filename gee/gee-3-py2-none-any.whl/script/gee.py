from cryptography.fernet import Fernet
import hashlib
import os
import argparse
import base64
import struct


CHUNK_SIZE = 64 * 1024


def checksum(file):
    return hashlib.md5(open(file, 'rb').read()).hexdigest()


def make_key(passphrase):
    hashed_key = hashlib.sha256(passphrase).digest()
    return base64.b64encode(hashed_key)


def encrypt_file(key, in_file, optional_name=None):
    if optional_name:
        out_file_name = optional_name + os.path.splitext(in_file)[1] + ".gee"
    else:
        out_file_name = in_file + ".gee"

    enc = Fernet(key)

    filesize = os.path.getsize(in_file)

    with open(in_file, "rb") as INFILE:
        with open(out_file_name, "wb") as OUTFILE:
            OUTFILE.write(struct.pack('<Q', filesize))

            while True:
                chunk = INFILE.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += " " * (16 - len(chunk) % 16)
                OUTFILE.write(enc.encrypt(chunk))

    print("Encryption successful: {} \nNew file name: {}".format(
        in_file, out_file_name))


def decrypt_file(key, in_file, sflag, optional_name=None):
    if optional_name:
        suffix = os.path.splitext(in_file)[0]
        suffix = os.path.splitext(in_file)[1]
        out_file_name = optional_name + suffix
    else:
        out_file_name = os.path.splitext(in_file)[0]

    dec = Fernet(key)
    with open(in_file, "rb") as INFILE:
        packed_size = INFILE.read(struct.calcsize("Q"))
        original_size = struct.unpack("<Q", packed_size)[0]

        with open(out_file_name, "wb") as OUTFILE:
            while True:
                chunk = INFILE.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                OUTFILE.write(dec.decrypt(chunk))
            OUTFILE.truncate(original_size)

    print("Decryption successful: {} \nNew file name: {}".format(
        in_file, out_file_name))

    if sflag == None:
        print("Deleting encrypted file.")
        os.remove(in_file)
    else:
        print("Deletion of encrypted file was suppressed.")


def main():
    parser = argparse.ArgumentParser(
        description='Quickly encrypt/decrypt single files. Files are encrypted with Fernet (see https://github.com/fernet/spec)')
    parser.add_argument(
        'infile', help='Name of file to start with. If file ends with ".gee", it will be decrypted. Otherwise the file will be encrypted.')
    parser.add_argument(
        'passphrase', help='Passphrase to be converted to encryption key.')
    parser.add_argument(
        "-n", "--name", help="Rename the output file after encryption/decryption. Gee will take care of file extensions.")
    parser.add_argument(
        "-c", "--checksum", help="Print the MD5 hash of the input file and then exit. No encryption/decryption is done, but you still need to provide a passphrase.", action="count")
    parser.add_argument(
        "-s", "--suppress", help="Suppress deletion of encrypted file after decryption.", action="count")

    args = parser.parse_args()
    key = make_key(args.passphrase)

    if args.checksum > 0:
        print("MD5 for {}:".format(args.infile))
        print(checksum(args.infile))
        exit()

    if os.path.splitext(args.infile)[1] == ".gee":
        try:
            decrypt_file(key, args.infile, args.suppress, args.name)
        except:
            print("Incorrect decryption passphrase. Nothing happened.")
    else:
        encrypt_file(key, args.infile, args.name)


if __name__ == '__main__':
    main()
