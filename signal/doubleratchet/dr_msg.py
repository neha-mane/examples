# -*- generated by 1.0.12 -*-
import da
PatternExpr_203 = da.pat.TuplePattern([da.pat.ConstantPattern('pubk_init'), da.pat.FreePattern('pubk_bytes')])
PatternExpr_210 = da.pat.FreePattern('B')
PatternExpr_287 = da.pat.TuplePattern([da.pat.ConstantPattern('rep'), da.pat.FreePattern('r'), da.pat.TuplePattern([da.pat.FreePattern('msg_header'), da.pat.FreePattern('msg_ct')])])
PatternExpr_299 = da.pat.FreePattern('B')
PatternExpr_327 = da.pat.TuplePattern([da.pat.ConstantPattern('rep'), da.pat.FreePattern('r')])
PatternExpr_334 = da.pat.FreePattern('B')
PatternExpr_418 = da.pat.TuplePattern([da.pat.ConstantPattern('msg'), da.pat.FreePattern('r'), da.pat.TuplePattern([da.pat.FreePattern('msg_header'), da.pat.FreePattern('msg_ct')])])
PatternExpr_430 = da.pat.FreePattern('A')
_config_object = {}
import sys
from sa.secalgoB import keygen
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
import doubleratchet as DR

class roleA(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._roleAReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_roleAReceivedEvent_0', PatternExpr_203, sources=[PatternExpr_210], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_roleAReceivedEvent_1', PatternExpr_287, sources=[PatternExpr_299], destinations=None, timestamps=None, record_history=None, handlers=[self._roleA_handler_286]), da.pat.EventPattern(da.pat.ReceivedEvent, '_roleAReceivedEvent_2', PatternExpr_327, sources=[PatternExpr_334], destinations=None, timestamps=None, record_history=None, handlers=[self._roleA_handler_326])])

    def setup(self, B, rounds, SK, AD, **rest_544):
        super().setup(B=B, rounds=rounds, SK=SK, AD=AD, **rest_544)
        self._state.B = B
        self._state.rounds = rounds
        self._state.SK = SK
        self._state.AD = AD
        self._state.bob_init_pubk = None
        self._state.state = DR.state()
        self._state.recv_set = set()

    def run(self):
        super()._label('_st_label_200', block=False)
        B = pubk_bytes = None

        def ExistentialOpExpr_201():
            nonlocal B, pubk_bytes
            for (_, (_, _, self._state.B), (_ConstantPattern220_, pubk_bytes)) in self._roleAReceivedEvent_0:
                if (_ConstantPattern220_ == 'pubk_init'):
                    if True:
                        return True
            return False
        _st_label_200 = 0
        while (_st_label_200 == 0):
            _st_label_200 += 1
            if ExistentialOpExpr_201():
                _st_label_200 += 1
            else:
                super()._label('_st_label_200', block=True)
                _st_label_200 -= 1
        self._state.bob_init_pubk = X25519PublicKey.from_public_bytes(pubk_bytes)
        DR.RatchetInitAlice(self._state.state, self._state.SK, self._state.bob_init_pubk)
        for r in range(self._state.rounds):
            msg = ('This is message ' + str(r))
            self.send(('msg', r, DR.RatchetEncrypt(self._state.state, msg, self._state.AD)), to=self._state.B)
            super()._label('_st_label_278', block=False)
            _st_label_278 = 0
            while (_st_label_278 == 0):
                _st_label_278 += 1
                if (r in self._state.recv_set):
                    _st_label_278 += 1
                else:
                    super()._label('_st_label_278', block=True)
                    _st_label_278 -= 1
            else:
                if (_st_label_278 != 2):
                    continue
            if (_st_label_278 != 2):
                break

    def _roleA_handler_286(self, r, msg_header, msg_ct, B):
        msg_pt = DR.RatchetDecrypt(self._state.state, msg_header, msg_ct, self._state.AD)
        self.output(msg_pt)
        self._state.recv_set.add(r)
    _roleA_handler_286._labels = None
    _roleA_handler_286._notlabels = None

    def _roleA_handler_326(self, r, B):
        self._state.recv_set.add(r)
    _roleA_handler_326._labels = None
    _roleA_handler_326._notlabels = None

class roleB(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_roleBReceivedEvent_0', PatternExpr_418, sources=[PatternExpr_430], destinations=None, timestamps=None, record_history=None, handlers=[self._roleB_handler_417])])

    def setup(self, A, rounds, SK, AD, **rest_544):
        super().setup(A=A, rounds=rounds, SK=SK, AD=AD, **rest_544)
        self._state.A = A
        self._state.rounds = rounds
        self._state.SK = SK
        self._state.AD = AD
        self._state.bob_init_key_pair = None
        self._state.state = DR.state()
        self._state.recv_count = 0

    def run(self):
        self._state.bob_init_key_pair = DR.GENERATE_DH()
        DR.RatchetInitBob(self._state.state, self._state.SK, self._state.bob_init_key_pair)
        self.send(('pubk_init', self._state.bob_init_key_pair.public_key().public_bytes()), to=self._state.A)
        super()._label('_st_label_409', block=False)
        _st_label_409 = 0
        while (_st_label_409 == 0):
            _st_label_409 += 1
            if (self._state.recv_count == self._state.rounds):
                _st_label_409 += 1
            else:
                super()._label('_st_label_409', block=True)
                _st_label_409 -= 1

    def _roleB_handler_417(self, r, msg_header, msg_ct, A):
        msg_pt = DR.RatchetDecrypt(self._state.state, msg_header, msg_ct, self._state.AD)
        self.output(msg_pt)
        self._state.recv_count += 1
        rep = ('This is reply ' + str(r))
        self.send(('rep', r, DR.RatchetEncrypt(self._state.state, rep, self._state.AD)), to=A)
    _roleB_handler_417._labels = None
    _roleB_handler_417._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])

    def run(self):
        rounds = (int(sys.argv[1]) if (len(sys.argv) > 1) else 10)
        SK = keygen('random', 32)
        AD = keygen('random', 32)
        A = self.new(roleA)
        B = self.new(roleB)
        self._setup(A, (B, rounds, SK, AD))
        self._setup(B, (A, rounds, SK, AD))
        self._start(B)
        self._start(A)
