from datetime import datetime
from typing import List

from domain.coupon.entity import Coupon

class Coupons:
    """
    Coupon Collection
    """
    def __init__(self, items: List[Coupon]):
        self._items = items

    def valid(self, now: datetime) -> "Coupons":
        return Coupons([c for c in self._items if c.is_valid(now)])

    def all(self) -> List[Coupon]:
        return list(self._items)
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)    