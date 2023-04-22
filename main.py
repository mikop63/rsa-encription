import random
import math
import time


def Miller_Rabbin_test(n: int, k=25) -> int:
    """
    Тест, который определит составное число или возможно простое

    :param n: число, которое проверяется на простату
    :param k: число раундов
    :return: 0 - число вероятно простое, 1 - составное
    """

    s = 0
    t = n - 1
    while t % 2 == 0:
        t //= 2
        s += 1
    a = random.randint(2, n - 2)
    for i in range(k):
        x = pow(a, t, n)  # a^t%n
        if x == 1 or x == n - 1:
            continue
        for j in range(s - 1):
            x = pow(x, 2, n)
            if x == 1:
                return 1
            if x == n - 1:
                break
        else:
            return 1  # для for
    return 0


def generate() -> int:
    """
    Функция сгенерирует число

    :return: нечетное число длиной от 511 до 512 бит
    """
    numb = random.randint(2 ** 511, 2 ** 512) | 1
    Miller_Rabbin = Miller_Rabbin_test(numb)
    while Miller_Rabbin == 1:
        numb += 2
        Miller_Rabbin = Miller_Rabbin_test(numb)
    return numb


def Euclid_ext(a: int, b: int) -> tuple:
    """
    Расширенный алгоритм Евклида. Находит наибольший общий делитель

    :param a:
    :param b:
    :return: a*u[1] + b*u[2] = u[0]
    """
    u = (a, 1, 0)
    v = (b, 0, 1)
    while v[0] > 0:
        q = u[0] // v[0]
        t = (u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2])
        u = v
        v = t
    return u


def invert(a: int, m: int) -> int:
    u = Euclid_ext(a, m)
    if u[0] > 1: # Если НОД > 1 вернется ошибка
        raise ValueError('No inverse')
    return u[1] % m


def encode_str_to_int(message: str) -> int:
    """
    Перевод текста в int.

    :param message: текст, который переведется в тип int
    :return: закодированный текст
    """
    b = bytes(str(message), encoding='utf-8')
    x = int.from_bytes(b, byteorder='big')
    return x


def decode_int_to_str(enc_message: int) -> str:
    """
    Переводим из int в str

    :param enc_message: комбинация int
    :return: раскодированная строка
    """
    b = enc_message.to_bytes((enc_message.bit_length() + 7) // 8,
                             byteorder='big')  # вычисляем количество байтов, которое требуется для хранения числа
    # если x занимает 10 бит, мы должны зарезервировать 2 байта (16 бит), а не только 1 байт, чтобы сохранить это число
    return str(b, encoding='utf-8')


def encryption(message: int, e: int, n: int) -> int:
    """
    Шифрование bytes. Возводим сообщение в степень e по модулю n

    :param message: Шифруемое сообщение
    :param e: отрытая экспонента
    :param n: модуль
    :return: Зашифрованное сообщение
    """
    return pow(message, e, n)


def decryption(message: int, d: int, n: int) -> int:
    return pow(message, d, n)


def pkcs1_v1_5_enctypt(n: int, message: int, e):
    """
    Приводим зашифрованное сообщение к стандарту rfc8017, чтобы из-за короткого сообщение нельзя было взломать ключ
    :param n: модуль
    :param message: зашифрованное сообщение
    :return:
    """

    # https://datatracker.ietf.org/doc/html/rfc8017#section-7.2.1
    # пункты 7.2.1 , 7.2.2
    # EM = 0x00 | | 0x02 | | PS | | 0x00 | | M
    # 0x00 | | 0x02 - сигнатура
    # PS - случайный набор цифр, без 0, не меньше 8 байт
    # 0x00 - отделяет payload от сообщения
    # нужно, чтобы нельзя было подобрать ключ если зашифрованное сообщение мало

    # считаем количество байт в числе n
    k = int(math.log(n, 2) // 8 + 1)  # второй вариант int(math.log(n, 256) + 1). Байты - числа от 0 до 255
    mLen = int(math.log(message, 2) // 8 + 1)
    if mLen > k - 11:
        raise ValueError('Сообщение слишком длинное')

    # TODO: уточнить сколько цифр генерировать
    payloads = [random.randint(1, 255) for i in range(10)]
    header = bytes([0, 2]) + bytes(payloads) + bytes([0]) + message.to_bytes((message.bit_length() + 7) // 8,
                                                                             byteorder='big')
    header_int = int.from_bytes(header, byteorder='big')
    return encryption(header_int, e, n)


def pkcs1_v1_5_decrypt(em, d, n):
    # Шаг 1: расшифровываем RSA
    em_int = decryption(em, d, n)

    # Шаг 2: EM = 0x00 || 0x02 || PS || 0x00 || M
    # Извлекаем M из EM
    # TODO: bytes([0]) + -это костыль. Почему-то в сигнатуре вместо: b'\x00\x02, получается: b'\x02
    em_bytes = bytes([0]) + em_int.to_bytes((em_int.bit_length() + 7) // 8, byteorder='big')
    ps_index = em_bytes.index(0x00, 0x02)  # Находим разделитель
    ps = em_bytes[2:ps_index]
    m = em_bytes[ps_index + 1:]
    if em_bytes[:2] != b'\x00\x02' or len(ps) < 8:
        raise ValueError('Не верная сигнатура PKCS#1 v1.5')
    return m


if __name__ == '__main__':
    print('*** \t [Код готов к шифрованию] \t ***');time.sleep(3)
    message = str(input('Введите сообщение: '))
    print('*** \t [Генерация числа p...] \t ***');time.sleep(7)
    p = generate()
    print(f"Число p: {p}")
    print('*** \t [Генерация числа q...] \t ***');time.sleep(4)
    q = generate()
    print(f"Число q: {q}")
    n = p * q
    fi = (p - 1) * (q - 1)
    e = 65537  # это в двоичной системе 100...(15)...001
    print('*** \t [Вычисление d...] \t\t ***');time.sleep(11)
    d = invert(e, fi)  # вычисляем e = d mod(fi). d - это обратное число e
    print(f"Число d: {d}")

    # e, n - открытый ключ
    # d, n - закрытый ключ

    # message = 'Только представьте, сколько занимает времени и усилий переводить тех'
    # message = 'Только представьте, сколько занимает времени и усилий переводи'
    # message = 'переводи'
    print('*** \t [Идет процесс шифрования] \t ***');time.sleep(10)
    enc_mess = pkcs1_v1_5_enctypt(n, encode_str_to_int(message), e)
    print(f"Результат шифрования:\n{enc_mess}")

    print('*** \t [Начинается процесс расшифрования] \t ***');time.sleep(13)
    decrypt_mess = pkcs1_v1_5_decrypt(enc_mess, d, n).decode('utf-8')
    print(f'Расшифрованное сообщение:\n{decrypt_mess}')
