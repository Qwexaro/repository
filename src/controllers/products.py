import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/products", tags=["products"])

PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), "products.json")

def load_products():
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        save_products([])
        return []
    except json.JSONDecodeError:
        save_products([])
        return []

def save_products(products):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

@router.get("/")
async def get_products(sorting: str = None):
    products = load_products()
    products_list = products.copy()

    if sorting:
        if sorting.lower() == "asc":
            products_list.sort(key=lambda x: x["name"].lower())
        elif sorting.lower() == "desc":
            products_list.sort(key=lambda x: x["name"].lower(), reverse=True)
        else:
            raise HTTPException(
                status_code=400,
                detail="Параметр sorting должен быть 'asc' или 'desc'"
            )

    return {
        "products": products_list,
        "total": len(products_list),
        "sorting": sorting if sorting else "not applied"
    }

@router.get("/category/{category_name}")
async def get_products_by_category(category_name: str, sorting: str = None):
    products = load_products()

    filtered_products = [
        product for product in products
        if product["category"].lower() == category_name.lower()
    ]

    if not filtered_products:
        raise HTTPException(
            status_code=404,
            detail=f"Продукты в категории '{category_name}' не найдены"
        )

    products_list = filtered_products.copy()

    if sorting:
        if sorting.lower() == "asc":
            products_list.sort(key=lambda x: x["name"].lower())
        elif sorting.lower() == "desc":
            products_list.sort(key=lambda x: x["name"].lower(), reverse=True)
        else:
            raise HTTPException(
                status_code=400,
                detail="Параметр sorting должен быть 'asc' или 'desc'"
            )

    return {
        "category": category_name,
        "products": products_list,
        "total": len(products_list),
        "sorting": sorting if sorting else "not applied"
    }

@router.delete("/{product_name}")
async def delete_product(product_name: str):
    products = load_products()

    for i, product in enumerate(products):
        if product["name"].lower() == product_name.lower():
            deleted_product = products.pop(i)
            save_products(products)
            return {
                "message": f"Продукт '{deleted_product['name']}' успешно удален",
                "deleted_product": deleted_product
            }

    raise HTTPException(
        status_code=404,
        detail=f"Продукт '{product_name}' не найден"
    )

@router.post("/")
async def create_product(product: dict):
    products = load_products()

    for existing_product in products:
        if existing_product["name"].lower() == product["name"].lower():
            raise HTTPException(
                status_code=400,
                detail=f"Продукт '{product['name']}' уже существует"
            )

    products.append(product)
    save_products(products)

    return {
        "message": f"Продукт '{product['name']}' успешно добавлен",
        "product": product
    }