# from https://gist.github.com/sirosen/ec4196fee9779e5de865b0d03f12f0c8
# adding this in repsonse to https://elixirforum.com/t/verifying-blockchain-crypto-signature-elixir-erlang/49226/17?u=legitstack
# so...
# option 1. conform elixir to ravencoin signing (IDEAL https://github.com/lastmeta/Satori/issues/31#issuecomment-1200665236)
# option 2. this, sign differently, the way elixir expects to verify (finish signverify.py)
# option 3. use the python verification on the server. (verify.py)
"""
RSA Sign a Message using a private key
Just turns this example into a script:
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#signing
"""

import sys
import hashlib
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

if len(sys.argv) != 3:
    print('USAGE: sign.py privkey file')
    sys.exit(2)

privkeyfile = sys.argv[1]
messagefile = sys.argv[2]

with open(privkeyfile) as f:
    privkey = serialization.load_pem_private_key(
        f.read(), password=None, backend=default_backend())

with open(messagefile) as m:
    message = m.read()
    prehashed = hashlib.sha256(message).hexdigest()

sig = privkey.sign(
    prehashed,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256())

print(base64.b64encode(sig))

#
# verify.py
"""
RSA Verify a Message against a pubkey
Just turns this example into a script:
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#signing
    
timeit tests reveal that verification takes 0.1ms on a modern CPU
"""

import sys
import hashlib
import base64
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


if len(sys.argv) != 4:
    print('USAGE: verify.py pubkey messagefile sigfile')
    sys.exit(2)

pubkeyfile = sys.argv[1]
messagefile = sys.argv[2]
sigfile = sys.argv[3]

with open(pubkeyfile) as f:
    pubkey = serialization.load_pem_public_key(
        f.read(), backend=default_backend())

with open(messagefile) as m:
    message = m.read()
    prehashed_msg = hashlib.sha256(message).hexdigest()

with open(sigfile) as s:
    sig = s.read()
    decoded_sig = base64.b64decode(sig)


try:
    pubkey.verify(
        decoded_sig,
        prehashed_msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256())
    print('valid!')
    sys.exit(0)
except InvalidSignature:
    print('invalid!')
    sys.exit(1)