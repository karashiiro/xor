import argparse
from os import path
import sys

parser = argparse.ArgumentParser(description="Save an XOR'd copy of a file.")
parser.add_argument("--file", "-f", dest="file_path", nargs=1, type=str, required=True,
    help="Path to the file to be XOR'd.")
parser.add_argument("--key", "-k", dest="xor_key", nargs=1, type=str, required=True,
    help="XOR key to apply to the file.")
parser.add_argument("--suffix", dest="suffix", nargs=1, type=str, default="_xor",
    help="Optional suffix for the output file.")
args = parser.parse_args(sys.argv[1:])

if len(args.xor_key[0]) % 2 != 0:
    print("error: xor encryption key length must be divisible by 2")
    sys.exit(1)

xor_byte_count = int(len(args.xor_key[0]) / 2)
xor_key_bytes = [int(args.xor_key[0][i*2:i*2+2], base=16) for i in range(0, xor_byte_count)]

new_contents_list = []
with open(args.file_path[0], "rb") as f:
    contents = f.read()
    i = 0
    for x in contents:
        new_contents_list.append(x ^ xor_key_bytes[i])
        i += 1
        if i == len(xor_key_bytes):
            i = 0
new_contents = bytes(new_contents_list)

dir_name, file_name = path.split(args.file_path[0])
fn_no_ext, ext = path.splitext(file_name)
out_path = path.join(dir_name, fn_no_ext + args.suffix + ext)
with open(out_path, "wb") as o:
    o.write(new_contents)
