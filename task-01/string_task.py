def verbing(s):
    if len(s) >= 3:
        if s[-3:] == "ing":
            s += "ly"
        else:
            s += "ing"
    return s


def not_bad(s):
    a = s.find("not")
    b = s.find("bad")
    print(a)
    if 0 <= a < b:
        return s[:a] + "good" + s[b + 3:]
    return s


def front_back(a, b):
    x = (len(a) + 1) // 2
    y = (len(b) + 1) // 2
    return a[:x] + b[:y] + a[x:] + b[y:]
