from datetime import datetime
from decimal import Decimal

from domain.coupon.value_object import CouponApplyResult

def test_is_expired(expired_coupon, fixed_coupon):
    # expired_coupon 은 yesterday → expired=True
    assert expired_coupon.is_expired(datetime.utcnow()) is True
    # fixed_coupon 은 tomorrow → expired=False
    assert fixed_coupon.is_expired(datetime.utcnow()) is False

def test_fixed_coupon_policy_via_entity(fixed_coupon, sample_product):
    """
    Coupon.policy.apply 을 직접 호출해서 기대하는 결과가 나오는지 확인
    """
    result: CouponApplyResult = fixed_coupon.policy.apply(
        unit_price=sample_product.unit_price,
        quantity=2,
        shipping_fee=sample_product.shipping_fee
    )
    assert isinstance(result, CouponApplyResult)
    assert result.discount_amount == Decimal("1000")
    assert not result.free_shipping
    assert result.final_price == sample_product.unit_price * 2 - Decimal("1000") + sample_product.shipping_fee

def test_free_shipping_coupon_policy(free_ship_coupon, sample_product):
    res: CouponApplyResult = free_ship_coupon.policy.apply(
        unit_price=sample_product.unit_price,
        quantity=3,
        shipping_fee=sample_product.shipping_fee
    )
    assert res.free_shipping is True
    assert res.discount_amount == Decimal("0")
    assert res.final_price == sample_product.unit_price * 3
