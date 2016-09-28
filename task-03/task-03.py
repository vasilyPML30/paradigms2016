import math
import numpy


def read(real_size, size):
    matr = numpy.zeros(shape=(size, size), dtype=int)
    for i in range(real_size):
        j = 0
        for n in input().split(' '):
            matr[i][j] = n
            j += 1
    return matr


def write(matr, size):
    for i in range(size):
        for j in range(size):
            print(matr[i][j], end=" ")
        print()


def mult(M1, M2):
    m1 = M1.copy()
    m2 = M2.copy()
    size = m1.shape[0]
    if size == 1:
        m1[0][0] *= m2[0][0]
        return m1
    size >>= 1
    A = numpy.ndarray(shape=(2, 2, size, size), dtype=int)
    B = numpy.ndarray(shape=(2, 2, size, size), dtype=int)
    C = numpy.ndarray(shape=(2, 2, size, size), dtype=int)
    for i in range(2):
        for j in range(2):
            A[i][j] = m1[size * i:size * (i + 1), size * j:size * (j + 1)]
    for i in range(2):
        for j in range(2):
            B[i][j] = m2[size * i:size * (i + 1), size * j:size * (j + 1)]
    P1 = mult(A[0][0] + A[1][1], B[0][0] + B[1][1])
    P2 = mult(A[1][0] + A[1][1], B[0][0])
    P3 = mult(A[0][0], B[0][1] - B[1][1])
    P4 = mult(A[1][1], B[1][0] - B[0][0])
    P5 = mult(A[0][0] + A[0][1], B[1][1])
    P6 = mult(A[1][0] - A[0][0], B[0][0] + B[0][1])
    P7 = mult(A[0][1] - A[1][1], B[1][0] + B[1][1])
    C[0][0] = P1 + P4 + P7 - P5
    C[0][1] = P3 + P5
    C[1][0] = P2 + P4
    C[1][1] = P1 + P3 + P6 - P2
    ans = numpy.ndarray(shape=(size << 1, size << 1), dtype=int)
    for i in range(2):
        for j in range(2):
            ans[size * i:size * (i + 1), size * j:size * (j + 1)] = C[i][j]
    return ans


def main():
    real_size = int(input())
    size = 1 << math.ceil(math.log2(real_size))
    matr1 = read(real_size, size)
    matr2 = read(real_size, size)
    write(mult(matr1, matr2), real_size)


if __name__ == "__main__":
    main()
