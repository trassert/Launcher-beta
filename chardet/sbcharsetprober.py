from typing import Dict, List, NamedTuple, Optional, Union
from .charsetprober import CharSetProber
from .enums import CharacterCategory, ProbingState, SequenceLikelihood
class SingleByteCharSetModel(NamedTuple):
    charset_name: str
    language: str
    char_to_order_map: Dict[int, int]
    language_model: Dict[int, Dict[int, int]]
    typical_positive_ratio: float
    keep_ascii_letters: bool
    alphabet: str
class SingleByteCharSetProber(CharSetProber):
    SAMPLE_SIZE = 64
    SB_ENOUGH_REL_THRESHOLD = 1024  
    POSITIVE_SHORTCUT_THRESHOLD = 0.95
    NEGATIVE_SHORTCUT_THRESHOLD = 0.05
    def __init__(
        self,
        model: SingleByteCharSetModel,
        is_reversed: bool = False,
        name_prober: Optional[CharSetProber] = None,
    ) -> None:
        super().__init__()
        self._model = model
        self._reversed = is_reversed
        self._name_prober = name_prober
        self._last_order = 255
        self._seq_counters: List[int] = []
        self._total_seqs = 0
        self._total_char = 0
        self._control_char = 0
        self._freq_char = 0
        self.reset()
    def reset(self) -> None:
        super().reset()
        self._last_order = 255
        self._seq_counters = [0] * SequenceLikelihood.get_num_categories()
        self._total_seqs = 0
        self._total_char = 0
        self._control_char = 0
        self._freq_char = 0
    @property
    def charset_name(self) -> Optional[str]:
        if self._name_prober:
            return self._name_prober.charset_name
        return self._model.charset_name
    @property
    def language(self) -> Optional[str]:
        if self._name_prober:
            return self._name_prober.language
        return self._model.language
    def feed(self, byte_str: Union[bytes, bytearray]) -> ProbingState:
        if not self._model.keep_ascii_letters:
            byte_str = self.filter_international_words(byte_str)
        else:
            byte_str = self.remove_xml_tags(byte_str)
        if not byte_str:
            return self.state
        char_to_order_map = self._model.char_to_order_map
        language_model = self._model.language_model
        for char in byte_str:
            order = char_to_order_map.get(char, CharacterCategory.UNDEFINED)
            if order < CharacterCategory.CONTROL:
                self._total_char += 1
            if order < self.SAMPLE_SIZE:
                self._freq_char += 1
                if self._last_order < self.SAMPLE_SIZE:
                    self._total_seqs += 1
                    if not self._reversed:
                        lm_cat = language_model[self._last_order][order]
                    else:
                        lm_cat = language_model[order][self._last_order]
                    self._seq_counters[lm_cat] += 1
            self._last_order = order
        charset_name = self._model.charset_name
        if self.state == ProbingState.DETECTING:
            if self._total_seqs > self.SB_ENOUGH_REL_THRESHOLD:
                confidence = self.get_confidence()
                if confidence > self.POSITIVE_SHORTCUT_THRESHOLD:
                    self.logger.debug(
                        "%s confidence = %s, we have a winner", charset_name, confidence
                    )
                    self._state = ProbingState.FOUND_IT
                elif confidence < self.NEGATIVE_SHORTCUT_THRESHOLD:
                    self.logger.debug(
                        "%s confidence = %s, below negative shortcut threshold %s",
                        charset_name,
                        confidence,
                        self.NEGATIVE_SHORTCUT_THRESHOLD,
                    )
                    self._state = ProbingState.NOT_ME
        return self.state
    def get_confidence(self) -> float:
        r = 0.01
        if self._total_seqs > 0:
            r = (
                (
                    self._seq_counters[SequenceLikelihood.POSITIVE]
                    + 0.25 * self._seq_counters[SequenceLikelihood.LIKELY]
                )
                / self._total_seqs
                / self._model.typical_positive_ratio
            )
            r = r * (self._total_char - self._control_char) / self._total_char
            r = r * self._freq_char / self._total_char
            if r >= 1.0:
                r = 0.99
        return r
