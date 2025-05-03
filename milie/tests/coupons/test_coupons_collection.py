import pytest
from domain.coupon.collection import Coupons

def test_valid_filters_out_expired(fixed_coupon, expired_coupon):
    """
    Coupons.valid()가 만료된 쿠폰을 걸러내는지 확인
    """
    all_coupons = Coupons([fixed_coupon, expired_coupon])
    valid = list(all_coupons.valid())
    assert valid == [fixed_coupon]

def test_iteration_over_coupons(fixed_coupon, free_ship_coupon):
    """
    Coupons를 순회(iter)할 수 있는지 확인
    """
    coll = Coupons([fixed_coupon, free_ship_coupon])
    policies = [c.policy for c in coll]
    assert policies == [fixed_coupon.policy, free_ship_coupon.policy]
