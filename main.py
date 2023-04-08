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

if __name__ == '__main__':
    p = generate()
    q = generate()



