import sys
import atexit
def exit_cacert_ctx() -> None: _CACERT_CTX.__exit__(None, None, None)  
if sys.version_info >= (3, 11):
    from importlib.resources import as_file, files
    _CACERT_CTX = None
    _CACERT_PATH = None
    def where() -> str:
        global _CACERT_CTX
        global _CACERT_PATH
        if _CACERT_PATH is None:
            _CACERT_CTX = as_file(files("certifi").joinpath("cacert.pem"))
            _CACERT_PATH = str(_CACERT_CTX.__enter__())
            atexit.register(exit_cacert_ctx)
        return _CACERT_PATH
    def contents() -> str: return files("certifi").joinpath("cacert.pem").read_text(encoding="ascii")