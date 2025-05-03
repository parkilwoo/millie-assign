from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from adapter.repository.coupon_repository import CouponRepository
from domain.coupon.collection import Coupons
from infrastructure.orm.sql_alchemy.coupon.model import CouponModel, ProductCouponAssociation
from domain.coupon.policy import CouponPolicyFactory
from domain.coupon.entity import Coupon

class SQLAlchemyCouponRepository(CouponRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, coupon: Coupon) -> Coupon:
        model = CouponModel(
            name         = coupon.name,
            type         = coupon.coupon_type,
            value        = getattr(coupon.policy, "amount", None) or getattr(coupon.policy, "rate", None),
            expired_date = coupon.expired_date,
            usage_limit  = coupon.usage_limit,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        # 도메인 엔티티에 ID 채워주기
        coupon._set_coupon_id(model.id)
        return coupon        

    def find_by_ids(self, ids: List[int]):
        models = (
            self.session
                .query(CouponModel)
                .filter(CouponModel.id.in_(ids))
                .all()
        )
        entities = [self._to_entity(model) for model in models ]
        return Coupons(items=entities)

    def find_valid_by_product_id(self, product_id: int, now: datetime):
        models = (
            self.session
                .query(CouponModel)
                .join(ProductCouponAssociation)
                .filter(
                    ProductCouponAssociation.product_id == product_id,
                    CouponModel.expired_date >= now
                )
                .all()
        )
        entities = [self._to_entity(model) for model in models ]
        return Coupons(items=entities)

    def _to_entity(self, model: CouponModel) -> Coupon:
        policy = CouponPolicyFactory.create(model.type, model.value)
        coupon = Coupon(
            name         = model.name,
            coupon_type  = model.type,
            policy       = policy,
            expired_date = model.expired_date,
            usage_limit  = model.usage_limit,
        )
        coupon._set_coupon_id(model.id)
        return coupon