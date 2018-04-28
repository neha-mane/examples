# -*- generated by 1.0.12 -*-
import da
PatternExpr_1407 = da.pat.TuplePattern([da.pat.FreePattern('msg'), da.pat.BoundPattern('_BoundPattern1410_'), da.pat.FreePattern('counter')])
PatternExpr_1415 = da.pat.FreePattern('server')
PatternExpr_2201 = da.pat.TuplePattern([da.pat.TuplePattern([da.pat.ConstantPattern(22), da.pat.BoundPattern('_BoundPattern2204_'), da.pat.ConstantPattern(None), da.pat.FreePattern('cipher_fragment')]), da.pat.FreePattern('handshake_id'), da.pat.FreePattern('counter')])
PatternExpr_2216 = da.pat.FreePattern('client')
PatternExpr_2456 = da.pat.TuplePattern([da.pat.FreePattern('msg'), da.pat.BoundPattern('_BoundPattern2459_'), da.pat.FreePattern('counter')])
PatternExpr_2463 = da.pat.FreePattern('client')
PatternExpr_2809 = da.pat.TuplePattern([da.pat.TuplePattern([da.pat.ConstantPattern(20), da.pat.BoundPattern('_BoundPattern2812_'), da.pat.ConstantPattern(None), da.pat.FreePattern('cipher_fragment')]), da.pat.FreePattern('handshake_id'), da.pat.FreePattern('msg_counter')])
_config_object = {}
import time, sys, pickle
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC
from sa.secalgo import *
configure(verify_returns='bool')
PROTOCOL_VERSION_3_0 = (3, 0)
PROTOCOL_VERSION_1_0 = (3, 1)
PROTOCOL_VERSION_1_1 = (3, 2)
PROTOCOL_VERSION_1_2 = (3, 3)
TYPE_CHANGE_CIPHER_SPEC = 20
TYPE_ALERT = 21
TYPE_HANDSHAKE = 22
TYPE_APPLICATION_DATA = 23
VERIFY_DATA_LENGTH = 12
CHANGE_CIPHER_SPEC_BODY = 1
HELLO_REQUEST = 0
CLIENT_HELLO = 1
SERVER_HELLO = 2
CERTIFICATE = 11
SERVER_KEY_EXCHANGE = 12
CERTIFICATE_REQUEST = 13
SERVER_HELLO_DONE = 14
CERTIFICATE_VERIFY = 15
CLIENT_KEY_EXCHANGE = 16
FINISHED = 20
RSA_SIGN = 1
DSS_SIGN = 2
RSA_FIXED_DH = 3
DSS_FIXED_DH = 4
RSA_EPHEMERAL_DH_RESERVED = 5
DSS_EPHEMERAL_DH_RESERVED = 6
FORTEZZA_DMS_RESERVED = 20
CONN_SERVER = 0
CONN_CLIENT = 1
TLS_PRF_SHA256 = 0
CIPHER_STREAM = 0
CIPHER_BLOCK = 1
CIPHER_AEAD = 2
BULK_NULL = 0
BULK_RC4 = 1
BULK_3DES = 2
BULK_AES = 3
MAC_NULL = 0
MAC_HMAC_MD5 = 1
MAC_HMAC_SHA1 = 2
MAC_HMAC_SHA256 = 3
MAC_HMAC_SHA384 = 4
MAC_HMAC_SHA512 = 5
COMP_NULL = 0
TLS_NULL_WITH_NULL_NULL = (0, 0)
TLS_RSA_WITH_AES_128_CBC_SHA256 = (0, 60)
TLS_RSA_WITH_AES_256_CBC_SHA256 = (0, 61)
SIG_ANONYMOUS = 0
SIG_RSA = 1
SIG_DSA = 2
SIG_ECDSA = 3
HASH_NONE = 0
HASH_MD5 = 1
HASH_SHA1 = 2
HASH_SHA224 = 3
HASH_SHA256 = 4
HASH_SHA384 = 5
HASH_SHA512 = 6
KE_NULL = 0
KE_RSA = 1
KE_DH_DSS = 2
KE_DH_RSA = 3
KE_DHE_DSS = 4
KE_DHE_DSS = 5
KE_DH_ANON = 6

