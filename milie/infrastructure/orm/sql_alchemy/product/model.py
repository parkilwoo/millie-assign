from sqlalchemy import Column, Integer, String, Numeric, Enum as SqlEnum
from domain.product.discount_policy import DiscountPolicyType
from infrastructure.orm.sql_alchemy.base import Base
from sqlalchemy.orm import relationship

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    shipping_fee = Column(Numeric(10,2), nullable=False, default=0)
    discount_policy_type = Column(SqlEnum(DiscountPolicyType), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=True)

    coupons = relationship(
        "CouponModel",
        secondary="product_coupons",
        back_populates="products",
        lazy="select"
    )