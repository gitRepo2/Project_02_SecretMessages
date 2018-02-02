import string
import random
import pep8
from ciphers import Cipher


class Onetimepad(Cipher):
    '''This Onetimepad class takes no argument. It contains method to encrypt
    and decrypt a text with the "one time pad" cipher method.'''
    def __init__(self):
        self.key_needed_to_encrypt = False
        self.key_needed_to_decrypt = True
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.abc_to_num = {char: number for number,
                           char in zip(range(0, len(self.abc)),
                                       self.abc)}
        self.num_to_abc = {v: k for k, v in self.abc_to_num.items()}

    def encrypt(self, text):
        '''This method takes a text (string) as input argument and returns an encrypted
        text with a key (one time pad) in blocks of 5. This code can be used
        to decode the encrypted text. '''
        text = text.upper().replace(' ', '')

        #  Generated random keyword
        num_keyword = []
        for index in range(len(text)):
            num_keyword.append(random.randint(0, len(self.abc)-1))

        keyword = []
        for num in num_keyword:
            keyword.append(self.num_to_abc[num])

        num_text = []
        for char in text:
            num_text.append(self.abc_to_num[char])

        encrypted_text = []
        for num_in_text, num_in_key in zip(num_text, num_keyword):
            encrypted_text.append(self.num_to_abc[((
                num_in_text+num_in_key) % 26)])

        return self.encrypt_format_output(text, encrypted_text, keyword)

    def decrypt(self, text, keyword):
        '''This method take a encrypted text (string) and a keyword (string)
        as input argument and decrypts the text with the keyword.'''
        text = text.upper().replace(' ', '')
        keyword = keyword.upper().replace(' ', '')

        num_keyword = []
        for char in keyword:
            num_keyword.append(self.abc_to_num[char])

        num_text = []
        for char in text:
            num_text.append(self.abc_to_num[char])

        decrypted_text = []
        for num_in_text, num_in_key in zip(num_text, num_keyword):
            decrypted_text.append(self.num_to_abc[((
                num_in_text-num_in_key) % 26)])

        return self.decrypt_format_output(text, decrypted_text)

'''
otp = Onetimepad()
text = 'KNOWLEDGEISPOWER'
encrypted_text, key = otp.encrypt(text)
print('encrypted_text: ', encrypted_text, ' key: ', key)
decrypted_text = otp.decrypt(encrypted_text, key)
print('decrypted_text: ', decrypted_text)
'''

checker = pep8.Checker('onetimepad.py')
checker.check_all()