def _a(n, secret, seed):
    if (n == 0):
        return seed
    else:
        h = HMAC.new(secret, digestmod=SHA256)
        h.update(_a((n - 1), secret, seed))
        return h.digest()

def _p_hash(secret, seed, output_length):
    result = bytearray()
    i = 1
    while (len(result) < output_length):
        h = HMAC.new(secret, digestmod=SHA256)
        h.update(_a(i, secret, seed))
        h.update(seed)
        result.extend(h.digest())
        i += 1
    return bytes(result[:output_length])

def tls_prf_sha256(secret, label, seed, output_length):
    return _p_hash(secret, (label + seed), output_length)

class Security_Parameters():

    def __init__(self, ce):
        self.connection_end = ce
        self.prf_algorithm = TLS_PRF_SHA256
        self.bulk_cipher_algorithm = BULK_NULL
        self.cipher_type = CIPHER_STREAM
        self.enc_key_length = 0
        self.block_length = None
        self.fixed_iv_length = 0
        self.record_iv_length = 0
        self.mac_algorithm = MAC_NULL
        self.mac_length = 0
        self.mac_key_length = 0
        self.compression_method = COMP_NULL
        self.master_secret = None
        self.client_random = None
        self.server_random = None

class Connection_State():

    def __init__(self):
        self.compression_state = None
        self.cipher_state = None
        self.mac_key = None
        self.sequence_number = 0

