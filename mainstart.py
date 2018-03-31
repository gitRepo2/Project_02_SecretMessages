import os
import pep8
from caesar import Caesar
from keywordcipher import KeywordCipher
from bifid import Bifid
from hill import Hill
from onetimepad import Onetimepad


class UserInteraction():
    def __init__(self, ciphers=None):
        self.available_ciphers = {'caesar': Caesar(),
                                  'keywordcipher': KeywordCipher(),
                                  'bifid': Bifid(),
                                  'hill': Hill()}
        self.one_time_pad = ''
        self.one_time_padded_msg = ''
        self.use_one_time_pad = False
        self.cipher = ''
        self.encrypt = False
        self.decrypt = False
        self.message = ''
        self.key = ''
        self.quit = False

    def print_begining(self):
        '''This method prints a start text in the console for the user.'''
        print('Welcome to my Treehouse Techdegree Secret Messages project.\n')
        print('These are the current available ciphers methods:\n')
        for cipher in self.available_ciphers:
            print('-', cipher)

    def ask_for_encryption_type(self):
        '''This method shows the user the available cipher method and
        asks to enter for the desired cipher to be used.'''
        while True:
            user_input = input('\nWhich cipher would you like to use? ')
            if user_input.lower() == 'quit':
                self.quit = True
                break
            elif user_input.lower() in self.available_ciphers:
                print("\nYou have chosen the '{}' cipher method."
                      .format(user_input))
                print("It's a great cipher.")
                self.cipher = user_input.lower()
                break
            else:
                print('\nThe entered ciphers is not available.')
                print('Please enter one again or write quit.')

    def ask_en_or_decrypt(self):
        '''This method asks the user whether to encrypt or decrypt a
        a text.'''
        while True:
            user_input = input('\nDo you want to encrypt or decrypt? '
                               ).lower()
            if user_input == 'quit':
                self.quit = True
                break
            elif user_input == 'encrypt':
                self.encrypt = True
                break
            elif user_input == 'decrypt':
                self.decrypt = True
                break
            else:
                print('You can only chose between encrypt or decrypt.')

    def ask_for_key(self):
        '''This method asks the user to key in a key.'''
        while True:
            user_input = input('Enter the key you want to use? ')
            if user_input == '':
                print('No input was given. Please try again.')
            else:
                self.key = str(user_input)
                break

    def ask_for_message(self):
        '''This method asks the user to key in a text message.'''
        if self.encrypt:
            en_decrypt = 'encrypt'
        else:
            en_decrypt = 'decrypt'
        while True:
            user_input = input('\nEnter the message you want to {}. '
                               .format(en_decrypt))
            if user_input == '':
                print('No input was given. Please try again')
            else:
                self.message = str(user_input)
                break

    def ask_for_one_time_pad(self):
        '''This method asks the user to input a 'one time pad' code
        to additionaly secure the ciphers.'''
        while True:
            print('\nWould you like to use a one time pad?')
            user_input = input('[y/n]:')
            if user_input.lower() == 'n':
                break
            else:
                self.use_one_time_pad = True
                print('\nPlease enter a one time pad string with letters')
                print('as long or longer as you message. If left blank,')
                print('a new one will be generated for encryption.')
                print("Attention: 'J's are replaced with 'I's.\n")
                user_input = input('Your one time pad: ')
                user_input = user_input.upper().replace(' ', '')
                message = self.message.upper().replace(' ', '')
            if len(user_input) >= len(message) or len(user_input) == 0:
                self.one_time_pad = user_input
                break
            else:
                print('The entered one time pad code is too short.')

    def ask_for_more(self):
        '''This method asks the user to continue or to quit the
        en- or decryption program.'''
        user_input = input('\nDo you want to continue? Y/N ').lower()
        if user_input == 'n':
            self.quit = True
        else:
            self.message = ''
            self.one_time_pad = ''

    def quit_console(self):
        '''This method prints a good bye message to the user.'''
        print('\nYou decided to quit. Have a good day.')

    def clear_screen(self):
        '''This method clears the console screen.'''
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


def running():
    '''This method is running the user interaction.'''
    ui = UserInteraction()
    while True:
        ui.clear_screen()
        ui.print_begining()
        if ui.quit:
            break
        ui.ask_for_encryption_type()
        if ui.quit:
            break
        # ask for encrypt or decrypt
        ui.ask_en_or_decrypt()
        if ui.quit:
            break
        # ask for a one time pad
        ui.ask_for_one_time_pad()
        # ask for the message
        ui.ask_for_message()
        # Generate an object from the selected cipher
        selected_cipher = ui.available_ciphers[ui.cipher]
        # Encrypt message -------------------------------------
        if ui.encrypt:
            if selected_cipher.key_needed_to_encrypt:
                ui.ask_for_key()
            # Additionally cipher the message with a onetimepad
            if ui.use_one_time_pad:
                onetimepad_cipher = Onetimepad()
                ui.message, otp_output = onetimepad_cipher.encrypt(
                    ui.message, ui.one_time_pad)
                print('\nOne time pad outcome:')
                print(otp_output)

            if selected_cipher.key_needed_to_encrypt:
                print("\nYour chosen cipher is the'{}' cipher: ".format(str(
                    selected_cipher.__class__.__name__)))
                encrypted_text, printable_output = selected_cipher.encrypt(
                    ui.message, ui.key)
                print(printable_output)
            else:
                print("\nYour chosen cipher is the'{}' cipher: ".format(str(
                    selected_cipher.__class__.__name__)))
                encrypted_text, printable_output = selected_cipher.encrypt(
                    ui.message)
                print(printable_output)
            ui.encrypt = False
        # Decrypt message -------------------------------------
        if ui.decrypt:
            if selected_cipher.key_needed_to_decrypt:
                ui.ask_for_key()
                print("\nYour chosen cipher is the '{}' cipher: ".format(str(
                    selected_cipher.__class__.__name__)))
                decrypted_text, printable_output = selected_cipher.decrypt(
                    ui.message, ui.key)
                print(printable_output)
            else:
                print("\nYour chosen cipher is the '{}' cipher: ".format(str(
                    selected_cipher.__class__.__name__)))
                decrypted_text, printable_output = selected_cipher.decrypt(
                    ui.message)
                print(printable_output)
            ui.decrypt = False
            # Additionally cipher the message with a onetimepad
            if ui.use_one_time_pad:
                onetimepad_cipher = Onetimepad()
                print('One time pad decrypted:')
                _, printable_output = onetimepad_cipher.decrypt(
                    decrypted_text, ui.one_time_pad)
                print(printable_output)
                print('Be aware that the letter j is always exchanged with i')
                print('and decrypted message might be slightly longer than')
                print('the original message.')
        ui.ask_for_more()
        if ui.quit:
            break
    ui.quit_console()


if __name__ == "__main__":
    running()


checker = pep8.Checker('mainstart.py')
checker.check_all()
