from datetime import datetime
from domain.coupon.entity import Coupon
from adapter.repository.coupon_repository import CouponRepository
from domain.coupon.policy import CouponPolicyFactory
from domain.coupon.value_object import CouponType

class CouponService:
    def __init__(self, repository: CouponRepository):
        self.repository = repository

    def create_coupon(
        self,
        name: str,
        coupon_type: CouponType,
        value: float | None,
        expired_date: datetime,
        usage_limit: int
    ) -> Coupon:
        # 1. 정책 인스턴스 생성
        policy = CouponPolicyFactory.create(coupon_type, value)
        # 2. 도메인 Coupon 생성
        coupon = Coupon(
            name         = name,
            coupon_type  = coupon_type,
            policy       = policy,
            expired_date = expired_date,
            usage_limit  = usage_limit,
        )
        # 3) 저장 & 반환
        return self.repository.save(coupon)
