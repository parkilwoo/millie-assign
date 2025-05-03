from config import settings
from infrastructure.orm.sql_alchemy.coupon.repository_impl import SQLAlchemyCouponRepository
from infrastructure.orm.sql_alchemy.product.repository_impl import SQLAlchemyProductRepository
from infrastructure.orm.sql_alchemy.session import get_db_session

class RepositoryFactory:
    """
    Repository 구현체 주입을 위한 Class
    """
    def __init__(self):
        if settings.database_orm == "sqlalchemy":
            session = next(get_db_session())
            self._product_repository = SQLAlchemyProductRepository(session=session)
            self._coupon_repository = SQLAlchemyCouponRepository(session=session)
        # TODO 다른 orm 추가
        else:
            raise NotImplementedError("지원하지 않는 Database backend.")
    
    @property
    def product_repository(self):
        return self._product_repository
    
    @property
    def coupon_repository(self):
        return self._coupon_repository