import unittest
import random
from main import *


class TestRSACode(unittest.TestCase):

    def test_Miller_Rabbin_test(self):
        array = [
            997, 999
        ]
        expected_array = [
            0, 1
        ]

        # Проверяем правильность кодирования каждой строки
        for i in range(len(array)):
            self.assertEqual(expected_array[i], Miller_Rabbin_test(array[i]))

    def test_generate_is_odd(self):
        random.seed(123)  # устанавливаем начальное значение генератора
        generated_num = generate()
        self.assertTrue(generated_num % 2 == 1)

    def test_generated_number_is_prime(self):
        random.seed(456)
        generated_num = generate()
        self.assertTrue(Miller_Rabbin_test(generated_num) == 2)

    def test_generated_numbers_are_different(self):
        # проверка, что числа отличаются
        random.seed(789)
        generated_nums = set() # создаем множество уникальных элементов
        for i in range(10):
            generated_nums.add(generate())
        self.assertTrue(len(generated_nums) == 10)

    def test_gcd(self):
        self.assertEqual(Euclid_ext(10, 25), (5, -2, 1))
        self.assertEqual(Euclid_ext(14, 28), (14, 1, 0))
        self.assertEqual(Euclid_ext(3, 5),   (1, 2, -1))
        self.assertEqual(Euclid_ext(0, 7),   (7, 0, 1) )
        self.assertEqual(Euclid_ext(10, 0),  (10, 1, 0))

    def test_invert(self):
        assert invert(5, 7) == 3
        assert invert(11, 17) == 14
        assert invert(128, 397) == 183

        try:
            invert(128, 396)
        except ValueError as e:
            assert str(e) == 'No inverse'

        try:
            invert(4, 8)
        except ValueError as e:
            assert str(e) == 'No inverse'

        try:
            invert(2, 4)
        except ValueError as e:
            assert str(e) == 'No inverse'

    def test_encode_str_to_int(self):
        message = "Hello, world!"
        expected_result = 5735816763073854953388147237921
        result = encode_str_to_int(message)
        self.assertEqual(result, expected_result)

    def test_decode_int_to_str(self):
        message = 5735816763073854953388147237921
        expected_result = "Hello, world!"
        result = decode_int_to_str(message)
        self.assertEqual(result, expected_result)

    def test_encryption_small_numbers(self):
        message = 123
        e = 17
        n = 3233
        expected_result = 855
        self.assertEqual(encryption(message, e, n), expected_result)

    def test_encryption_large_numbers(self):
        message = 123456789
        e = 65537
        n = 18446744073709551629
        expected_result = 15778489691901747283
        self.assertEqual(encryption(message, e, n), expected_result)

    def test_encryption_zero_message(self):
        message = 0
        e = 17
        n = 3233
        expected_result = 0
        self.assertEqual(encryption(message, e, n), expected_result)

    def test_decryption_small_numbers(self):
        message = 855
        d = 2753
        n = 3233
        expected_result = 123
        self.assertEqual(decryption(message, d, n), expected_result)

    # def test_decryption_large_numbers(self):
    #     message = 15778489691901747283
    #     d = # TODO: получить
    #     n = 18446744073709551629
    #     expected_result = 123456789
    #     self.assertEqual(decryption(message, d, n), expected_result)

    def test_decryption_zero_message(self):
        # Test decryption of zero message
        message = 0
        d = 2753
        n = 3233
        expected_result = 0
        self.assertEqual(decryption(message, d, n), expected_result)

    def test_correct_length_message(self):
        """
        Проверяем чтобы вернуло не None
        """
        n = 95376459628305386763374032189781479946327966544355604413859597819135360234248586168591901659656404714340934629364048730553612647810195039090836512244107416432648598184245827573235406573668064510832442743287692810563639229246811883010643066541950799281763142355209184866640641358016693250755164268213017442283
        e = 65537
        message = 379695298917877702867225477352799283
        result = pkcs1_v1_5_enctypt(n, message, e)
        self.assertIsNotNone(result)

    def test_too_long_message(self):
        """
        Передаем слишком длинное сообщение
        """
        n = 123456789
        e = 65537
        message = 10**20
        with self.assertRaises(ValueError):
            pkcs1_v1_5_enctypt(n, message, e)