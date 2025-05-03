
import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from domain.product.entity import Product
from domain.coupon.entity import Coupon
from domain.coupon.policy import FixedDiscountCoupon, FreeShippingCoupon
from domain.coupon.value_object import CouponType

@pytest.fixture
def sample_product():
    """
    price=10,000원, discount_rate=0%, shipping_fee=2,000원인 테스트용 Product
    """
    return Product(
        name="테스트상품",
        price=Decimal("10000"),
        discount_rate=Decimal("0"),
        shipping_fee=Decimal("2000"),
    )


@pytest.fixture
def fixed_coupon():
    """
    1,000원 고정 할인, 만료일이 내일인 Coupon
    """
    return Coupon(
        name="FIXED_1000",
        coupon_type=CouponType.FIXED,
        policy=FixedDiscountCoupon(amount=Decimal("1000")),
        expired_date=datetime.utcnow() + timedelta(days=1),
    )

@pytest.fixture
def free_ship_coupon():
    """
    무료 배송 쿠폰, 만료일이 내일인 Coupon
    """
    return Coupon(
        name="FREE_SHIP",
        coupon_type=CouponType.FREE_SHIPPING,
        policy=FreeShippingCoupon(),
        expired_date=datetime.utcnow() + timedelta(days=1),
    )


@pytest.fixture
def expired_coupon():
    """
    이미 만료된 Coupon
    """
    return Coupon(
        name="EXPIRED_500",
        coupon_type=CouponType.FIXED,
        policy=FixedDiscountCoupon(amount=Decimal("500")),
        expired_date=datetime.utcnow() - timedelta(days=1),
    )