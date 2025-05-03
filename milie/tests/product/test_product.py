from decimal import Decimal
import pytest
from domain.coupon.collection import Coupons
from domain.coupon.value_object import CouponApplyResult

def test_apply_single_fixed(sample_product, fixed_coupon):
    """
    Product.apply_coupons()이 단일 고정할인 쿠폰을 제대로 적용하는지
    """
    coll = Coupons([fixed_coupon]).valid()
    result: CouponApplyResult = sample_product.apply_coupons(coll, quantity=2)

    # 원가 10,000×2=20,000 에서 1,000원 할인 + 배송비 2,000원
    assert result.discount_amount == Decimal("1000")
    assert not result.free_shipping
    assert result.bonus_quantity == 0
    assert result.final_price == Decimal("20000") - Decimal("1000") + Decimal("2000")

def test_apply_fixed_and_free_shipping(sample_product, fixed_coupon, free_ship_coupon):
    """
    Product.apply_coupons()이 고정할인 + 무료배송 쿠폰 조합을 제대로 처리하는지
    """
    coll = Coupons([fixed_coupon, free_ship_coupon]).valid()
    result: CouponApplyResult = sample_product.apply_coupons(coll, quantity=1)

    # 할인 1,000원, 무료배송 적용
    assert result.discount_amount == Decimal("1000")
    assert result.free_shipping
    # final_price = 10,000 - 1,000 (할인) + 0 (무료배송)
    assert result.final_price == Decimal("9000")

def test_apply_ignores_expired(sample_product, fixed_coupon, expired_coupon):
    """
    expired 쿠폰은 걸러지고, valid 쿠폰만 적용되는지
    """
    coll = Coupons([fixed_coupon, expired_coupon]).valid()
    result: CouponApplyResult = sample_product.apply_coupons(coll, quantity=1)

    # expired_coupon은 제외 → fixed_coupon만 적용
    assert result.discount_amount == Decimal("1000")
    assert not result.free_shipping
    assert result.final_price == Decimal("10000") - Decimal("1000") + Decimal("2000")
