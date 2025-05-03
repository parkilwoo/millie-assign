from decimal import Decimal
from domain.product.discount_policy import DiscountPolicy
from domain.coupon.collection import Coupons
from domain.product.value_object import PriceResult

class Product:
    """
    Product domain Entity
    가격, 이름, 할인정책 같은 기본적인 속성만 포함
    DiscountPolicy는 Product에 종속적인 관계이므로 필드로 포함
    """
    def __init__(
        self, 
        name: str,
        base_price: Decimal,
        shipping_fee: Decimal,
        discount_policy: DiscountPolicy
    ):
        self._product_id = None
        self.name = name
        self.base_price = base_price
        self.shipping_fee = shipping_fee
        self.discount_policy = discount_policy

    @property
    def product_id(self) -> int:
        return self._product_id

    def _set_product_id(self, product_id: int):
        if self._product_id is not None:
            raise AttributeError("product_id는 1번만 설정이 가능합니다")
        self._product_id = product_id

    def calculate_discount_price(self) -> Decimal:
        return self.discount_policy.apply(self.base_price)
    
    def calculate_price_with_coupons(
        self,
        coupons: Coupons,
        quantity: int
    ) -> PriceResult:
        """
        주어진 쿠폰 리스트와 수량을 반영하여
        최종 가격을 계산한 결과를 반환합니다.
        """
        unit_price = self.calculate_discount_price()
        original   = unit_price * quantity

        total_discount = Decimal("0")
        free_shipping  = False
        bonus_quantity = 0

        for coupon in coupons:
            result = coupon.policy.apply(
                unit_price   = self.base_price,
                quantity     = quantity,
                shipping_fee = self.shipping_fee
            )
            total_discount += result.discount_amount
            free_shipping  = free_shipping or result.free_shipping
            bonus_quantity += result.bonus_quantity

        final_shipping = Decimal("0") if free_shipping else self.shipping_fee
        final_price    = max(Decimal("0"), original - total_discount + final_shipping)
        
        return PriceResult(
            original_price=original,
            total_discount=total_discount,
            final_price=final_price,
            free_shipping=free_shipping,
            shipping_fee=final_shipping,
            bonus_quantity=bonus_quantity
        )