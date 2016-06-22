# Added by Neha Ahlawat
# This python wrapper for decryption reads in the file/buffer, 16 bytes at a time, 
# and calls the C function that implements AES decryption.

from aesDecrypt import *
import sys
import subprocess

# This function decrypts an ecnrypted file/buffer
# parameters for decrypt function are encrypted file/buffer name and RSA encrypted AES Key, and 
# it returns the name of decrypted plaintext file. 

def decrypt(arg1, arg2):
    arg1 = arg1+".enc"
    encryptedFile = open(arg2, "rb")
    returnFile = arg2+"DecryptOut.csv"
    keyFile = open(arg1+".dec", "rb")
    decryptedFile = open( returnFile, "wb")

    try:
        encryptedText = bytearray(16)
        encryptedText = encryptedFile.read(16)
        key = keyFile.read(16)
        while encryptedText != '':
            if key == '':
                print ("Key Read Error")
            
            else:
                decryptedText = bytearray(16)
                decryptedText = aesDecrypt(encryptedText, key)
                decryptedFile.write(decryptedText)
                encryptedText = bytearray(16)
                encryptedText = encryptedFile.read(16)
	
    finally:

        keyFile.close()
        encryptedFile.close()
        decryptedFile.close()
    return returnFile;

# Before decrypting the data, this fucntion decrypts the 
# encyrpted AES key using own private key and stores it in a file.

def rsaDecrypt(encryptedKey):
    encryptedKey = encryptedKey+".enc"
    decryptedKey = encryptedKey+".dec"
    args = ['openssl', 'rsautl', '-decrypt', '-inkey', 'private.pem','-in',  encryptedKey, '-out', decryptedKey]
    subprocess.call(args)
    return
