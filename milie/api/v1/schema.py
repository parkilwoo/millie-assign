from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from decimal import Decimal
from enum import Enum

from domain.coupon.value_object import CouponType

class DiscountPolicyType(str, Enum):
    """
    할인 정책 타입
    """
    NONE = "NONE"
    RATE = "RATE"
    AMOUNT = "AMOUNT"

class ProductCreateRequest(BaseModel):
    """
    상품 생성 API 요청 DTO
    """
    name: str = Field(..., example="Millie's library")
    base_price: Decimal = Field(..., example=10000)
    shipping_fee: Decimal = Field(..., example=2500)
    discount_policy_type: DiscountPolicyType = Field(..., example="RATE")
    discount_value: Decimal = Field(..., example=0.1)

class ProductSummary(BaseModel):
    product_id: int
    name: str
    base_price: Decimal
    shipping_fee: Decimal
    discount_policy_type: DiscountPolicyType

class ProductListResponse(BaseModel):
    products: List[ProductSummary]

class CouponSummary(BaseModel):
    coupon_id: int
    name: str
    type: CouponType
    expired_date: datetime

class ProductDetailResponse(BaseModel):
    product: ProductSummary
    available_coupons: List[CouponSummary]

class ApplyCouponRequest(BaseModel):
    product_id: int
    coupon_ids: List[int] = Field(..., example=[1, 2])
    quantity: int = Field(default=1, ge=1)

class ApplyCouponResponse(BaseModel):
    original_price: Decimal
    total_discount_amount: Decimal
    final_price: Decimal
    free_shipping: bool
    shipping_fee: Decimal
    bonus_quantity: int

class CouponCreateRequest(BaseModel):
    name: str = Field(..., example="10% 할인 쿠폰")
    type: CouponType = Field(..., example=CouponType.RATE_DISCOUNT)
    value: Optional[Decimal] = Field(None, example=Decimal("0.1"))
    expired_date: datetime = Field(..., example="2025-12-31T23:59:59")
    usage_limit: int = Field(1, ge=1, example=1)

    @validator("value", always=True)
    def check_value_for_type(cls, v, values):
        t = values.get("type")
        if t in (CouponType.FIXED_DISCOUNT, CouponType.RATE_DISCOUNT):
            if v is None:
                raise ValueError("금액/비율 할인 쿠폰에는 value를 꼭 지정해야 합니다.")
        else:
            if v is not None:
                raise ValueError("무료배송·1+1 쿠폰은 value가 없어야 합니다.")
        if t == CouponType.RATE_DISCOUNT and v is not None and not (Decimal("0") < v <= Decimal("1")):
            raise ValueError("비율 쿠폰의 value는 0~1 사이값만 가능합니다.")
        return v

    @validator("expired_date")
    def check_future_date(cls, v):
        if v <= datetime.now():
            raise ValueError("expired_date는 미래 시간을 지정해야 합니다.")
        return v

class CouponResponse(BaseModel):
    coupon_id: int
    name: str
    type: CouponType
    value: Optional[Decimal]
    expired_date: datetime
    usage_limit: int


class CouponAssignRequest(BaseModel):
    coupon_ids: List[int]

class CouponAssignResponse(BaseModel):
    product_id: int
    coupon_ids: List[int]
