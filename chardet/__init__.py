from typing import List, Union
from .charsetgroupprober import CharSetGroupProber
from .charsetprober import CharSetProber
from .enums import InputState
from .resultdict import ResultDict
from .universaldetector import UniversalDetector
from .version import VERSION, __version__
__all__ = ["UniversalDetector", "detect", "detect_all", "__version__", "VERSION"]
def detect(
    byte_str: Union[bytes, bytearray], should_rename_legacy: bool = False
) -> ResultDict:
    if not isinstance(byte_str, bytearray):
        if not isinstance(byte_str, bytes):
            raise TypeError(
                f"Expected object of type bytes or bytearray, got: {type(byte_str)}"
            )
        byte_str = bytearray(byte_str)
    detector = UniversalDetector(should_rename_legacy=should_rename_legacy)
    detector.feed(byte_str)
    return detector.close()
def detect_all(
    byte_str: Union[bytes, bytearray],
    ignore_threshold: bool = False,
    should_rename_legacy: bool = False,
) -> List[ResultDict]:
    if not isinstance(byte_str, bytearray):
        if not isinstance(byte_str, bytes):
            raise TypeError(
                f"Expected object of type bytes or bytearray, got: {type(byte_str)}"
            )
        byte_str = bytearray(byte_str)
    detector = UniversalDetector(should_rename_legacy=should_rename_legacy)
    detector.feed(byte_str)
    detector.close()
    if detector.input_state == InputState.HIGH_BYTE:
        results: List[ResultDict] = []
        probers: List[CharSetProber] = []
        for prober in detector.charset_probers:
            if isinstance(prober, CharSetGroupProber):
                probers.extend(p for p in prober.probers)
            else:
                probers.append(prober)
        for prober in probers:
            if ignore_threshold or prober.get_confidence() > detector.MINIMUM_THRESHOLD:
                charset_name = prober.charset_name or ""
                lower_charset_name = charset_name.lower()
                if lower_charset_name.startswith("iso-8859") and detector.has_win_bytes:
                    charset_name = detector.ISO_WIN_MAP.get(
                        lower_charset_name, charset_name
                    )
                if should_rename_legacy:
                    charset_name = detector.LEGACY_MAP.get(
                        charset_name.lower(), charset_name
                    )
                results.append(
                    {
                        "encoding": charset_name,
                        "confidence": prober.get_confidence(),
                        "language": prober.language,
                    }
                )
        if len(results) > 0:
            return sorted(results, key=lambda result: -result["confidence"])
    return [detector.result]
