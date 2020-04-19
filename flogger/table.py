import numpy as np

from   fixfmt import palide, string_length
from   fixfmt.table import (RowTable,
                            _get_formatter,
                            _get_header_position)

# -----------------------------------------------------------------------------


class StatelessRowTable(RowTable):

    def __init__(self):
        super().__init__()
        self.row = None

    def register(self, fields):
        self.row = fields
        for name in fields:
            if name not in self.names:
                self.names.append(name)

        self.set_fmts()

        row   = self.row
        names = self.names
        fmts  = [self.fmts.get(n, None) for n in names]
        defs  = [self.defaults.get(n, None) for n in names]
        vals  = (row.get(n, d) for n, d in zip(names, defs))

        sep = self.cfg["row"]["separator"]
        vals = (
            " " * f.width if v is None else f(v)
            for f, v in zip(fmts, vals)
        )

        return (
              sep["start"]
            + sep["between"].join(vals)
            + sep["end"]
        )

    def header(self):

        names = self.names
        fmts  = [self.fmts.get(n, None) for n in names]
        cfg   = self.cfg["header"]

        assert string_length(cfg["style"]["prefix"]) == 0
        assert string_length(cfg["style"]["suffix"]) == 0

        sep = cfg["separator"]

        def format_name(name, fmt):
            name = name or ""
            name = cfg["prefix"] + name + cfg["suffix"]
            pad_pos = _get_header_position(fmt)
            name = palide(
                name,
                fmt.width,
                elide_pos   =cfg["elide"]["position"],
                ellipsis    =cfg["elide"]["ellipsis"],
                pad_pos     =pad_pos
            )
            name = cfg["style"]["prefix"] + name + cfg["style"]["suffix"]
            return name

        return sep["start"] + sep["between"].join(
            format_name(n, f)
            for n, f in zip(names, fmts)
        ) + sep["end"]

    def set_fmts(self):
        cfg = self.cfg['formatters']
        for name in self.names:
            if name not in self.fmts:
                # FIXME: Do better.
                arr = np.array([
                    r[name] for r in [self.row]
                    if name in r
                    and r[name] is not None
                ])
                self.fmts[name] = _get_formatter(name, arr, cfg=cfg)

    def _line(self, fmts, cfg):
        if not cfg["show"]:
            return

        sep = cfg["separator"]
        yield (
              sep["start"]
            + "".join(
                  (sep["between"] if i > 0 else "")
                + cfg["line"] * f.width
                for i, f in enumerate(fmts)
            )
            + sep["end"]
        )
