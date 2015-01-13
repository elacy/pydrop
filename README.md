#PyDrop
A KISS submission system written in python for use with wsgi.

###Requirements
 * Python (I used 2.6)
 * Some httpd (I used apache)
 * WSGI (I used mod_wsgi for apache)
 * PyCrypto - https://www.dlitz.net/software/pycrypto/
 * python-gnupg - http://code.google.com/p/python-gnupg/

###How it works
WSGI calls the application function in pydrop.wsgi passing the environ variable et al whenever a 
http request is made. When the a file is uploaded PyDrop generates a random 32 byte key and a 
random 16 byte IV, creates a drop location, encrypts the key and IV using a GPG public key and 
saves the encrypted data to the drop location. Finally it streams the uploaded file and encrypts 
it chunk by chunk encrypt using AES_CBC_256 writing each chunk to the drop location.

When you wish to decrypt the submission you simply use gpg to decrypt the file using your private 
key which can be on a different computer and then use decrypt.py and the decrypted key + IV to 
decrypt the submission

###How to install
Create a directory to run your app from, create drop and a gnupg directory underneath that.
Place pydrop.wsgi at the directory root and point wsgi at that file.
init gnupg in the gnupg folder and add your public key to it.
Edit pydrop.wsgi to have the correct basePath and gpgFingerprint

###How to decrypt
from a drop directory take the key file, and decrypt it using gpg, take the output from that
and use decrypt.py to decrypt the file input within the drop directory.
