from datetime import datetime
from domain.coupon.policy import CouponPolicy
from domain.coupon.value_object import CouponType

class Coupon:
    """
    Coupon Domain Entity
    이름, 정책, 유효기간, 사용제한 등의 정보 포함
    """
    def __init__(
        self,
        name: str,
        coupon_type: CouponType,
        policy: CouponPolicy,
        expired_date: datetime,
        usage_limit: int = 1
    ):
        self._coupon_id   = None
        self.name = name
        self.coupon_type = coupon_type
        self.policy = policy
        self.expired_date = expired_date
        self.usage_limit = usage_limit
    @property
    def coupon_id(self) -> int:
        return self._coupon_id

    def _set_coupon_id(self, coupon_id: int):
        if self._coupon_id is not None:
            raise AttributeError("coupon_id는 한 번만 설정할 수 있습니다.")
        self._coupon_id = coupon_id

    def is_valid(self, now: datetime) -> bool:
        return self.expired_date >= now and self.usage_limit > 0