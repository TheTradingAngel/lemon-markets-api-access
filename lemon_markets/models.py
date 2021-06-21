from enum import Enum
from dataclasses import dataclass

__all__ = ['Instrument', 'InstrumentType']


class InstrumentType(Enum):
    STOCKS = 'stocks'
    BONDS = 'bonds'
    FUNDS = 'fonds'
    WARRANTS = 'warrants'


@dataclass
class Instrument:
    isin: str = None
    wkn: str = None
    title: str = None
    type: str = None
    symbol: str = None

    @classmethod
    def from_response(cls, data: dict):
        try:
            type_ = InstrumentType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected instrument type: %r' % data.get('type'))

        return cls(
            isin=data.get('isin'),
            wkn=data.get('wkn'),
            title=data.get('title'),
            type=type_,
            symbol=data.get('symbol'),
        )
