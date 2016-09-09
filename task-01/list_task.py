def remove_adjacent(lst):
    n = len(lst)
    i = 1
    res = list()
    if n == 0:
        return lst
    res.append(lst[0])
    while i < n:
        if lst[i - 1] != lst[i]:
            res.append(lst[i])
        i += 1
    return res


def linear_merge(lst1, lst2):
    res = []
    i = 0
    j = 0
    n1 = len(lst1)
    n2 = len(lst2)
    while i < n1 and j < n2:
        if lst1[i] <= lst2[j]:
            res.append(lst1[i])
            i += 1
        else:
            res.append(lst2[j])
            j += 1
    res.extend(lst1[i:])
    res.extend(lst2[j:])
    return res
