import math
import numpy


def read(real_size, size):
    matr = numpy.ndarray(shape=(size, size), dtype=int)
    matr.fill(0)
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


def plus(M1, M2):
    m1 = M1.copy()
    m2 = M2.copy()
    size = m1.shape[0]
    for i in range(size):
        for j in range(size):
            m1[i][j] += m2[i][j]
    return m1


def minus(M1, M2):
    m1 = M1.copy()
    m2 = M2.copy()
    size = m1.shape[0]
    for i in range(size):
        for j in range(size):
            m1[i][j] -= m2[i][j]
    return m1


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
            for a in range(size):
                for b in range(size):
                    A[i][j][a][b] = m1[size * i + a][size * j + b]
    for i in range(2):
        for j in range(2):
            for a in range(size):
                for b in range(size):
                    B[i][j][a][b] = m2[size * i + a][size * j + b]
    P1 = mult(plus(A[0][0], A[1][1]), plus(B[0][0], B[1][1]))
    P2 = mult(plus(A[1][0], A[1][1]), B[0][0])
    P3 = mult(A[0][0], minus(B[0][1], B[1][1]))
    P4 = mult(A[1][1], minus(B[1][0], B[0][0]))
    P5 = mult(plus(A[0][0], A[0][1]), B[1][1])
    P6 = mult(minus(A[1][0], A[0][0]), plus(B[0][0], B[0][1]))
    P7 = mult(minus(A[0][1], A[1][1]), plus(B[1][0], B[1][1]))
    C[0][0] = plus(plus(P1, P4), minus(P7, P5))
    C[0][1] = plus(P3, P5)
    C[1][0] = plus(P2, P4)
    C[1][1] = plus(plus(P1, P3), minus(P6, P2))
    ans = numpy.ndarray(shape=(size << 1, size << 1), dtype=int)
    for i in range(2):
        for j in range(2):
            for a in range(size):
                for b in range(size):
                    ans[size * i + a][size * j + b] = C[i][j][a][b]
    return ans


def main():
    real_size = int(input())
    size = 1 << math.ceil(math.log2(real_size))
    matr1 = read(real_size, size)
    matr2 = read(real_size, size)
    write(mult(matr1, matr2), real_size)


if __name__ == "__main__":
	main()