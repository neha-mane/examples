from sa.secalgoB import keygen, encrypt, decrypt, sign, verify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hmac import HMAC

# Sources:
# [1] - "The Double Ratchet Algorithm", Trevor Perrin, Moxie Marlinspike.
#       https://signal.org/docs/specifications/doubleratchet/
#       Revision 1.0, 11/20/2016

# The maximum number of message keys that can be skipped in a single chain.
# It should be set high enough to tolerate routine lost or delayed messages,
# but low enough that a malicious sender can't trigger excessive recipient
# computation. [1], p. 18
MAX_SKIP = 100


# State class defines an object containing the state variables that must be
# tracked by each party to the double ratchet protocol. [1], p. 19
class state():
    def __init__(self):
        state.DHs = None # DH Ratchet key pair (the "sending" or "self" ratchet key)
        state.DHr = None # DH Ratchet public key (the "received" or "remote" key)
        state.RK = None  # 32-byte Root Key
        state.CKs = None # 32-byte Chain Key for sending 
        state.CKr = None # 32-byte Chain Key for receiving
        state.Ns = None  # Message number for sending
        state.Nr = None  # Message number for receiving
        state.PN = None  # Number of messages in previous sending chain
        # Dictionary of skipped-over message keys, indexed by ratchet public
        # key and message number. Raises an exception if too many elements are
        # stored.
        state.MKSKIPPED = None
    #end def __init()__
#end class state

# Header class defines objects returned by the HEADER function, implemented
# below, and contains fields for the ratchet public key, "dh", the length
# of the previous sending chain, "pn", and the message number of this sent
# message for which this is the header, "n". [1], p. 18-19
class Header():
    def __init__(self, dh_pair, pn, n):
        self.dh = dh_pair.public_key().public_bytes() # Ratchet public key
        self.pn = pn # Number of messages in previous sending chain
        self.n = n # Message number for this message
    #end def __init__()

    # This returns a very boring string representation of a header object
    # for debugging purposes. This is not mentioned in [1]. 
    def __str__(self):
        return ('dh: ' + str(self.dh) +
                ', pn: ' + str(self.pn) +
                ', n: ' + str(self.n))
    #end def __str__()
#end class Header()

# External functions: "To instantiate the Double Ratchet requires defining the
# following functions", [1], p. 18. The specification provides function headers
# and descriptions for these functions, but does not include implementation.
# The implementation was done by us based on their security annd cryptographic
# recommendations on p.30 of [1].

# GENERATE_DH(): Returns a new Diffie-Hellman key pair. [1], p. 18
# This function is recommended to generate a key pair based on the Curve25519
# or Curve448 elliptic curves. [1], p. 30.
def GENERATE_DH():
    #keygen('ECC', curve = 'X21599')
    return X25519PrivateKey.generate()
#end def GENERATE_DH()

# DH(dh_pair, dh_pub): Returns the output from the Diffie-Hellman calculation
# between the private key from the DH key pair "dh_pair" and the DH public key
# "dh_pub". If the DH function rejects invalid public keys, then this function
# may raise an exception which terminates processing. [1], p. 18.
# This function is recommended to return the output from the X25519 or X448
# function as defined in RFC 7748. There is no need to check for invalid public
# keys. [1], p. 30.
def DH(dh_pair, dh_pub):
    return dh_pair.exchange(X25519PublicKey.from_public_bytes(dh_pub))
#end def DH()

# KDF_RK(rk, dh_out): Returns a pair (32-byte root key, 32-byte chain key) as
# the output of applying a KDF keyed by a 32-byte root key "rk", to a
# Diffie-Hellman output "dh_out". [1], p. 18.
# This function is recommended to be implemented using HKDF with SHA-256 or
# SHA-512, using "rk" as HKDF "salt", "dh_out" as HKDF "input key material",
# and an application-specific byte sequence as HKDF "info". The "info" value
# should be chosen to be distinct from other uses of HKDF in this
#application. [1], p. 30
def KDF_RK(rk, dh_out):
    kd = HKDF(algorithm = hashes.SHA256(),
              length=64,
              salt = rk,
              info = b'kdf_rk_info',
              backend = default_backend())
    kd_out = kd.derive(dh_out)
    root_key = kd_out[:32]
    chain_key = kd_out[32:]
    return root_key, chain_key
#end def KDF_RK()

# KDF_CK(ck): Returns a pair (32-byte chain key, 32-byte message key) as the
# output of applying a KDF keyed by a 32-byte chain key "ck" to some
# constant. [1], p. 18
# HMAC with SHA-256 or SHA-512 is recommended, using ck as the HMAC key and
# using separate constants as input (e.g. a single byte 0x01 as input to
# produce the message key, and a single byte 0x02 as input to produce the next
# chain key. [1], p. 30
def KDF_CK(ck):
    ck_h = HMAC(ck, hashes.SHA256(), backend = default_backend())
    ck_h.update(b'\1')
    chain_key = ck_h.finalize()
    mk_h = HMAC(ck, hashes.SHA256(), backend = default_backend())
    mk_h.update(b'\2')
    message_key = mk_h.finalize()
    return chain_key, message_key