class TLS_Peer(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._TLS_PeerReceivedEvent_0 = []
        self._TLS_PeerReceivedEvent_2 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_0', PatternExpr_1407, sources=[PatternExpr_1415], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_1', PatternExpr_2201, sources=[PatternExpr_2216], destinations=None, timestamps=None, record_history=None, handlers=[self._TLS_Peer_handler_2200]), da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_2', PatternExpr_2456, sources=[PatternExpr_2463], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_3', PatternExpr_2809, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._TLS_Peer_handler_2808])])

    def setup(self, ce, peer, secret_key, public_key, certificate_list, **rest_2945):
        super().setup(ce=ce, peer=peer, secret_key=secret_key, public_key=public_key, certificate_list=certificate_list, **rest_2945)
        self._state.ce = ce
        self._state.peer = peer
        self._state.secret_key = secret_key
        self._state.public_key = public_key
        self._state.certificate_list = certificate_list
        self._state.max_hs_id = 0
        self._state.supported_tls_versions = (PROTOCOL_VERSION_1_2,)
        self._state.supported_cipher_suites = (TLS_RSA_WITH_AES_256_CBC_SHA256,)
        self._state.supported_compression_methods = (COMP_NULL,)
        self._state.current_rsp = Security_Parameters(self._state.ce)
        self._state.current_wsp = Security_Parameters(self._state.ce)
        self._state.pending_rsp = Security_Parameters(self._state.ce)
        self._state.pending_wsp = Security_Parameters(self._state.ce)
        self._state.current_read_state = Connection_State()
        self._state.current_write_state = Connection_State()
        self._state.pending_read_state = Connection_State()
        self._state.pending_write_state = Connection_State()

    def run(self):
        if (not (self._state.peer == None)):
            self.initiate_handshake(self._state.peer)
        else:
            super()._label('_st_label_2853', block=False)
            _st_label_2853 = 0
            while (_st_label_2853 == 0):
                _st_label_2853 += 1
                if False:
                    _st_label_2853 += 1
                else:
                    super()._label('_st_label_2853', block=True)
                    _st_label_2853 -= 1

    def record_wrapper(self, content_type, tls_message):
        version = PROTOCOL_VERSION_1_2
        pt_fragment = tls_message
        pt_length = None
        tls_pt = (content_type, version, pt_length, pt_fragment)
        comp_length = pt_length
        if (not (self._state.current_wsp.compression_method == COMP_NULL)):
            comp_fragment = self._state.current_wsp.compression_method(pt_fragment)
        else:
            comp_fragment = pt_fragment
        tls_comp = (content_type, version, comp_length, comp_fragment)
        cipher_length = comp_length
        if (self._state.current_wsp.cipher_type == CIPHER_STREAM):
            if (self._state.current_wsp.mac_algorithm == MAC_NULL):
                cipher_mac = b''
            else:
                cipher_mac = sign((self._state.current_write_state.sequence_number, content_type, version, comp_length, comp_fragment), key=self._state.current_write_state.mac_key)
            stream_ciphered = (comp_fragment, cipher_mac)
            if (not (self._state.current_wsp.bulk_cipher_algorithm == BULK_NULL)):
                cipher_fragment = encrypt(stream_ciphered, key=self._state.current_write_state.cipher_state[0])
            else:
                cipher_fragment = stream_ciphered
        elif (self._state.current_wsp.cipher_type == CIPHER_BLOCK):
            iv = keygen('random', self._state.current_wsp.record_iv_length)
            if (self._state.current_wsp.mac_algorithm == MAC_NULL):
                cipher_mac = b''
            else:
                cipher_mac = sign((self._state.current_write_state.sequence_number, content_type, version, comp_length, comp_fragment), key=self._state.current_write_state.mac_key)
            cipher_padding = b''
            cipher_pad_length = 0
            block_ciphered = (comp_fragment, cipher_mac, cipher_padding, cipher_pad_length)
            cipher_fragment = (iv, encrypt(block_ciphered, key=self._state.current_write_state.cipher_state[0]))
        tls_cipher = (content_type, version, cipher_length, cipher_fragment)
        return tls_cipher

    def record_unwrapper(self, tls_cipher):
        (content_type, version, cipher_length, cipher_fragment) = tls_cipher
        if (not (version == PROTOCOL_VERSION_1_2)):
            return
        if (self._state.current_rsp.cipher_type == CIPHER_STREAM):
            if (self._state.current_rsp.bulk_cipher_algorithm == BULK_NULL):
                (comp_fragment, cipher_mac) = cipher_fragment
            else:
                (comp_fragment, cipher_mac) = decrypt(cipher_fragment, key=self._state.current_read_state.cipher_state[0])
        elif (self._state.current_rsp.cipher_type == CIPHER_BLOCK):
            (iv, block_ciphered) = cipher_fragment
            (comp_fragment, cipher_mac, cipher_padding, cipher_pad_length) = decrypt(block_ciphered, key=self._state.current_read_state.cipher_state[0])
        comp_length = cipher_length
        if (not (self._state.current_rsp.mac_algorithm == MAC_NULL)):
            if (not verify(((self._state.current_read_state.sequence_number, content_type, version, comp_length, comp_fragment), cipher_mac), key=self._state.current_read_state.mac_key)):
                self.output('MAC VERIFICATION ERROR')
                return
        pt_length = comp_length
        if (not (self._state.current_rsp.compression_method == COMP_NULL)):
            pt_fragment = self._state.current_rsp.compression_method(comp_fragment, 'decompress')
        else:
            pt_fragment = comp_fragment
        return pt_fragment

    def update_pending_parameters(self, cipher_suite, comp_method, crand, srand):
        self._state.pending_rsp.compression_method = comp_method
        self._state.pending_rsp.client_random = crand
        self._state.pending_rsp.server_random = srand
        self._state.pending_wsp.compression_method = comp_method
        self._state.pending_wsp.client_random = crand
        self._state.pending_wsp.server_random = srand
        if (cipher_suite == TLS_RSA_WITH_AES_256_CBC_SHA256):
            self._state.pending_rsp.bulk_cipher_algorithm = BULK_AES
            self._state.pending_rsp.cipher_type = CIPHER_BLOCK
            self._state.pending_rsp.enc_key_length = 32
            self._state.pending_rsp.block_length = 16
            self._state.pending_rsp.fixed_iv_length = 16
            self._state.pending_rsp.record_iv_length = 16
            self._state.pending_rsp.mac_algorithm = MAC_HMAC_SHA256
            self._state.pending_rsp.mac_length = 32
            self._state.pending_rsp.mac_key_length = 32
            self._state.pending_wsp.bulk_cipher_algorithm = BULK_AES
            self._state.pending_wsp.cipher_type = CIPHER_BLOCK
            self._state.pending_wsp.enc_key_length = 32
            self._state.pending_wsp.block_length = 16
            self._state.pending_wsp.fixed_iv_length = 16
            self._state.pending_wsp.record_iv_length = 16
            self._state.pending_wsp.mac_algorithm = MAC_HMAC_SHA256
            self._state.pending_wsp.mac_length = 32
            self._state.pending_wsp.mac_key_length = 32
            return KE_RSA
        return KE_NULL

    def update_connection_state(self):
        key_block_length = (2 * (self._state.pending_wsp.enc_key_length + self._state.pending_wsp.mac_key_length))
        key_block = tls_prf_sha256(self._state.pending_wsp.master_secret, b'key expansion', (self._state.pending_wsp.client_random + self._state.pending_wsp.server_random), key_block_length)
        first_slice = self._state.pending_wsp.mac_key_length
        second_slice = (first_slice + self._state.pending_wsp.mac_key_length)
        third_slice = (second_slice + self._state.pending_wsp.enc_key_length)
        fourth_slice = (third_slice + self._state.pending_wsp.enc_key_length)
        first_block = key_block[:first_slice]
        second_block = key_block[first_slice:second_slice]
        third_block = key_block[second_slice:third_slice]
        fourth_block = key_block[third_slice:]
        if (self._state.pending_wsp.connection_end == CONN_CLIENT):
            self._state.pending_write_state.mac_key = keygen('mac', key_mat=first_block)
            self._state.pending_read_state.mac_key = keygen('mac', key_mat=second_block)
            self._state.pending_write_state.cipher_state = [keygen('shared', key_mat=third_block)]
            self._state.pending_read_state.cipher_state = [keygen('shared', key_mat=fourth_block)]
        else:
            self._state.pending_read_state.mac_key = keygen('mac', key_mat=first_block)
            self._state.pending_write_state.mac_key = keygen('mac', key_mat=second_block)
            self._state.pending_read_state.cipher_state = [keygen('shared', key_mat=third_block)]
            self._state.pending_write_state.cipher_state = [keygen('shared', key_mat=fourth_block)]

    def initiate_handshake(self, server):
        self.output('CLIENT - begin Handshake')
        handshake_id = (self._id, self._state.max_hs_id)
        self._state.max_hs_id += 1
        msg_counter = 0
        handshake_messages = []
        self._state.current_rsp.connection_end = CONN_CLIENT
        self._state.current_wsp.connection_end = CONN_CLIENT
        self._state.pending_rsp.connection_end = CONN_CLIENT
        self._state.pending_wsp.connection_end = CONN_CLIENT
        client_random = (time.time(), keygen('random', 28))
        body_ch = (PROTOCOL_VERSION_1_2, client_random, None, (TLS_RSA_WITH_AES_256_CBC_SHA256,), (0,), None)
        handshake_ch = (CLIENT_HELLO, None, body_ch)
        handshake_messages.append(handshake_ch)
        msg_counter += 1
        self.send((self.record_wrapper(TYPE_HANDSHAKE, handshake_ch), handshake_id, msg_counter), to=server)
        super()._label('_st_label_1404', block=False)
        msg = server = counter = None

        def ExistentialOpExpr_1405():
            nonlocal msg, server, counter
            for (_, (_, _, server), (msg, _BoundPattern1426_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern1426_ == handshake_id):
                    if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_HELLO == self.record_unwrapper(msg)[0])):
                        return True
            return False
        _st_label_1404 = 0
        while (_st_label_1404 == 0):
            _st_label_1404 += 1
            if ExistentialOpExpr_1405():
                _st_label_1404 += 1
            else:
                super()._label('_st_label_1404', block=True)
                _st_label_1404 -= 1
        msg_counter = counter
        handshake_sh = self.record_unwrapper(msg)
        handshake_messages.append(handshake_sh)
        (_, _, body_sh) = handshake_sh
        (server_version, server_random, session_id, cipher_suite, compression_method, extensions) = body_sh
        if (not (server_version == PROTOCOL_VERSION_1_2)):
            return
        key_exchange_alg = self.update_pending_parameters(cipher_suite, compression_method, client_random[1], server_random[1])
        if (not (key_exchange_alg in {KE_NULL, KE_DH_ANON})):
            super()._label('_st_label_1509', block=False)
            msg = server = counter = None

            def ExistentialOpExpr_1510():
                nonlocal msg, server, counter
                for (_, (_, _, server), (msg, _BoundPattern1529_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1529_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (CERTIFICATE == self.record_unwrapper(msg)[0])):
                            return True
                return False
            _st_label_1509 = 0
            while (_st_label_1509 == 0):
                _st_label_1509 += 1
                if ExistentialOpExpr_1510():
                    _st_label_1509 += 1
                else:
                    super()._label('_st_label_1509', block=True)
                    _st_label_1509 -= 1
            msg_counter = counter
            handshake_sc = self.record_unwrapper(msg)
            handshake_messages.append(handshake_sc)
            (_, _, body_cert) = handshake_sc
            (cert_list,) = body_cert
            verdict = True
            for (i, cert) in enumerate(cert_list):
                if (i < (len(cert_list) - 1)):
                    if (not verify(((cert[0], cert[1]), cert[2]), key=cert_list[(i + 1)][1])):
                        verdict = False
                elif (not verify(((cert[0], cert[1]), cert[2]), key=cert[1])):
                    verdict = False
            if (not verdict):
                self.output('CLIENT - CERTIFICATE AUTHENTICATION FAILURE')
                return
            server_public_key = cert_list[0][1]
        if (not (key_exchange_alg in {KE_NULL, KE_RSA, KE_DH_DSS, KE_DH_RSA})):
            super()._label('_st_label_1666', block=False)
            msg = server = counter = None

            def ExistentialOpExpr_1667():
                nonlocal msg, server, counter
                for (_, (_, _, server), (msg, _BoundPattern1686_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1686_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_KEY_EXCHANGE == self.record_unwrapper(msg)[0])):
                            return True
                return False
            _st_label_1666 = 0
            while (_st_label_1666 == 0):
                _st_label_1666 += 1
                if ExistentialOpExpr_1667():
                    _st_label_1666 += 1
                else:
                    super()._label('_st_label_1666', block=True)
                    _st_label_1666 -= 1
            msg_counter = counter
            pass
        if (not (key_exchange_alg in {KE_NULL, KE_DH_ANON})):
            super()._label('_st_label_1717', block=False)
            msg = server = counter = None

            def ExistentialOpExpr_1718():
                nonlocal msg, server, counter
                for (_, (_, _, server), (msg, _BoundPattern1737_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1737_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (CERTIFICATE_REQUEST == self.record_unwrapper(msg)[0])):
                            return True
                return False
            msg = server = counter = None

            def ExistentialOpExpr_1761():
                nonlocal msg, server, counter
                for (_, (_, _, server), (msg, _BoundPattern1780_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1780_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_HELLO_DONE == self.record_unwrapper(msg)[0])):
                            return True
                return False
            _st_label_1717 = 0
            while (_st_label_1717 == 0):
                _st_label_1717 += 1
                if ExistentialOpExpr_1718():
                    msg_counter = counter
                    pass
                    _st_label_1717 += 1
                elif ExistentialOpExpr_1761():
                    pass
                    _st_label_1717 += 1
                else:
                    super()._label('_st_label_1717', block=True)
                    _st_label_1717 -= 1
        super()._label('_st_label_1801', block=False)
        msg = server = counter = None

        def ExistentialOpExpr_1802():
            nonlocal msg, server, counter
            for (_, (_, _, server), (msg, _BoundPattern1821_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern1821_ == handshake_id):
                    if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_HELLO_DONE == self.record_unwrapper(msg)[0])):
                        return True
            return False
        _st_label_1801 = 0
        while (_st_label_1801 == 0):
            _st_label_1801 += 1
            if ExistentialOpExpr_1802():
                _st_label_1801 += 1
            else:
                super()._label('_st_label_1801', block=True)
                _st_label_1801 -= 1
        msg_counter = counter
        handshake_shd = self.record_unwrapper(msg)
        handshake_messages.append(handshake_shd)
        pre_master_secret = (PROTOCOL_VERSION_1_2, keygen('random', 46))
        encrypted_pre_master_secret = (encrypt(pre_master_secret, key=server_public_key),)
        body_cke = (encrypted_pre_master_secret,)
        handshake_cke = (CLIENT_KEY_EXCHANGE, None, body_cke)
        handshake_messages.append(handshake_cke)
        msg_counter += 1
        self.send((self.record_wrapper(TYPE_HANDSHAKE, handshake_cke), handshake_id, msg_counter), to=server)
        pms = (bytes(pre_master_secret[0]) + pre_master_secret[1])
        msecret = tls_prf_sha256(pms, b'master secret', (self._state.pending_wsp.client_random + self._state.pending_wsp.server_random), 48)
        self._state.pending_wsp.master_secret = msecret
        self._state.pending_rsp.master_secret = msecret
        self.update_connection_state()
        handshake_ccs = (CHANGE_CIPHER_SPEC_BODY,)
        msg_counter += 1
        self.send((self.record_wrapper(TYPE_CHANGE_CIPHER_SPEC, handshake_ccs), handshake_id, msg_counter), to=server)
        self._state.current_wsp = self._state.pending_wsp
        self._state.current_write_state = self._state.pending_write_state
        self._state.pending_wsp = Security_Parameters(self._state.current_wsp.connection_end)
        self._state.pending_write_state = Connection_State()
        shm = b''
        m_count = 1
        for m in handshake_messages:
            shm += (b'msg' + str(m_count).encode('ascii'))
            m_count += 1
        print('CLIENT_SHM1:\n', shm)
        verification_data = tls_prf_sha256(self._state.current_wsp.master_secret, b'client finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
        print('CURRENT_WSP_MS:\n', self._state.current_wsp.master_secret)
        print('HASH:', SHA256.new(shm).digest())
        print('CLIENT:\n', verification_data)
        finished = (verification_data,)
        handshake_cfin = (FINISHED, None, finished)
        handshake_messages.append(handshake_cfin)
        shm += (b'msg' + str(m_count).encode('ascii'))
        print('CLIENT_SHM2:\n', shm)
        msg_counter += 1
        self.send((self.record_wrapper(TYPE_HANDSHAKE, handshake_cfin), handshake_id, msg_counter), to=server)
        super()._label('_st_label_2085', block=False)
        msg = server = counter = None

        def ExistentialOpExpr_2086():
            nonlocal msg, server, counter
            for (_, (_, _, server), (msg, _BoundPattern2105_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern2105_ == handshake_id):
                    if ((msg[0] == TYPE_CHANGE_CIPHER_SPEC) and (counter > msg_counter)):
                        return True
            return False
        _st_label_2085 = 0
        while (_st_label_2085 == 0):
            _st_label_2085 += 1
            if ExistentialOpExpr_2086():
                _st_label_2085 += 1
            else:
                super()._label('_st_label_2085', block=True)
                _st_label_2085 -= 1
        msg_counter = counter
        super()._label('_st_label_2121', block=False)
        msg = server = counter = None

        def ExistentialOpExpr_2122():
            nonlocal msg, server, counter
            for (_, (_, _, server), (msg, _BoundPattern2141_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern2141_ == handshake_id):
                    if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (FINISHED == self.record_unwrapper(msg)[0])):
                        return True
            return False
        _st_label_2121 = 0
        while (_st_label_2121 == 0):
            _st_label_2121 += 1
            if ExistentialOpExpr_2122():
                _st_label_2121 += 1
            else:
                super()._label('_st_label_2121', block=True)
                _st_label_2121 -= 1
        msg_counter = counter
        (_, _, (finish_data,)) = self.record_unwrapper(msg)
        client_data = tls_prf_sha256(self._state.current_rsp.master_secret, b'server finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
        if (not (client_data == finish_data)):
            self.output('CLIENT - Handshake Failed')
            return
        self.output('CLIENT - Handshake complete')

    def _TLS_Peer_handler_2200(self, cipher_fragment, handshake_id, counter, client):
        msg_counter = counter
        handshake_messages = []
        handshake_msg = self.record_unwrapper((TYPE_HANDSHAKE, PROTOCOL_VERSION_1_2, None, cipher_fragment))
        if (not (CLIENT_HELLO == handshake_msg[0])):
            return
        self.output('SERVER - begin Handshake')
        self._state.current_rsp.connection_end = CONN_SERVER
        self._state.current_wsp.connection_end = CONN_SERVER
        self._state.pending_rsp.connection_end = CONN_SERVER
        self._state.pending_wsp.connection_end = CONN_SERVER
        handshake_messages.append(handshake_msg)
        (client_version, client_random, session_id, cipher_suites, compression_methods, extensions) = handshake_msg[2]
        server_version = min(client_version, max(self._state.supported_tls_versions))
        server_random = (time.time(), keygen('random', 28))
        if (not (session_id == None)):
            self.output('Client attempting abbreivated handshake.')
        else:
            session_id = None
            cipher_suite = {suite for suite in cipher_suites for _FreePattern2325_ in self._state.supported_cipher_suites if (_FreePattern2325_ == suite)}.pop()
            compression_method = {method for method in compression_methods for _FreePattern2341_ in self._state.supported_compression_methods if (_FreePattern2341_ == method)}.pop()
            body_sh = (server_version, server_random, session_id, cipher_suite, compression_method, extensions)
            handshake_sh = (SERVER_HELLO, None, body_sh)
            handshake_messages.append(handshake_sh)
            msg_counter += 1
            self.send((self.record_wrapper(TYPE_HANDSHAKE, handshake_sh), handshake_id, msg_counter), to=client)
            key_exchange_alg = self.update_pending_parameters(cipher_suite, compression_method, client_random[1], server_random[1])
            body_sc = (self._state.certificate_list,)
            handshake_sc = (CERTIFICATE, None, body_sc)
            handshake_messages.append(handshake_sc)
            msg_counter += 1
            self.send((self.record_wrapper(TYPE_HANDSHAKE, handshake_sc), handshake_id, msg_counter), to=client)
            body_shd = ()
            handshake_shd = (SERVER_HELLO_DONE, None, body_shd)
            handshake_messages.append(handshake_shd)
            msg_counter += 1
            self.send((self.record_wrapper(TYPE_HANDSHAKE, handshake_shd), handshake_id, msg_counter), to=client)
            super()._label('_st_label_2453', block=False)
            client = counter = msg = None

            def ExistentialOpExpr_2454():
                nonlocal client, counter, msg
                for (_, (_, _, client), (msg, _BoundPattern2474_, counter)) in self._TLS_PeerReceivedEvent_2:
                    if (_BoundPattern2474_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (CLIENT_KEY_EXCHANGE == self.record_unwrapper(msg)[0])):
                            return True
                return False
            _st_label_2453 = 0
            while (_st_label_2453 == 0):
                _st_label_2453 += 1
                if ExistentialOpExpr_2454():
                    _st_label_2453 += 1
                else:
                    super()._label('_st_label_2453', block=True)
                    _st_label_2453 -= 1
            msg_counter = counter
            handshake_cke = self.record_unwrapper(msg)
            handshake_messages.append(handshake_cke)
            (_, _, body_cke) = handshake_cke
            pre_master_secret = decrypt(body_cke[0][0], key=self._state.secret_key)
            pms = (bytes(pre_master_secret[0]) + pre_master_secret[1])
            msecret = tls_prf_sha256(pms, b'master secret', (self._state.pending_wsp.client_random + self._state.pending_wsp.server_random), 48)
            self._state.pending_wsp.master_secret = msecret
            self._state.pending_rsp.master_secret = msecret
            self.update_connection_state()
            super()._label('_st_label_2564', block=False)
            client = counter = msg = None

            def ExistentialOpExpr_2565():
                nonlocal client, counter, msg
                for (_, (_, _, client), (msg, _BoundPattern2584_, counter)) in self._TLS_PeerReceivedEvent_2:
                    if (_BoundPattern2584_ == handshake_id):
                        if ((msg[0] == TYPE_CHANGE_CIPHER_SPEC) and (counter > msg_counter)):
                            return True
                return False
            _st_label_2564 = 0
            while (_st_label_2564 == 0):
                _st_label_2564 += 1
                if ExistentialOpExpr_2565():
                    _st_label_2564 += 1
                else:
                    super()._label('_st_label_2564', block=True)
                    _st_label_2564 -= 1
            msg_counter = counter
            super()._label('_st_label_2600', block=False)
            client = counter = msg = None

            def ExistentialOpExpr_2601():
                nonlocal client, counter, msg
                for (_, (_, _, client), (msg, _BoundPattern2620_, counter)) in self._TLS_PeerReceivedEvent_2:
                    if (_BoundPattern2620_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (FINISHED == self.record_unwrapper(msg)[0])):
                            return True
                return False
            _st_label_2600 = 0
            while (_st_label_2600 == 0):
                _st_label_2600 += 1
                if ExistentialOpExpr_2601():
                    _st_label_2600 += 1
                else:
                    super()._label('_st_label_2600', block=True)
                    _st_label_2600 -= 1
            msg_counter = counter
            handshake_cfin = self.record_unwrapper(msg)
            (_, _, (finish_data,)) = handshake_cfin
            shm = b''
            m_count = 1
            for m in handshake_messages:
                shm += (b'msg' + str(m_count).encode('ascii'))
                m_count += 1
            print('SERVER_SHM1:\n', shm)
            server_data = tls_prf_sha256(self._state.current_rsp.master_secret, b'client finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
            if (not (server_data == finish_data)):
                self.output('SERVER - Handshake failed')
                return
            handshake_messages.append(handshake_cfin)
            shm += (b'msg' + str(m_count).encode('ascii'))
            print('SERVER_SHM2:\n', shm)
            handshake_ccs = (CHANGE_CIPHER_SPEC_BODY,)
            msg_counter += 1
            self.send((self.record_wrapper(TYPE_CHANGE_CIPHER_SPEC, handshake_ccs), handshake_id, msg_counter), to=client)
            self._state.current_wsp = self._state.pending_wsp
            self._state.current_write_state = self._state.pending_write_state
            self._state.pending_wsp = Security_Parameters(self._state.current_wsp.connection_end)
            self._state.pending_write_state = Connection_State()
            verification_data = tls_prf_sha256(self._state.current_wsp.master_secret, b'server finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
            finished = (verification_data,)
            handshake_sfin = (FINISHED, None, finished)
            msg_counter += 1
            self.send((self.record_wrapper(TYPE_HANDSHAKE, handshake_sfin), handshake_id, msg_counter), to=client)
            self.output('SERVER - Handshake Complete')
    _TLS_Peer_handler_2200._labels = None
    _TLS_Peer_handler_2200._notlabels = None

    def _TLS_Peer_handler_2808(self, cipher_fragment, handshake_id, msg_counter):
        self.output('CHANGE_CIPHER_SPEC!!!!!!!!!!!!!!!!!!!')
        self._state.current_rsp = self._state.pending_rsp
        self._state.current_read_state = self._state.pending_read_state
        self._state.pending_rsp = Security_Parameters(self._state.current_rsp.connection_end)
        self._state.pending_read_state = Connection_State()
    _TLS_Peer_handler_2808._labels = None
    _TLS_Peer_handler_2808._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])
    _config_object = {'channel': 'reliable'}

    def run(self):
        tls_server = self.new(TLS_Peer)
        tls_client = self.new(TLS_Peer)
        (sk_root, pk_root) = keygen('public')
        (sk_server, pk_server) = keygen('public')
        server_certificate = ('server', pk_server, sign(('server', pk_server), key=sk_root))
        root_certificate = ('root', pk_root, sign(('root', pk_root), key=sk_root))
        certificate_list = (server_certificate, root_certificate)
        self._setup(tls_server, (CONN_SERVER, None, sk_server, pk_server, certificate_list))
        self._setup(tls_client, (CONN_CLIENT, tls_server, None, None, None))
        self._start(tls_server)
        self._start(tls_client)