import fixfmt
from   fixfmt.table import (DEFAULT_CFG,
                            UNICODE_BOX_CFG)


# -----------------------------------------------------------------------------

class StatelessRowTable:

    def __init__(self, header, width=6, vlines=False):
        if vlines:
            self.cfg = UNICODE_BOX_CFG
        else:
            self.cfg = DEFAULT_CFG
        self.header_ = header
        self.fmts = {}
        for name in self.header_:
            if name not in self.fmts:
                self.fmts[name] = fixfmt.String(width)

    def register(self, row):
        if not set(row.keys()) == set(self.header_):
            raise ValueError()
        fmts = [self.fmts.get(n) for n in self.header_]
        vals = [row.get(n) for n in self.header_]
        return self._fmt(fmts, vals)

    def header(self):
        fmts = [self.fmts.get(n) for n in self.header_]
        vals = self.header_
        return self._fmt(fmts, vals)

    def hline(self):
        cfg = self.cfg["underline"]
        fmts = [self.fmts.get(n, None) for n in self.header_]
        sep = cfg["separator"]
        return (
              sep["start"]
            + "".join(
                  (sep["between"] if i > 0 else "")
                + cfg["line"] * f.width
                for i, f in enumerate(fmts)
            )
            + sep["end"]
        )

    def _fmt(self, fmts, vals):
        sep = self.cfg["row"]["separator"]
        vals = [
            " " * f.width if v is None else f(v)
            for f, v in zip(fmts, vals)
        ]
        return (
              sep["start"]
            + sep["between"].join(vals)
            + sep["end"]
        )
