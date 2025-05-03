from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class PriceResult:
    original_price:      Decimal
    total_discount:      Decimal
    final_price:         Decimal
    free_shipping:       bool
    shipping_fee:        Decimal
    bonus_quantity:      int