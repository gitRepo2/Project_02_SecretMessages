import string
import pep8
from ciphers import Cipher


class KeywordCipher(Cipher):
    def __init__(self):
        self.key_needed_to_encrypt = True
        self.key_needed_to_decrypt = True
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def encrypt(self, text, keyword):
        '''This method takes a text and a keyword as an input argument
        and returns an encrpyted text using the keyword cipher
        approach. The encrypted text is returned as one block of capital
        letters . E.g. 'ENCRY PTEDT EXT'.'''
        output = []
        text = text.upper().replace(' ', '')
        keyword = keyword.upper()

        encoded_abc = list(self.abc)
        for index in range(len(keyword)):
            encoded_abc.remove(keyword[::-1][index])
            encoded_abc.insert(0, keyword[::-1][index])

        encode_dict = {char: letter for letter,
                       char in zip(encoded_abc, self.abc)}
        for char in text:
            output.append(encode_dict[char])
        return self.encrypt_format_output(text, output, keyword)

    def decrypt(self, text, keyword):
        '''This method takes a text and a keyword as an input argument
        and returns a decrpyted text using the keyword cipher
        approach. The encrypted text is returned as one block of capital
        letters. E.g. 'DECRY PTEDT EXT'.'''
        output = []
        text = text.upper().replace(' ', '')
        keyword = keyword.upper()

        encoded_abc = list(self.abc)
        for index in range(len(keyword)):
            encoded_abc.remove(keyword[::-1][index])
            encoded_abc.insert(0, keyword[::-1][index])
        decode_dict = {char: letter for letter,
                       char in zip(self.abc, encoded_abc)}
        for char in text:
            output.append(decode_dict[char])
        return self.decrypt_format_output(text, output)

'''
kc = KeywordCipher()
# print('encrypted: ', hi.encrypt('KNOWLEDGE IS POWER))
# print('decrypted: ', hi.decrypt('FNWFNWKCGFXPLLUL'))
text = 'KNOWLEDGEISPOWER'
key = 'kryptos'
if text == kc.decrypt(kc.encrypt(text, key), key):
    print('The en- and decryption worked')
else:
    print('The en- and decryption did NOT work')
print(kc.encrypt(text, key))
print(kc.decrypt(kc.encrypt(text, key), key))
'''
checker = pep8.Checker('keywordcipher.py')
checker.check_all()
