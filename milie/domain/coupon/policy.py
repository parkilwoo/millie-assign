from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Callable

from domain.coupon.exception import InvalidDiscountAmount
from domain.coupon.value_object import CouponApplyResult, CouponType
"""
쿠폰 정책이 다양해지거나 변경될 것을 고려하여, Strategy 패턴을 적용
"""
class CouponPolicy(ABC):
    """
    쿠폰 정책 Interface
    """    
    @abstractmethod
    def apply(
        self,
        unit_price: Decimal,
        quantity: int,
        shipping_fee: Decimal
    ) -> CouponApplyResult:
        pass

class FixedDiscountCoupon(CouponPolicy):
    """
    고정 금액 할인 쿠폰 구현체
    """
    def __init__(self, amount: Decimal):
        self.amount = amount

    def apply(self, unit_price, quantity, shipping_fee):
        total_price = unit_price * quantity
        return CouponApplyResult(discount_amount=min(self.amount, total_price))

class RateDiscountCoupon(CouponPolicy):
    """
    비율 금액 할인 쿠폰 구현체 
    """
    def __init__(self, rate: float):
        if not 0 <= rate <= 1.0:
            raise InvalidDiscountAmount("쿠폰을 이용한 할인율은 0 ~ 100%만 가능합니다.")
        self.rate = rate

    def apply(self, unit_price, quantity, shipping_fee):
        total_price = unit_price * quantity
        discount = total_price * Decimal(self.rate)
        return CouponApplyResult(discount_amount=discount)
    
class FreeShippingCoupon(CouponPolicy):
    """
    배송비 무료 쿠폰 구현체
    """
    def apply(self, unit_price, quantity, shipping_fee):
        return CouponApplyResult(free_shipping=True)
    
class OnePlusOneCoupon(CouponPolicy):
    """
    1+1 쿠폰 구현체
    """
    def apply(self, unit_price, quantity, shipping_fee):
        bonus = quantity // 2
        return CouponApplyResult(bonus_quantity=bonus)

class NoneCoupon(CouponPolicy):
    """
    쿠폰 미사용 구현체
    """
    def apply(self, unit_price, quantity, shipping_fee):
        return CouponApplyResult()
    

class CouponPolicyFactory:
    # CouponType 별로, DB 모델에서 받은 value 처리
    _registry: dict[CouponType, Callable[[Decimal | None], CouponPolicy]] = {
        CouponType.FIXED_DISCOUNT:  lambda v: FixedDiscountCoupon(amount=v or Decimal("0")),
        CouponType.RATE_DISCOUNT:   lambda v: RateDiscountCoupon(rate=float(v or 0)),
        CouponType.FREE_SHIPPING:   lambda v: FreeShippingCoupon(),
        CouponType.ONE_PLUS_ONE:    lambda v: OnePlusOneCoupon(),
    }

    @classmethod
    def create(cls, coupon_type: CouponType, value: Decimal | None) -> CouponPolicy:
        factory = cls._registry.get(coupon_type)
        if not factory:
            return NoneCoupon() 
        return factory(value)    