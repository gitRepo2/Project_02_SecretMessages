import pep8


class Cipher:

    def create_blocks(self, text):
        '''This method takes a string or list as input argument text
        and removes any spaces before adding new after every 5. character.
        It returns a string of blocks of five. '''
        text = "".join(text)
        text = text.replace(' ', '')
        text = list(text)
        block_size = 5
        for index in range(len(text)):
            if index % (block_size+1) == block_size:
                text.insert(index, ' ')
        return "".join(text)

    def encrypt_format_output(self, text, encrypted_text, key=0):
        '''This method takes a text, an encrpyted text and if available
        a key. It returns the information in a ready to print format.'''
        encrypted_text = self.create_blocks(encrypted_text)
        output = output = "Text input: {}\nEncrypted text: {}\n".format(
                text, encrypted_text)
        if key:
            key = self.create_blocks(key)
            output = "Text input: {}\nEncrypted text: {}\nKey: {}".format(
                text, encrypted_text, key)
        return output

    def decrypt_format_output(self, text, decrypted_text):
        '''This method takes a text, an decrpyted text. It returns the
        information in a ready to print format.'''
        decrypted_text = self.create_blocks(decrypted_text)
        output = "Encrypted text input: {}\nDecrypted text: {}\n".format(
                text, decrypted_text)
        return output


checker = pep8.Checker('ciphers.py')
checker.check_all()
