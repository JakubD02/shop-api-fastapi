from enum import Enum

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    BOOKS = "books"
    CLOTHING = "clothing"
    FOOD = "food"
    SPORT = "sport"
    TOOLS = "tools"
    OTHER = "other"
