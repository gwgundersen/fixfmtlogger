"""============================================================================
Utilities for parsing loggers.
============================================================================"""

from flogger.logger import IterFlogger

# -----------------------------------------------------------------------------


class Parser:

    pass


# -----------------------------------------------------------------------------

class IterParser(Parser):

    def __init__(self, logger):
        """
        """
        self.logger = logger
        assert(isinstance(logger, IterFlogger))
        self.iter_key = logger.iter_key
        with open(logger.fpath, 'r') as f:
            raw_lines = f.readlines()
        if len(raw_lines) == 0:
            raise ValueError(f'File "{logger.fpath}" is empty.')
        self.args, start_i = self._collect_metadata(raw_lines)
        self.results = self._collect_results(raw_lines, start_i)

    def _collect_metadata(self, raw_lines):
        """
        """
        start_i = -1
        args = {}
        for i, line in enumerate(raw_lines):
            parts = self._parts(line)
            if len(parts) == 1:
                continue
            if self._is_iter(parts):
                start_i = i
                break
            args[parts[0]] = parts[1]
        assert(start_i > 0)
        return args, start_i

    def _parts(self, line):
        """
        """
        return [l.strip() for l in line.split(':')]

    def _collect_results(self, raw_lines, start_i):
        """
        """
        results = []
        for i, line in enumerate(raw_lines[start_i:]):
            parts = self._parts(line)
            if self._is_iter(parts):
                r = dict(iter=int(parts[1]))
                results.append(r)
            elif self._is_hline(parts):
                continue
            elif len(parts) > 2:
                return results
            else:
                key, val = parts
                results[-1][key] = val
        return results

    def _is_hline(self, parts):
        """
        """
        if len(parts) > 1:
            return False
        if (parts[0] == self.logger._HLINE
                or parts[0] == self.logger._HLINE_BOLD):
            return True
        return False

    def _is_iter(self, parts):
        """
        """
        if parts[0] == self.iter_key:
            try:
                int(parts[1])
            except ValueError:
                raise ValueError('Error parsing iterations.')
            return True
        return False