#end def KDF_CK()

# ENCRYPT(mk, plaintext, associated_data): Returns an AEAD encryption of
# "plaintext" with message key "mk". The "associate_data" is authenticated
# but is not included in the ciphertext. Because each message is key is used
# only once , the AEAD nonce may be handled in several ways: fixed to a
# constant; derived from "mk" alongside an independent AEAD encryption key;
# derived as an additional output from KDF_CK(); or chosen randomly and
# transmitted. [1], p. 18
# This function is recommended to be implemented with an AEAD encryption scheme
# based on either SIV or a composition of CBC with HMAC. These schemes provide
# some misuse-resistance in case a key is mistakenly used multiple times. A
# concrete recommendation based on CBC and HMAC is as follows:
#  -HKDF is used with SHA-256 or SHA 512 to generate 80 bytes of output. The
#   HKDF "salt" is set to a zero-filled byte sequence equal to the hash's
#   output length. HKDF "input key material" is set to "mk". HKDF "info" is
#   set to an application-specific byte sequence distinct from other uses of
#   HKDF in the application.
#  -The HKDF output is divided into a 32-byte encryption key, a 32-byte
#   authentication key, and a 16-byte IV.
#  -The plaintext is encrypted used AES-256 in CBC mode with PCKS#7 padding,
#   using the encryption key and IV from the previous step.
#  -HMAC is calculated using the authentication key and the same hash function
#   as above. The HMAC input is the "associated_data" prepended to the
#   ciphertext. The HMAC output is appended to the ciphertext.
# [1], p. 30
def ENCRYPT(mk, plaintext, associated_data):
    kd = HKDF(algorithm = hashes.SHA256(),
              length = 80,
              salt = (b'\0' * 32),
              info = b'kdf_encrypt_info',
              backend = default_backend())
    kd_out = kd.derive(mk)
    enc_key = keygen('shared', key_mat = kd_out[:32])
    auth_key = keygen('mac', key_mat = kd_out[32:64])
    kd_iv = kd_out[64:]
    ct = encrypt(plaintext, key = enc_key, iv = kd_iv)
    data, mac = sign(associated_data + ct, key = auth_key)
    return ct + mac
#end def ENCRYPT()

# DECRYPT(mk, ciphertext, associated_data): Returns the AEAD decryption of
# "ciphertext" with message key "mk". If authentication fails, as exception
# will be raised that terminates processing.
def DECRYPT(mk, ciphertext, associated_data):
    kd = HKDF(algorithm = hashes.SHA256(),
              length = 80,
              salt = (b'\0' * 32),
              info = b'kdf_encrypt_info',
              backend = default_backend())
    kd_out = kd.derive(mk)
    
    enc_key = keygen('shared', key_mat = kd_out[:32])
    auth_key = keygen('mac', key_mat = kd_out[32:64])
    kd_iv = kd_out[64:]
    ct_iv = ciphertext[:16]
    ct_mac = ciphertext[-32:]
    ct = ciphertext[:-32]
    assert kd_iv == ct_iv
    verdict = verify((b'\0' + associated_data + ct, ct_mac), key = auth_key)
    if verdict != None:
        return decrypt(ct, key = enc_key)
    else:
        raise Exception()
#end def DECRYPT()

# HEADER(dh_pair, pn, n): Creates a new message header containing the DH
# ratchet public key from the key pair in "dh_pair", the previous chain length
# "pn", and the message number n. The returned header object contains ratchet
# public key "dh", and integers "pn" and "n". [1], p. 18
def HEADER(dh_pair, pn, n):
    return Header(dh_pair, pn, n)
#end def HEADER()

# CONCAT(ad, header): Encodes a message header into a parseable byte sequence,
# prepends the "ad" byte sequence, and returns the result. If "ad" is not
# guaranteed to be a parsable byte sequence, a length value should be prepended
# to the output to ensure that the output is parseable as a unique pair
# ("ad", "header"). [1], p. 18
def CONCAT(ad, header):
    pubk_as_bytes = header.dh
    # CMK: fixing the max value for pn and n as 65535 bytes
    pn_as_bytes = header.pn.to_bytes(2, byteorder = 'big')
    n_as_bytes = header.n.to_bytes(2, byteorder = 'big')
    ad_length = len(ad)
    # CMK: same for length of ad
    ad_length_as_bytes = ad_length.to_bytes(2, byteorder = 'big')
    return ad + pubk_as_bytes + pn_as_bytes + n_as_bytes
#end def CONCAT()

# End External Functions
