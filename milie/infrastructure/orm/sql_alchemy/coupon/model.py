from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from domain.coupon.value_object import CouponType
from infrastructure.orm.sql_alchemy.base import Base

class CouponModel(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(SqlEnum(CouponType), nullable=False)
    value = Column(Numeric(10, 2), nullable=True) # 금액 및 비율 할인등에 사용될 값, 1+1같은건 Null
    expired_date = Column(DateTime, nullable=False)
    usage_limit   = Column(Integer, nullable=False, default=1)

    products = relationship(
        "ProductModel",
        secondary="product_coupons",
        back_populates="coupons"
    )

class ProductCouponAssociation(Base):
    __tablename__ = "product_coupons"

    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), primary_key=True)