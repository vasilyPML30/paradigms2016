import math
import numpy
import sys


def read(real_size, size):
    matr = numpy.zeros(shape=(size << 1, size), dtype=int)
    inpt = numpy.loadtxt(sys.stdin, ndmin=2)
    matr[:real_size, :real_size] = inpt[:real_size]
    matr[size:size + real_size, :real_size] = inpt[:real_size]
    return matr


def write(matr, size):
    for row in matr[:size, :size]:
        print(*row)


def mult(M1, M2):
    m1 = M1.copy()
    m2 = M2.copy()
    size = m1.shape[0]
    if size == 1:
        m1[0][0] *= m2[0][0]
        return m1
    size >>= 1
    A00 = m1[:size, :size]
    A01 = m1[:size, size:]
    A10 = m1[size:, :size]
    A11 = m1[size:, size:]

    B00 = m2[:size, :size]
    B01 = m2[:size, size:]
    B10 = m2[size:, :size]
    B11 = m2[size:, size:]

    P1 = mult(A00 + A11, B00 + B11)
    P2 = mult(A10 + A11, B00)
    P3 = mult(A00, B01 - B11)
    P4 = mult(A11, B10 - B00)
    P5 = mult(A00 + A01, B11)
    P6 = mult(A10 - A00, B00 + B01)
    P7 = mult(A01 - A11, B10 + B11)

    C00 = P1 + P4 + P7 - P5
    C01 = P3 + P5
    C10 = P2 + P4
    C11 = P1 + P3 + P6 - P2

    ANS = numpy.zeros(shape=(size << 1, size << 1), dtype=int)

    ANS[:size, :size] = C00
    ANS[:size, size:] = C01
    ANS[size:, :size] = C10
    ANS[size:, size:] = C11

    return ANS


def main():
    real_size = int(input())
    size = 1 << math.ceil(math.log2(real_size))
    matr = read(real_size, size)
    write(mult(matr[:size], matr[size:]), real_size)


if __name__ == "__main__":
    main()
