import random

def Miller_Rabbin_test(n, k = 25):
    """
997 - простое
999 - составное
    :param numb:
    :param k: число раундов
    :return: 0 - число вероятно простое, 1 - составное
    """

    s = 0
    t = n - 1
    while t%2 == 0:
        t //= 2
        s += 1
    a = random.randint(2, n - 2)
    for i in range(k):
        x = pow(a, t, n) # a^t%n
        if x == 1 or x == n - 1:
            continue
        for j in range(s - 1):
            x = pow(x, 2, n)
            if x == 1:
                return 1
            if x == n - 1:
                break
        else:
            return 1 # для for
    return 0

def generate():
    numb = random.randint(2 ** 511, 2 ** 512) | 1  # число длиной от 511 до 512 бит, нечетное
    Miller_Rabbin = Miller_Rabbin_test(numb)
    while Miller_Rabbin == 1:
        numb += 2
        Miller_Rabbin = Miller_Rabbin_test(numb)
    return numb

def euclid_ext(a, b):
    """
    Расширенный алгоритм Евклида

    :param a:
    :param b:
    :return: a*u[1] + b*u[2] = u[0]
    """
    u = (a, 1, 0)
    v = (b, 0, 1)
    while v[0]>0:
        q = u[0]//v[0]
        t = (u[0]%v[0], u[1] - q*v[1], u[2]- q*v[2])
        u = v
        v = t
    return u

def invert(a, m):
    u = euclid_ext(a, m)
    if u[0]>1:
        return 'No inverse'
    return u[1]%m

if __name__ == '__main__':
    p = generate()
    q = generate()
    n = p * q
    fi = (p - 1) * (q - 1)
    e = 65537 # это в двоичке 100...(15)...001
    d = (invert(e, fi)) # вычисляем e = d mod(fi). d - это обратное число e

    # e, n - открытый ключ
    # d, n - закрытый ключ

