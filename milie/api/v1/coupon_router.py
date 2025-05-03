from fastapi import APIRouter, Depends
from api.v1.schema import CouponCreateRequest, CouponResponse
from application.coupon.coupon_service import CouponService
from factory.service_factory import service_factory

router = APIRouter(tags=["coupon"])

@router.post(
    "/coupons",
    response_model=CouponResponse,
)
async def create_coupon(
    req: CouponCreateRequest,
    service: CouponService = Depends(service_factory.get_coupon_service)
):
    coupon = service.create_coupon(
        name         = req.name,
        coupon_type  = req.type,
        value        = req.value,
        expired_date = req.expired_date,
        usage_limit  = req.usage_limit,
    )
    return CouponResponse(
        coupon_id    = coupon.coupon_id,
        name         = coupon.name,
        type         = coupon.coupon_type,
        value        = getattr(coupon.policy, "amount", None) or getattr(coupon.policy, "rate", None),
        expired_date = coupon.expired_date,
        usage_limit  = coupon.usage_limit,
    )
