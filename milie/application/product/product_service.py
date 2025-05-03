from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from adapter.repository.coupon_repository import CouponRepository
from adapter.repository.product_repository import ProductRepository
from domain.coupon.collection import Coupons
from domain.product.discount_policy import DiscountPolicyFactory, DiscountPolicyType
from domain.product.entity import Product
from domain.product.value_object import PriceResult


class ProductService:
    """
    Facade 패턴
    """
    def __init__(self, product_repository: ProductRepository, coupon_repository: CouponRepository):
        self.product_repository = product_repository
        self.coupon_repository = coupon_repository

    def create_product(
        self,
        name: str,
        base_price: Decimal,
        shipping_fee: Decimal,
        policy_type: DiscountPolicyType,
        value: Optional[Decimal]
    ) -> Product:
        policy = DiscountPolicyFactory.create(policy_type=policy_type, value=value)
        product = Product(
            name=name,
            base_price=base_price,
            shipping_fee=shipping_fee,
            discount_policy=policy
        )
        return self.product_repository.save(product=product)

    def get_all_products(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Product]:
        return self.product_repository.find_all(offset=offset, limit=limit)
    
    def get_product_with_available_coupons(self, product_id: int) -> Tuple[Product, Coupons]:
        product = self.product_repository.find_by_id(product_id)
        coupons = self.coupon_repository.find_valid_by_product_id(
            product_id, datetime.now()
        )
        return product, coupons

    def calculate_price(
        self,
        product_id: int,
        coupon_ids:  List[int],
        quantity:    int,
    ) -> PriceResult:
        # 1. 상품 조회
        product = self.product_repository.find_by_id(product_id)

        # 2. 쿠폰 조회 & 만료 필터링
        coupons = self.coupon_repository.find_by_ids(coupon_ids)
        valid_coupons = coupons.valid(datetime.now())

        # 3. 상품 엔티티에 계산 위임
        return product.calculate_price_with_coupons(valid_coupons, quantity)

    def attach_coupons(self, product_id: int, coupon_ids: List[int]) -> List[int]:
        # 1. 상품 존재 확인
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")

        # 2. 쿠폰 일괄 조회 및 유효성 검사
        coupons = self.coupon_repository.find_by_ids(coupon_ids)
        if len(coupons) != len(coupon_ids):
            raise ValueError("Not valid coupon detected")

        # 3. 연관관계 저장
        self.product_repository.associate_coupons(product_id, coupon_ids)

        # 4. 연관된 coupon_ids 반환
        return coupon_ids