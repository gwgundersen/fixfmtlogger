"""============================================================================
Logger with fix-width formatting.
============================================================================"""

import fixfmt
from   flogger.table import StatelessRowTable
import logging
import os
import sys


# -----------------------------------------------------------------------------
# Base Flogger class.
# -----------------------------------------------------------------------------

class Flogger:

    _DEF_LINE_W   = 80
    _HLINE        = '-' * _DEF_LINE_W
    _HLINE_BOLD   = '=' * _DEF_LINE_W

    def __init__(self, fpath=None, overwrite=False, precision=6, metadata=None,
                 flush=False):
        """
        """
        if fpath:
            if os.path.exists(fpath) and not overwrite:
                raise FileExistsError(f'File "{fpath}" already exists.')

            # Create underlying logger.
            self.fpath = fpath
            handler = logging.FileHandler(f'{self.fpath}', mode='w+')
            self.logger = logging.getLogger('logger.main')
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(handler)

            self.use_file = True
        else:
            self.use_file = False

        self.precision = precision

        self.first = True
        self.flush = flush

        if metadata:
            self.hline(bold=True)
            self._log_metadata(metadata)

    def log(self, data):
        """
        """
        raise NotImplementedError()

    def hline(self, bold=False):
        """
        """
        mark = self._HLINE_BOLD if bold else self._HLINE
        self._log(mark)

    def format_number(self, value):
        """
        """
        return f'{float(value):.{self.precision}f}'

# -----------------------------------------------------------------------------
# "Private" functions.
# -----------------------------------------------------------------------------

    def _log(self, msg):
        """
        """
        if self.use_file:
            self.logger.info(msg)
            if self.flush:
                sys.stdout.flush()
        else:
            print(msg)

    def _log_metadata(self, args):
        """
        """
        self._log('Metadata')
        # Call `var` because `args` can be an `argparse.ArgumentParser`
        # instance.
        fields  = [f for f in args]
        longest = len(max(fields, key=len))
        fmtter  = fixfmt.String(longest)
        for k, v in args.items():
            self._log(f'  {fmtter(k)}: {v}')


# -----------------------------------------------------------------------------
# Iteration-based logging.
# -----------------------------------------------------------------------------

class KeyValLogger(Flogger):

    def __init__(self, fpath=None, key_width=None, val_width=None,
                 overwrite=False, precision=6, metadata=None, flush=False,
                 iter_key='iter', freq=1):
        """
        """
        super().__init__(
            fpath=fpath,
            overwrite=overwrite,
            precision=precision,
            metadata=metadata,
            flush=flush
        )
        self.key_width = key_width
        self.val_width = val_width
        self.key_fmttr = None
        self.val_fmttr = None
        self.iter_keys = None
        self.iter_key  = iter_key
        self.freq      = freq

    def log(self, data):
        """
        """
        if data[self.iter_key] % self.freq != 0:
            return

        if self.first:
            self.first = False
            self.iter_keys = data.keys()

            if not self.key_width:
                fields = [k for k in data.keys()]
                self.key_width = len(max(fields, key=len))
            if not self.val_width:
                # Minus 2 because of the ': ' characters.
                self.val_width = self._DEF_LINE_W - self.key_width - 2

            self.key_fmttr = fixfmt.String(self.key_width)
            self.val_fmttr = fixfmt.String(self.val_width)
            self.hline(bold=True)
        else:
            if self.iter_keys != data.keys():
                raise ValueError('Data is inconsistent across iterations.')
            self.hline()
        if self.iter_key not in self.iter_keys:
            raise ValueError('Iteration number not provided.')

        for k, v in data.items():
            if is_number(v) and k != self.iter_key:
                v = self.format_number(v)
            self._log(f'{self.key_fmttr(k)}: {self.val_fmttr(v)}')

    def get_format_map(self):
        """
        """
        map_ = {}
        for k in self.iter_keys:
            map_[self.key_fmttr(k)] = k
        return map_


# -----------------------------------------------------------------------------
# Table-based logging.
# -----------------------------------------------------------------------------

class TableLogger(Flogger):

    def __init__(self, header, sep='\t', fpath=None, cell_width=None,
                 vlines=True, overwrite=False, precision=6, metadata=None,
                 flush=False):
        """
        """
        self.header = header
        self.sep    = sep
        self.tbl    = StatelessRowTable(header, width=cell_width,
                                        vlines=vlines)

        super().__init__(
            fpath=fpath,
            overwrite=overwrite,
            precision=precision,
            metadata=metadata,
            flush=flush
        )

        self.hline(bold=True)
        self._log(self.tbl.header())
        self._log(self.tbl.hline())

    def log(self, data):
        line = self.tbl.register(data)
        self._log(line)


# -----------------------------------------------------------------------------
# Utilities.
# -----------------------------------------------------------------------------

def is_number(obj):
    """Return `True` if object is number, `False` otherwise.
    """
    if isinstance(obj, bool):
        return False
    try:
        float(obj)
        return True
    except (TypeError, ValueError):
        return False
