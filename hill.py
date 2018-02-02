from ciphers import Cipher
import numpy as np
import random
import pep8
import sys


class Hill(Cipher):
    def __init__(self):
        abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ-'
        self.arith_abc = {char: number for number,
                          char in zip(range(0, len(abc)), abc)}
        self.inv_arith_abc = {v: k for k, v in self.arith_abc.items()}
        self.key_m_size = 3
        self.key_needed_to_encrypt = False
        self.key_needed_to_decrypt = True
        sys.setrecursionlimit(1000000)

    def egcd(self, a, b):
        '''This method calculates the extended greatest common
        divisor of two positive integers. The source of this
        code is:
        https://en.wikibooks.org/wiki/Algorithm_Implementation/
        ..Mathematics/Extended_Euclidean_algorithm
        The method returns '''
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = self.egcd(b % a, a)
            return (g, y - (b // a) * x, x)

    def mulinv(self, det, len_of_abc):
        '''This method takes two arguments and calculates the
        modular inverse of it and returns it.
        The source of this code is:
        https://en.wikibooks.org/wiki/Algorithm_Implementation/
        ..Mathematics/Extended_Euclidean_algorithm'''
        g, x, _ = self.egcd(det, len_of_abc)
        if g == 1:
            return x % len_of_abc

    def minor(self, np_matrix):
        '''This method takes the a square matrix in numpy format and
        returns the minor of it.'''
        minor = np.ones((np_matrix.shape[0], np_matrix.shape[0]))
        if np_matrix.shape[0] != np_matrix.shape[1]:
            raise ValueError('Input is not a square matrix')
        for n in range(len(np_matrix)):
            for m in range(len(np_matrix)):
                reducedn = np.delete(np_matrix, n, axis=0)
                reducedm = np.delete(reducedn, m, axis=1)
                minor[n, m] = np.linalg.det(reducedm)
        return minor

    def adj_sign(self, np_matrix):
        '''This method takes a 3x3 numpy matrix and multiplies it with
        this adjacent sign matrix:
        [1, -1, 1], [-1, 1, -1], [1, -1, 1]]
        The altered numpy matrix is returned.'''
        if np_matrix.shape[0] != np_matrix.shape[1]:
            raise ValueError('Input is not a square matrix')
        return np.multiply(np_matrix, np.matrix([[1, -1, 1],
                                                 [-1, 1, -1],
                                                 [1, -1, 1]]))

    def encrypt(self, text):
        '''This method takes a text as input parameter. It uses a
        randomly generated key to encrypt the text message using the
        hill cipher approach. The text, the encrpyted text and the
        generated key are returned one string. Note: If the text length
        is not dividable through 3, then additional randomly generated
        letters are added to the text.'''
        input_text = text
        text = text.upper().replace(' ', '')
        addition = 0
        # Add random numbers to the text end if len % 3 not equal 0
        while True:
            if len(text) % self.key_m_size == 0:
                break
            addition += 1
            text += self.inv_arith_abc[random.randint(0, 26)]
        # Convert text letters to numbers
        arith_text = []
        for char in text:
            arith_text.append(self.arith_abc[char])
        #  Split text into 3x1 matrices
        np_text_matrices = []
        for num in range(len(arith_text)):
            if num % self.key_m_size == 0:
                np_text_matrices.append(np.matrix(arith_text[
                    num:num+self.key_m_size]))
        # Generate a random key matrix
        while True:
            np_key_matrix = np.random.randint(self.key_m_size**2,
                                              size=(self.key_m_size,
                                                    self.key_m_size))
            det = np.linalg.det(np_key_matrix) % 26
            det = int(round(det, 0))
            if det != 0 and det % 2 != 0 and det % 13 != 0:
                break
        # Encrypt the text by matrix multiplication with the key
        output = []
        en_text_matrices = np.dot(np_text_matrices, np_key_matrix) % 26
        for m_item in np.nditer(en_text_matrices):
            output.append(self.inv_arith_abc[int(round(m_item.item(0), 0))])
        # Convert the number key to a letter key
        letter_key = []
        for m_item in np.nditer(np_key_matrix):
            letter_key.append(self.inv_arith_abc[
                int(round(m_item.item(0), 0))])
        return self.encrypt_format_output(input_text, output, letter_key)

    def decrypt(self, text, key):
        '''This decrypt method take a text to decipher and a 9 letter
        long key. It returns a string with the original test and the
        deciphered message using the Hill chipher approach.'''
        text = text.upper().replace(' ', '')
        key = key.upper().replace(' ', '')
        addition = 0
        while True:
            if len(text) % self.key_m_size == 0:
                break
            addition += 1
            text += '-'
        # Convert text letters to numbers
        arith_text = []
        for char in text:
            arith_text.append(self.arith_abc[char])
        # Convert key letters to numbers
        arith_key = []
        for char in key:
            arith_key.append(self.arith_abc[char])
        # Split text into a 3x3 matrices
        np_text_matrices = []
        for num in range(len(arith_text)):
            if num % self.key_m_size == 0:
                np_text_matrices.append(np.matrix(
                    arith_text[num:num+self.key_m_size]))
        # Split key into a 3x3 matrices
        np_key_matrix = np.matrix(arith_key)
        np_key_matrix.resize((self.key_m_size, self.key_m_size))
        # Modular multiplicative inverse of key matrix
        # Find determinant of key
        det_of_key_matrix = np.linalg.det(np_key_matrix)
        mod_of_det_key = det_of_key_matrix % 26
        # Get the multiplicate inverse of the key matrix
        mulinv_of_det_key = self.mulinv(int(round(
            mod_of_det_key.item(0), 0)), 26)
        # Transpose key
        transp_key = np_key_matrix.getT()
        # Find minor of key matrix
        minor_of_matrix_key = self.minor(transp_key)
        # Find co-factor with the adjacent sign key matrix
        cofactor_adj_sign_minor = self.adj_sign(minor_of_matrix_key)
        # Multiplicate the key matrix with the cofactor
        key_inverse_mul_co = mulinv_of_det_key * np.round(
            cofactor_adj_sign_minor, 0)
        # Calculate the modulo to have the inverse key ready
        np_key_inverse = np.round(key_inverse_mul_co % 26, 0)
        # Decrypt the text matrices
        en_text_matrices = np.dot(np_text_matrices, np_key_inverse) % 26
        output = []
        for nu in np.nditer(en_text_matrices):
            output.append(self.inv_arith_abc[int(round(nu.item(0), 0))])
        return self.decrypt_format_output(text, output)


'''
# Test
hi = Hill()
# print('encrypted: ', hi.encrypt('ATTATTSESDFA'))
# print('decrypted: ', hi.decrypt('DKWDK WKOSY IB'))
text = 'ATTACK'
#print('text: ', text)
encrypted_text, key = hi.encrypt(text)
print('encrypted_text: ', encrypted_text)
print('key: ', key)
decrypted_text = hi.decrypt(encrypted_text, key)
print('decrypted_text: ', decrypted_text)
'''

checker = pep8.Checker('hill.py')
checker.check_all()
