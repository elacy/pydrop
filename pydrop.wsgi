html = """
<html><body>
<form enctype="multipart/form-data" method="post">
<p>File: <input type="file" name="file"></p>
<p>File: <input type="file" name="file"></p>
<p><input type="submit" value="Upload"></p>
</form>
</body>
</html>"""
def application(environ, start_response):
        gpgFingerprint = '96A3CD408389940947328DF682EE54E94497643D'
        basePath = '/path/to/pydrop'
        if environ.get('REQUEST_METHOD') == 'POST':
                content_length = int(environ.get('CONTENT_LENGTH', 0))
                chunksize = 65536
                if content_length != 0:
                        dropInput(environ['wsgi.input'],content_length,basePath, gpgFingerprint)

        status = '200 OK'

        response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(html)))]
        start_response(status, response_headers)

        return [html]

class Key:
        def __init__(self):
                import os
                self.key = os.urandom(32)
                self.IV = os.urandom(16)

def dropInput(input,inputLength,basePath,gpgFingerprint):
        dropDir = createDropDir(basePath + '/drop')
        key = Key()

        gpgEncryptKey(basePath,gpgFingerprint,dropDir,key)

        crypt = initCipher(key)
        chunksize = 65536
        BLOCK_SIZE = 32
        f = open(dropDir + '/input','w')
        PADDING = '{'
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        while 1:
                remain = inputLength - f.tell()
                if remain <= 0: break
                chunk = input.read(min(chunksize, remain))
                if  not chunk: break
                f.write(crypt.encrypt(pad(chunk)))
        f.close()

def createDropDir(basePath):
        import os
        while 1:
                rand = basePath +'/' + randomKey(10)
                if not os.path.exists(rand):
                        os.makedirs(rand)
                        return rand

def randomKey(size):
        import random
        import string
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(size))

def initCipher(key):
        from Crypto.Cipher import AES
        return AES.new(key.key, AES.MODE_CBC,key.IV)

def gpgEncryptKey(basePath,fingerprint,dropDir,key):
        import gnupg
        gpg = gnupg.GPG(gnupghome=basePath +'/gnupg')
        file = gnupg._make_binary_stream(key.key + key.IV, gpg.encoding)
        return gpg.encrypt_file(file, fingerprint,always_trust=1, output=dropDir+'/key').data