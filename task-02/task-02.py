import os
import hashlib
import time
import argparse

equal_files = {}

def walk_through(rootdir):
	omit = len(rootdir) + 1
	for subdir, dirs, files in os.walk(rootdir):
		first_char = subdir.split('/')[-1][0]
		dirs[:] = [d for d in dirs if not d[0] == '.' and not d[0] == '~']
		for file in files:
			file = subdir + '/' + file
			hash = get_hash(file)
			if equal_files.__contains__(hash):
				equal_files[hash] += (file[omit:], )
			else:
				equal_files.update({hash: (file[omit:], )})

def get_hash(file):
	f = open(file, 'rt')
	sha1 = hashlib.sha1()
	while True:
		part = f.read(50000)
		sha1.update(part.encode("utf-8"))
		if len(part) == 0:
			break
	f.close()
	return sha1.hexdigest()

def main():
	parser = argparse.ArgumentParser(description="output files with equal content")
	parser.add_argument("path", type=str, help="home directory")
	args = parser.parse_args()
	walk_through(args.path)
	for file in equal_files:
		print(':'.join(equal_files[file]) + '\n' if len(equal_files[file]) > 1 else "", end = "")

#if __name__ == "__main__":
main()