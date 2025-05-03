from application.coupon.coupon_service import CouponService
from application.product.product_service import ProductService
from factory.repository_factory import RepositoryFactory

class ServiceFactory:
    """
    Service Layer 주입을 위한 Class
    """
    def __init__(self):
        self.repository = RepositoryFactory()
    
    def get_product_service(self) -> ProductService:
        return ProductService(product_repository=self.repository.product_repository, coupon_repository=self.repository.coupon_repository)
    
    def get_coupon_service(self) -> CouponService:
        return CouponService(repository=self.repository.coupon_repository)
    
service_factory = ServiceFactory()