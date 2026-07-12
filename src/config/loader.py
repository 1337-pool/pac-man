import pathlib
import json

class ParsingError(Exception):
    pass


def strip_comments(s: str) -> str:
    clean_config: str = ""
    i = 0
    in_string = False

    while i < len(s):
        if s[i] == '"' and (i == 0 or s[i - 1] != '\\'):
            in_string = not in_string
            clean_config += s[i]
            i += 1
            continue

        if in_string:
            clean_config += s[i]
            i += 1
            continue

        if s[i] == "#":
            while s[i] != "\n" and i != len(s) - 1:
                i += 1
        elif s[i] == '/' and i != len(s) - 1 and s[i + 1] == '/':
            while s[i] != "\n" and i != len(s) - 1:
                i += 1
        elif s[i] == '/' and i != len(s) - 1 and s[i + 1] == '*':
            while i < len(s) - 1 and not (s[i] == '*' and s[i + 1] == '/'):
                i += 1
            i += 1
        else:
            clean_config += s[i]
        i += 1

    return clean_config

# handlit hado : /* */   //  #
# o hadi: {"name": "a#b"}
# o filenotfound o invalid json o permission error

def load_config(path: str) -> dict:

    if pathlib.Path(path).suffix != ".json":
        raise ParsingError("invalid file suffix")

    try:
        with open(path) as f:
            clean_config: str = strip_comments(f.read())
            if not len(clean_config):
                raise ParsingError("empty file ajmi:)")
            dic = json.loads(clean_config)

    except FileNotFoundError:
        raise ParsingError(f"File not found: {path}")

    except OSError:
        raise ParsingError(f"OSError: {path}")

    except PermissionError:
        raise ParsingError(f"permission error (n9s f chkhsiya): {path}")

    except json.JSONDecodeError as exc:
        raise ParsingError(f"Invalid JSON: {exc}")

    return dic
