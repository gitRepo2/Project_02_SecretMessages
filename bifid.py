from ciphers import Cipher
import pep8


class Bifid(Cipher):
    def __init__(self):
        self.key_needed_to_encrypt = False
        self.key_needed_to_decrypt = False
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        abc_index = 0
        self.tableau = {}
        for x in range(0, 6):
            for y in range(0, 6):
                self.tableau.update({self.abc[abc_index]: (x, y)})
                abc_index += 1
        self.inv_tableau = {v: k for k, v in self.tableau.items()}

    def encrypt(self, text):
        '''This method takes a text as a input argument and returns a biphid
        cipher encrypted string back. The encrypted text is return in blocks
        of 5 characters characters divided by a space.E.g. 'CDXSA FHXMU'. '''
        text = text.upper().replace(' ', '')
        output = []
        coordinates_begin = []
        coordinates_end = []
        # Convert text into its coordinates
        for char in text:
            try:
                coordinates_begin.append(self.tableau[char][0])
                coordinates_end.append(self.tableau[char][1])
            except ValueError:
                output.append(char)
        coordinates = coordinates_begin + coordinates_end
        # Read out in rows
        for cor_index in range(0, len(coordinates), 2):
            output.append(self.inv_tableau[coordinates[cor_index],
                                           coordinates[cor_index+1]])
        return self.encrypt_format_output(text, output, key=None)

    def decrypt(self, text):
        '''This method takes a text as a input argument and returns a biphid
        cipher decrypted string back. The encrypted text is return as one block
        of capital letters. E.g. 'DECRYPTEDTEXT'. '''
        output = []
        text = text.upper().replace(' ', '')
        coordinates = []
        # Get coordinates
        for char in text:
            try:
                coordinates.append(self.tableau[char][0])
                coordinates.append(self.tableau[char][1])
            except ValueError:
                output.append(char)
        coordinates_begin = coordinates[:int(len(coordinates)/2)]
        coordinates_end = coordinates[int(len(coordinates)/2):]
        output = []
        # Read out in rows
        for cor_index in range(0, len(coordinates_begin)):
            output.append(self.inv_tableau[coordinates_begin[cor_index],
                                           coordinates_end[cor_index]])
        return self.decrypt_format_output(text, output)

'''
#  test
bi = Bifid()
print(bi.encrypt('68E2AA3'))
print(bi.decrypt('98901 0X'))
# print(help(bi.decrypt))
'''
checker = pep8.Checker('bifid.py')
checker.check_all()
