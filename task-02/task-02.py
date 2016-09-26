import os
import hashlib
import time
import argparse
from collections import defaultdict


def walk_through(rootdir):
	equal_files = defaultdict(list)
	for subdir, _, files in os.walk(rootdir):
		for file in files:
			if not file[0] == '.' and not file[0] == '~' and not os.path.islink(file):
				file = os.path.join(subdir, file)
				hash = get_hash(file)
				equal_files[hash].append(os.path.relpath(file))
	return equal_files


def get_hash(file):
	with open(file, 'rb') as f:
		sha1 = hashlib.sha1()
		while True:
			part = f.read(50000)
			sha1.update(part)
			if not part:
				break
	return sha1.hexdigest()


def main():
	parser = argparse.ArgumentParser(
	description="output files with equal content")
	parser.add_argument("path", type=str, help="home directory")
	args = parser.parse_args()
	equal_files = walk_through(args.path)
	for value in equal_files.values():
		if len(value) > 1:
			print(':'.join(value))

# if __name__ == "__main__":
main()
