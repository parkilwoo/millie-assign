from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from domain.coupon.collection import Coupons
from domain.coupon.entity import Coupon

class CouponRepository(ABC):
    @abstractmethod
    def save(self, coupon: Coupon) -> Coupon:
        pass

    @abstractmethod
    def find_by_ids(self, ids: List[int]) -> Coupons:
        pass

    @abstractmethod
    def find_valid_by_product_id(self, product_id: int, now: datetime) -> Coupons:
        pass

