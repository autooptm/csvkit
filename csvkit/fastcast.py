
import datetime as _datetime
import os
import re
from decimal import Decimal

import agate


class _Verified:

    _fast_ok = None

    def _shortcut(self, value):
        raise NotImplementedError

    def cast(self, d):
        if self._fast_ok is not False and type(d) is str:
            fast = self._shortcut(d)
            if fast is not None:
                if self._fast_ok is None:
                    self._fast_ok = fast == super().cast(d)
                    if not self._fast_ok:
                        return super().cast(d)
                return fast
        return super().cast(d)


class Date(_Verified, agate.Date):
    _ISO = re.compile(r'\A(\d{4})-(\d{2})-(\d{2})\Z')

    def _shortcut(self, d):
        if self.date_format is not None:
            return None
        m = self._ISO.match(d.strip())
        if m is None:
            return None
        try:
            return _datetime.date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError:
            return None


class DateTime(_Verified, agate.DateTime):
    _ISO = re.compile(r'\A(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})\Z')

    def _shortcut(self, d):
        if self.datetime_format is not None or getattr(self, 'timezone', None) is not None:
            return None
        m = self._ISO.match(d.strip())
        if m is None:
            return None
        try:
            return _datetime.datetime(int(m[1]), int(m[2]), int(m[3]),
                                      int(m[4]), int(m[5]), int(m[6]))
        except ValueError:
            return None


class Number(_Verified, agate.Number):
    _PLAIN = re.compile(r'\A-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z')

    def _shortcut(self, d):
        s = d.strip()
        if self._PLAIN.match(s) is None:
            return None
        return Decimal(s)


def types():
    if os.getenv('CSVKIT_NO_FASTCAST'):
        return agate.Number, agate.Date, agate.DateTime
    return (agate.Number if os.getenv('CSVKIT_FASTCAST_NUMBER') == '0' else Number,
            agate.Date if os.getenv('CSVKIT_FASTCAST_DATE') == '0' else Date,
            agate.DateTime if os.getenv('CSVKIT_FASTCAST_DATE') == '0' else DateTime)
