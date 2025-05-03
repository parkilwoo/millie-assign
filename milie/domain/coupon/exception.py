"""
쿠폰 적용 예외처리
"""
EXPIRED_MSG = "쿠폰 유효기간이 만료 되었습니다."

class CouponApplyException(Exception):
    pass

class InvalidDiscountAmount(CouponApplyException):
    """
    비정상적인 할인율
    """
    pass

class ExpiredCouponException(CouponApplyException):
    """
    기간이 만료된 쿠폰 사용
    """
    def __init__(self):
        super().__init__(EXPIRED_MSG)