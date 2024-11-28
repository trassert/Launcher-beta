from typing import Union
from .chardistribution import SJISDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .enums import MachineState, ProbingState
from .jpcntx import SJISContextAnalysis
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import SJIS_SM_MODEL
class SJISProber(MultiByteCharSetProber):
    def __init__(self) -> None:
        super().__init__()
        self.coding_sm = CodingStateMachine(SJIS_SM_MODEL)
        self.distribution_analyzer = SJISDistributionAnalysis()
        self.context_analyzer = SJISContextAnalysis()
        self.reset()
    def reset(self) -> None:
        super().reset()
        self.context_analyzer.reset()
    @property
    def charset_name(self) -> str:
        return self.context_analyzer.charset_name
    @property
    def language(self) -> str:
        return "Japanese"
    def feed(self, byte_str: Union[bytes, bytearray]) -> ProbingState:
        assert self.coding_sm is not None
        assert self.distribution_analyzer is not None
        for i, byte in enumerate(byte_str):
            coding_state = self.coding_sm.next_state(byte)
            if coding_state == MachineState.ERROR:
                self.logger.debug(
                    "%s %s prober hit error at byte %s",
                    self.charset_name,
                    self.language,
                    i,
                )
                self._state = ProbingState.NOT_ME
                break
            if coding_state == MachineState.ITS_ME:
                self._state = ProbingState.FOUND_IT
                break
            if coding_state == MachineState.START:
                char_len = self.coding_sm.get_current_charlen()
                if i == 0:
                    self._last_char[1] = byte
                    self.context_analyzer.feed(
                        self._last_char[2 - char_len :], char_len
                    )
                    self.distribution_analyzer.feed(self._last_char, char_len)
                else:
                    self.context_analyzer.feed(
                        byte_str[i + 1 - char_len : i + 3 - char_len], char_len
                    )
                    self.distribution_analyzer.feed(byte_str[i - 1 : i + 1], char_len)
        self._last_char[0] = byte_str[-1]
        if self.state == ProbingState.DETECTING:
            if self.context_analyzer.got_enough_data() and (
                self.get_confidence() > self.SHORTCUT_THRESHOLD
            ):
                self._state = ProbingState.FOUND_IT
        return self.state
    def get_confidence(self) -> float:
        assert self.distribution_analyzer is not None
        context_conf = self.context_analyzer.get_confidence()
        distrib_conf = self.distribution_analyzer.get_confidence()
        return max(context_conf, distrib_conf)
