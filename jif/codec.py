"""`# coding: jif` -- teaches Python the `jif` / `eljif` keywords by rewriting source before it's parsed.

Registered at interpreter startup by jif.pth, so it works in any file with the cookie.
"""
import codecs
import encodings.utf_8 as utf8
import io
import tokenize

_STARTS = {tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING}


def transform(src):
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, SyntaxError):
        return src  # let Python produce the real error
    offsets = [0]
    for line in src.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    pos = lambda rc: offsets[rc[0] - 1] + rc[1]

    edits = []
    for i, t in enumerate(toks):
        if t.type != tokenize.NAME or t.string not in ("jif", "eljif"):
            continue
        if i and toks[i - 1].type not in _STARTS:
            continue  # `jif` used as a normal name, e.g. jif("x > 5")
        depth = 0
        for j in range(i + 1, len(toks)):
            s = toks[j].string
            if toks[j].type == tokenize.OP:
                depth += s in "([{"
                depth -= s in ")]}"
                if s == ":" and depth == 0:
                    break  # ponytail: a lambda in the condition confuses this, don't put lambdas in a jif
        else:
            continue
        expr = src[pos(toks[i + 1].start):pos(toks[j].start)]
        kw = "if" if t.string == "jif" else "elif"
        pad = "\n" * expr.count("\n")  # keep line numbers stable for multi-line conditions
        edits.append((pos(t.start), pos(toks[j].start), f'{kw} __import__("jif").jif({" ".join(expr.split())!r}{pad})'))

    for start, end, new in reversed(edits):
        src = src[:start] + new + src[end:]
    return src


def decode(data, errors="strict"):
    text, n = utf8.decode(data, errors)
    return transform(text), n


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, data, errors, final):
        return decode(data, errors) if final else ("", 0)  # need the whole file to rewrite it


def _search(name):
    if name == "jif":
        return codecs.CodecInfo(
            name="jif", encode=utf8.encode, decode=decode,
            incrementalencoder=utf8.IncrementalEncoder, incrementaldecoder=IncrementalDecoder,
            streamreader=utf8.StreamReader, streamwriter=utf8.StreamWriter,
        )


codecs.register(_search)
