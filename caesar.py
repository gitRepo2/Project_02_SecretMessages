import string
from ciphers import Cipher
import pep8


class Caesar(Cipher):
    FORWARD = string.ascii_uppercase * 3

    def __init__(self, offset=3):
        self.offset = offset
        self.FORWARD = string.ascii_uppercase + string.ascii_uppercase[
            :self.offset+1]
        self.BACKWARD = string.ascii_uppercase[
            :self.offset+1] + string.ascii_uppercase
        self.key_needed_to_encrypt = False
        self.key_needed_to_decrypt = False

    def encrypt(self, text):
        '''This method takes a text as input parameter and returns
        a the input text, a encrypted text and a key=None using the
        Caesar cipher approach.'''
        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.FORWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.FORWARD[index+self.offset])
        return self.encrypt_format_output(text, output, key=None)

    def decrypt(self, text):
        '''This method takes a text as input parameter and returns
        the this text, a decrypted text using the Caesar cipher
        approach.'''
        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.BACKWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.BACKWARD[index-self.offset])
        return self.decrypt_format_output(text, output)


checker = pep8.Checker('caesar.py')
checker.check_all()
