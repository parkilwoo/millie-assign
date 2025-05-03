from typing import List
from fastapi import APIRouter, Depends, Path, Query
from application.product.product_service import ProductService
from factory.service_factory import service_factory
from api.v1.schema import ApplyCouponResponse, CouponAssignRequest, CouponAssignResponse, CouponSummary, ProductCreateRequest, ProductDetailResponse, ProductListResponse, ProductSummary

router = APIRouter(tags=["Product"])

@router.post("/products", response_model=ProductSummary, status_code=201)
async def create_product(
    req: ProductCreateRequest,
    service: ProductService = Depends(service_factory.get_product_service)
):
    product = service.create_product(
        name=req.name,
        base_price=req.base_price,
        shipping_fee=req.shipping_fee,
        policy_type=req.discount_policy_type,
        value=req.discount_value
    )

    return ProductSummary(
        product_id=product.product_id,
        name=product.name,
        base_price=product.base_price,
        shipping_fee=product.shipping_fee,
        discount_policy_type=product.discount_policy.get_type_and_value()[0]
    )

@router.get("/products", response_model=ProductListResponse)
async def list_products(
    offset: int = Query(default=None, ge=0),
    limit: int = Query(default=None, ge=1),
    service: ProductService = Depends(service_factory.get_product_service)
):
    products = service.get_all_products(offset=offset, limit=limit)

    return ProductListResponse(
        products=[
            ProductSummary(
                product_id=p.product_id,
                name=p.name,
                base_price=p.base_price,
                shipping_fee=p.shipping_fee,
                discount_policy_type=p.discount_policy.get_type_and_value()[0]
            )
            for p in products
        ]
    )


@router.get("/products/{product_id}", response_model=ProductDetailResponse)
async def get_product_detail(
    product_id: int,
    service: ProductService = Depends(service_factory.get_product_service)
):
    product, coupons = service.get_product_with_available_coupons(product_id)

    return ProductDetailResponse(
        product=ProductSummary(
            product_id=product.product_id,
            name=product.name,
            base_price=product.base_price,
            shipping_fee=product.shipping_fee,
            discount_policy_type=product.discount_policy.get_type_and_value()[0]
        ),
        available_coupons=[
            CouponSummary(
                coupon_id=c.coupon_id,
                name=c.name,
                type=c.coupon_type,
                expired_date=c.expired_date
            )
            for c in coupons.all()
        ]
    )

@router.get("/products/{product_id}/price", response_model=ApplyCouponResponse)
async def calulate_price(
    product_id: int = Path(..., description="대상 상품 ID"),
    coupon_ids: List[int] = Query(..., description="적용할 쿠폰 ID들", example=[1, 2, 3]),
    quantity: int = Query(default=1, ge=1),
    service: ProductService = Depends(service_factory.get_product_service)
):
    result = service.calculate_price(
        product_id = product_id,
        coupon_ids = coupon_ids,
        quantity   = quantity,
    )
    return ApplyCouponResponse(
        original_price=result.original_price,
        total_discount_amount=result.total_discount,
        final_price=result.final_price,
        free_shipping=result.free_shipping,
        shipping_fee=result.shipping_fee,
        bonus_quantity=result.bonus_quantity
    )


@router.post("/products/{product_id}/coupons", response_model=CouponAssignResponse, status_code=201)
async def assign_coupons(
    product_id: int,
    req: CouponAssignRequest
):
    assigned = service_factory.get_product_service().attach_coupons(
        product_id, req.coupon_ids
    )
    return CouponAssignResponse(product_id=product_id, coupon_ids=assigned)