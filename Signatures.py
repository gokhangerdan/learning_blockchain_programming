# modules for generate keys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

# modules for sign
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# modules for verify
from cryptography.exceptions import InvalidSignature


def generate_keys():
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public = private.public_key()
    return private, public


def sign(message, private):
    message = bytes(message, 'utf-8')
    sig = private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig


def verify(message, sig, public):
    message = bytes(message, 'utf-8')
    try:
        public.verify(
            sig,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    pr, pu = generate_keys()
    print(pr)
    print(pu)
    message = "This is a secret message"
    sig = sign(message, pr)
    print(sig)
    correct = verify(message, sig, pu)

    if correct:
        print("Success! Good sig")
    else:
        print("ERROR! Signature is bad")

    pr2, pu2 = generate_keys()

    sig2 = sign(message, pr2)

    correct = verify(message, sig2, pu)

    if correct:
        print("ERROR! Bad signature checks out!")
    else:
        print("Success! Bad sig detected")

    badmess = message + "Q"

    correct = verify(badmess, sig, pu)

    if correct:
        print("ERROR! Tampered message checks out!")
    else:
        print("Success! Tampering detected")
