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
                                  'hill': Hill(),
                                  'onetimepad': Onetimepad()}
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
                print('You can only chose between engrypt or decrypt.')

    def ask_for_key(self):
        '''This method asks the user to key in a key.'''
        while True:
            user_input = input('\nEnter the key you want to use? ')
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
            user_input = input('\nEnter the message you want to {}? '
                               .format(en_decrypt))
            if user_input == '':
                print('No input was given. Please try again')
            else:
                self.message = str(user_input)
                break

    def ask_for_more(self):
        '''This method asks the user to continue or to quit the
        en- or decryption program.'''
        user_input = input('\nDo you want to continue? Y/N ').lower()
        if user_input == 'n':
            self.quit = True

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
        ui.ask_en_or_decrypt()
        if ui.quit:
            break
        ui.ask_for_message()
        # Generate an object from the selected cipher
        selected_cipher = ui.available_ciphers[ui.cipher]
        # Encrypt message
        if ui.encrypt:
            if selected_cipher.key_needed_to_encrypt:
                ui.ask_for_key()
                print(selected_cipher.encrypt(ui.message, ui.key))
            else:
                print(selected_cipher.encrypt(ui.message))
            ui.encrypt = False
        # Decrypt message
        if ui.decrypt:
            if selected_cipher.key_needed_to_decrypt:
                ui.ask_for_key()
                print(selected_cipher.decrypt(ui.message, ui.key))
            else:
                print(selected_cipher.decrypt(ui.message))
            ui.decrypt = False
        ui.ask_for_more()
        if ui.quit:
            break
    ui.quit_console()


if __name__ == "__main__":
    running()


checker = pep8.Checker('mainstart.py')
checker.check_all()
