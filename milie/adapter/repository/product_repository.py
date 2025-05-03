from abc import ABC, abstractmethod
from typing import List, Optional

from domain.product.entity import Product

class ProductRepository(ABC):
    """
    상품 입,출력 port 인터페이스
    """
    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def find_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def find_all(self, offset: Optional[int], limit: Optional[int]) -> List[Product]:
        pass

    @abstractmethod
    def associate_coupons(self, product_id: int, coupon_ids: List[int]) -> None:
        """
        product_id와 coupon_ids를 연결하는 메서드
        """