from dataclasses import dataclass, asdict

@dataclass
class CartItem:
    quantity: int
    name: str
    imagepath: str
    price: float #Django sessions can't store Decimal safely

    @staticmethod
    def from_dict(data: dict) -> "CartItem":
        return CartItem(
            quantity = data.get("quantity", 0),
            name = data.get("name",' '),
            imagepath = data.get("imagepath",' '),
            price=float(data.get("price", 0))
        )

    def to_dict(self) -> dict:
        return asdict(self)
