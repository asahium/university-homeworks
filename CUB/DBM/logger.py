from collections import OrderedDict


class Logger:
    def __init__(self, name, fmt=None):
        self.name = name
        self.fmt = fmt or {}
        self._current = OrderedDict()
        self._header_printed = False

    def add_scalar(self, step, key, value):
        self._current['step'] = step
        self._current[key] = value

    def iter_info(self):
        if not self._header_printed:
            print(' | '.join(f'{k:>10}' for k in self._current))
            self._header_printed = True

        parts = []
        for key, val in self._current.items():
            if key == 'step':
                parts.append(f'{val:>10}')
            else:
                fmt_spec = self.fmt.get(key)
                if fmt_spec:
                    formatted = format(val, fmt_spec)
                else:
                    formatted = f'{val:.4f}' if isinstance(val, float) else str(val)
                parts.append(f'{formatted:>10}')

        print(' | '.join(parts))
        self._current = OrderedDict()
