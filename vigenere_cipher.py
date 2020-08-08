"""
File contains implementation of Vigenere Cipher with a slight change
It works also for UPPER CASE letters, special characters and numbers (encoded in a BASE_STRING const)
You can change the BASE_STRING however you want, to get different encoding
but remember to save the BASE_STRING structure you used

"""
import numpy as np
import getopt, sys

BASE_STRING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#1234567890/\.,!@#$%^&*()'
NUM_CHARS = len(BASE_STRING)


def generateVigenereMatrix(baseString):
    """
    Params:
        baseString: string of characters used to generate Vigenere matrix ('alphabet')
        
    Returns a Vigenere matrix according to https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
    but with regard to BASE_STRING structure (either it contains numbers/special chars or not)
    """
    
    numChars = len(baseString)
    
    matrix = np.zeros((numChars, numChars), dtype='U')
    
    for i in range(0, numChars):
        firstPart = baseString[i:]
        remainingChars = baseString[:i]
        row = firstPart+remainingChars
        
        matrix[i] = np.array([char for char in row])     
    return matrix


def encodeVigenere(text, keyword, baseString = BASE_STRING):
    """
    Params:
        text: text to encode
        keyword: keyword used in encoding algorithm (according to https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
        baseString: string of characters used to generate Vigenere matrix
    Returns:
        encryptedText: text encrypted using a keyword 
        or raises Exception - WrongKeywordLengthException if len(keyword) is < len(text) - encrypting not safe
    """

    if len(keyword) < len(text):
        modLen = int(len(text) / len(keyword))
        keyword = keyword * (modLen + 1)
        #raise Exception('WrongKeywordLengthExecption')

    temp = ''.join([keyword[i] for i in range(0, len(text))])
    text = text
        
    matrix = generateVigenereMatrix(baseString)
        
    encryptedText = ''
    for i in range(0, len(text)):
        index = (np.where(matrix[:, 0] == text[i])[0][0], np.where(matrix[0, :] == temp[i])[0][0])
        encryptedText = encryptedText + (matrix[index[0], index[1]])
            
    return encryptedText


def decodeVigenere(encryptedText, keyword, baseString = BASE_STRING):
    """
    Params:
        encryptedText: text encoded using Vigenere cipher
        keyword: keyword that was used during encoding
        baseString: string of characters used to generate Vigenere matrix
    Returns:
        decryptedText: decoded text (original text used in encoding)
    """

    if len(keyword) < len(encryptedText):
        modLen = int(len(encryptedText) / len(keyword))
        keyword = keyword * (modLen + 1)

    decryptedText = ''
    for i in range(0, len(encryptedText)):
        valText = np.where(np.array(list(baseString)) == encryptedText[i])[0][0]
        valKeyword = np.where(np.array(list(baseString)) == keyword[i])[0][0]
    
        valDecrypted = valText - valKeyword
        decryptedText = decryptedText + (list(baseString)[valDecrypted])
    
    return decryptedText


def hardToCrackPasswordGenerator(base, keyword, baseString = BASE_STRING, length=10):
    import random
    shuffledBase = ''.join(random.sample(base, len(base)))
    shuffledKeyword = ''.join(random.sample(keyword, len(keyword)))
    
    return ''.join(random.sample(encodeVigenere(shuffledBase, shuffledKeyword, baseString), length))


def main():

    HELP_MSG = """Hello! This is an implementation of Vigenere Cipher in python. \ncmd args:
    -h : help
    -e : encode any given string, you must provide a string to encode along with a keyword (REMEMBER THE KEYWORD!);
    -d : decode any given string using keyword (THE SAME ONE YOU HAD TO REMEMBER), you must provide string to decode and a keyword;
    -g : password generator, you must provide a base string and a keyword -> the two will be shuffled and Vigenere cipher will be apllied, additionally you can provide a length of password;

    When len(keyword) < len(text) the keyword is multiplcated. No need to remember the multiplcated case. The program takes care of it - remember only base keyword.
    
    encode example:             decode example:             password generator example:
    -e BASEWORD KEYWORD         -d ENCODED KEYWORD          -g BASEWORD KEYWORD LENGTH (optional)
      """

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:e:g:", ["help", "decode", "encode", "generate"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, arg in opts:
        if o == "-h" or o == '':
            print(HELP_MSG)

        elif o == "-d":
            if len(args) != 1:
                print("Wrong number of arguments (too many or too few).\nExiting.")
                sys.exit(2)
            else:
                encoded = arg
                keyword = args[0]

            decoded = decodeVigenere(encoded, keyword)
            print(f'Decoded text: {decoded}')

        elif o == "-e":
            if len(args) != 1:
                print("Wrong number of arguments (too many or too few).\nExiting.")
                sys.exit(2)
            else:
                base = arg
                keyword = args[0]

            encoded = encodeVigenere(base, keyword)
            print(f'Encoded text: {encoded}')




        elif o == "-g":
            generatorArgs = [arg]
            for a in args:
                generatorArgs.append(a)

            if len(generatorArgs) < 2 or len(generatorArgs) > 3:
                print("You didn't provide the correct amount of arguments.")
                sys.exit(2)

            elif len(generatorArgs) == 2:
                print("You provided 2 arguments: base and keyword. \nLet's check if they're correct.")

                if len(generatorArgs[0]) > len(generatorArgs[1]):
                    print("Wrong BASE WORD length.")
                    sys.exit(2)
                else:
                    base = generatorArgs[0]
                    keyword = generatorArgs[1]
                    password = hardToCrackPasswordGenerator(base, keyword)

                    print(f'Password generated successfully.\nYou password: {password}')

            else:
                print("You provided 3 arguments. The last one should be integer - length of password. Let me chceck...")

                try:
                    length = int(generatorArgs[2])
                    print("Length argument correct.")
                except Exception as e:
                    print(e)
                    print("Wrong length. Assuming default length - 10")
                    length = 10

                base = generatorArgs[0]
                keyword = generatorArgs[1]
                password = hardToCrackPasswordGenerator(base, keyword, length=length)

                print(f'Password generated successfully.\nYou password: {password}')

if __name__ == "__main__":
    main()





