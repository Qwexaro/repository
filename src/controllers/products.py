from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/products", tags=["products"])

products = [
    {
        "name": "Рис с колбасками",
        "category": "Блюда с рисом",
        "price": "102",
        "weight": "23kg"
    },
    {
        "name": "Торт бенгальский",
        "category": "Десерты",
        "price": "67",
        "weight": "23kg"
    },
    {
        "name": "Сникерс торт",
        "category": "Десерты",
        "price": "75",
        "weight": "28kg"
    },
    {
        "name": "Креветки",
        "category": "Морепродукты",
        "price": "67",
        "weight": "23kg"
    },
    {
        "name": "Оливье",
        "category": "Салаты",
        "price": "88",
        "weight": "13kg"
    },
    {
        "name": "Роллы запеченные",
        "category": "Блюда с рисом",
        "price": "167",
        "weight": "99kg"
    },
    {
        "name": "Торт наполеон",
        "category": "Десерты",
        "price": "37",
        "weight": "53kg"
    }
]


# Получить список всех продуктов с возможностью сортировки
@router.get("/")
async def get_products(sorting: str = None):
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


# Получить продукты по категории с возможностью сортировки
@router.get("/category/{category_name}")
async def get_products_by_category(category_name: str, sorting: str = None):
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


# Удалить продукт по имени
@router.delete("/{product_name}")
async def delete_product(product_name: str):
    # Ищем продукт по имени (регистронезависимый поиск)
    for i, product in enumerate(products):
        if product["name"].lower() == product_name.lower():
            deleted_product = products.pop(i)
            return {
                "message": f"Продукт '{deleted_product['name']}' успешно удален",
                "deleted_product": deleted_product
            }

    # Если продукт не найден
    raise HTTPException(
        status_code=404,
        detail=f"Продукт '{product_name}' не найден"
    )


# Альтернативный вариант удаления по индексу (если нужно)
@router.delete("/by-index/{product_index}")
async def delete_product_by_index(product_index: int):
    if product_index < 0 or product_index >= len(products):
        raise HTTPException(
            status_code=404,
            detail=f"Продукт с индексом {product_index} не найден"
        )

    deleted_product = products.pop(product_index)
    return {
        "message": f"Продукт '{deleted_product['name']}' успешно удален",
        "deleted_product": deleted_product
    }