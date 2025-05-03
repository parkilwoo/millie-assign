from typing import List
from sqlalchemy.orm import Session
from adapter.repository.product_repository import ProductRepository
from domain.product.discount_policy import DiscountPolicyFactory
from domain.product.entity import Product
from infrastructure.orm.sql_alchemy.product.model import ProductModel
from infrastructure.orm.sql_alchemy.coupon.model import ProductCouponAssociation

class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, product):
        policy_type, value = product.discount_policy.get_type_and_value()

        model = ProductModel(
            name=product.name,
            base_price=product.base_price,
            shipping_fee=product.shipping_fee,
            discount_policy_type=policy_type,
            discount_value=value
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        product._set_product_id(product_id=model.id)
        return product
    
    def find_by_id(self, product_id: int) -> Product:
        model = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not model:
            raise ValueError(f"Product not found: {product_id}")

        return self._to_entity(model=model)

    
    def find_all(self, offset, limit) -> List[Product]:
        query = self.session.query(ProductModel)
        if offset:
            query = query.offset(offset=offset)
        if limit:
            query = query.limit(limit=limit)
        return [self._to_entity(row) for row in query.all()]
    
    def associate_coupons(self, product_id: int, coupon_ids: List[int]):
        for cid in coupon_ids:
            assoc = ProductCouponAssociation(
                product_id=product_id,
                coupon_id=cid
            )
            self.session.add(assoc)
        self.session.commit()
    
    def _to_entity(self, model: ProductModel) -> Product:
        # 1. 할인 정책 복원
        policy = DiscountPolicyFactory.create(
            model.discount_policy_type,
            model.discount_value
        )
        # 2. Product 도메인 엔티티 생성 (shipping_fee 포함)
        product = Product(
            name            = model.name,
            base_price      = model.base_price,
            shipping_fee    = model.shipping_fee,
            discount_policy = policy
        )
        product._set_product_id(model.id)
        return product