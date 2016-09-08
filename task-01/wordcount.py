import sys


def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words


def Count(words):
    res = dict.fromkeys(words, 0)
    for i in words:
        res[i] += 1
    return res


def print_words(fname):
    ans = Count(read_words(fname))
    ans = sorted(ans.items())
    for i in ans:
        print(i[0], i[1])


def print_top(fname):
    ans = Count(read_words(fname))
    ans = sorted(ans.items(), key = lambda x: x[1], reverse = True)
    for i in ans[:20]:
        print(i[0], i[1])


def main():
    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)
    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)


if __name__ == '__main__':
    main()
