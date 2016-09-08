def remove_adjacent(lst):
    n = len(lst)
    i = 0
    while i < n:
        if i > 0 and lst[i - 1] == lst[i]:
            lst.pop(i)
            i -= 1
            n -= 1
        i += 1
    return lst


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
    while i < n1:
        res.append(lst1[i])
        i += 1
    while j < n2:
        res.append(lst2[j])
        j += 1
    return res
