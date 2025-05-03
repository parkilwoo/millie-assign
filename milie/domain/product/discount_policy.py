from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Callable, Optional

class DiscountPolicyType(str, Enum):
    """
    할인 정책 Type
    """
    NONE = "NONE"
    RATE = "RATE"
    AMOUNT = "AMOUNT"

"""
할인 정책이 다양해지거나 변경될 것을 고려하여, Strategy 패턴을 적용
"""
class DiscountPolicy(ABC):
    """
    할인 정책 Interface
    """
    @abstractmethod
    def apply(self, price: Decimal) -> Decimal:
        pass

    @abstractmethod
    def get_type_and_value(self) -> tuple[DiscountPolicyType, Decimal | None]:
        pass

class RateDiscountPolicy(DiscountPolicy):
    """
    비율 할인 정책 구현체
    """
    def __init__(self, rate: float):
        if not 0 <= rate <= 1.0:
            raise ValueError("할인율은 0 ~ 100%만 가능합니다.")
        self.rate = rate

    def apply(self, price):
        return price * Decimal(1 - self.rate)
    
    def get_type_and_value(self):
        return (DiscountPolicyType.RATE, Decimal(self.rate))

class AmountDiscountPolicy(DiscountPolicy):
    """
    금액 할인 정책 구현체
    """
    def __init__(self, amount: Decimal):
        self.amount = amount
    
    def apply(self, price):
        return max(price - self.amount, Decimal("0"))
    
    def get_type_and_value(self):
        return (DiscountPolicyType.AMOUNT, self.amount)

class NoneDiscountPolicy(DiscountPolicy):
    """
    할인 미적용 구현체
    """
    def apply(self, price):
        return price
    
    def get_type_and_value(self):
        return (DiscountPolicyType.NONE, None)
    
# TODO 새로운 할인 정책이 생길경우 추가



class DiscountPolicyFactory:
    """
    DiscountPolicyType 별로 생성 함수를 매핑해 두는 레지스트리 패턴
    """
    # policy_type -> (value) -> DiscountPolicy 인스턴스를 반환하는 팩토리 함수
    _registry: dict[DiscountPolicyType, Callable[[Optional[Decimal]], DiscountPolicy]] = {
        DiscountPolicyType.NONE:  lambda v: NoneDiscountPolicy(),
        DiscountPolicyType.AMOUNT: lambda v: AmountDiscountPolicy(v if v is not None else Decimal("0")),
        DiscountPolicyType.RATE:   lambda v: (
            RateDiscountPolicy(float(v))
            if v is not None else (_raise("할인율이 필요합니다."))
        ),
    }

    @classmethod
    def create(cls, policy_type: DiscountPolicyType, value: Optional[Decimal]) -> DiscountPolicy:
        factory = cls._registry.get(policy_type)
        if not factory:
            raise NoneDiscountPolicy()
        return factory(value)
    
def _raise(msg: str):
    # Lambda에서 Exception helper
    raise ValueError(msg)    