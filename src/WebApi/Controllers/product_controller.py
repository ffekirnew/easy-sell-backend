from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Path
from pydantic import BaseModel

from Application.Contracts.iproduct_service import ProductServiceInterface
from Application.UseCases.DTOs.Product.create_product_dto import \
    CreateProductDto
from Application.UseCases.DTOs.Product.product_dto import ProductDto
from Application.UseCases.Services.product_service import ProductService
from Persistence.Repositories.product_repository import ProductRepository

product_repository = ProductRepository([])
product_service: ProductServiceInterface = ProductService(product_repository)


router = APIRouter()


class ProductCreate(BaseModel):
    name: str
    price: int
    description: str
    image: str
    categories: list
    quantity: int
    createdAt: str
    userTelegramId: str


@router.get("/products", response_model=list[ProductDto])
def list_products():
    products = product_service.list()
    return products


@router.post("/products", response_model=str)
def create_product(product_data: ProductCreate):
    product = CreateProductDto(**product_data.dict())
    product_id = product_service.add(product)
    return {"message": "Product created", "product_id": str(product_id)}


@router.get("/products/{product_id}", response_model=ProductDto)
def get_product(product_id: ObjectId = Path(..., title="The product ID")):
    product = product_service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=str)
def update_product(
    product_id: ObjectId = Path(..., title="The product ID"),
    product_data: ProductCreate = Body(..., title="Updated product data"),
):
    product = CreateProductDto(**product_data.dict())
    product_service.update(product_id, product)
    return {"message": "Product updated successfully"}


@router.delete("/products/{product_id}", response_model=str)
def delete_product(product_id: ObjectId = Path(..., title="The product ID")):
    product_service.delete(product_id)
    return {"message": "Product deleted successfully"}
