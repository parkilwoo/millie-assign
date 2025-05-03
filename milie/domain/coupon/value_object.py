from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class CouponType(Enum):
    """
    쿠폰 타입을 정의한 Enum Class
    """
    FIXED_DISCOUNT = "금액 할인"
    RATE_DISCOUNT = "비율 할인"
    FREE_SHIPPING = "배송비 무료"
    ONE_PLUS_ONE = "1+1 증정"
    # TODO 추후 새로운 쿠폰 타입이 추가되면 작성

@dataclass
class CouponApplyResult:
    """
    쿠폰 사용 결과를 나타내는 Class
    """
    discount_amount: Decimal = Decimal("0")
    free_shipping: bool = False
    bonus_quantity: int = 0
    final_price: Decimal = Decimal("0")
    # TODO 추후 새로운 쿠폰 정책이 추가되면 작성(eg. 사은품 증정: bonus_free_gift)