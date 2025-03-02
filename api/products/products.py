from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductPublic,
    SavedProductCreate,
    SavedProductPublic
)
from ..services.products import ProductCrud
from ..users.users import current_active_user
from db.models import User, SavedProduct

router = APIRouter()


@router.post("/", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, product_crud: ProductCrud = Depends(ProductCrud)):
    client = await product_crud.create_product(product_data)
    return client


@router.get("/", response_model=list[ProductPublic])
async def get_products(
    offset: int = 0, limit: int = 10, product_crud: ProductCrud = Depends(ProductCrud)
):
    products = await product_crud.get_products(offset=offset, limit=limit)
    return products


@router.get('/saved-list')
async def get_saved_products(
    user: User = Depends(current_active_user),
    product_crud: ProductCrud = Depends(ProductCrud)
):
    return await product_crud.get_saved_products(user_id=user.id)


@router.delete('/{product_id}/saved-list', status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_product(
    product_id: int,
    user: User = Depends(current_active_user),
    product_crud: ProductCrud = Depends(ProductCrud),
):
    deleted_product = await product_crud.delete_saved_product(user_id=user.id, product_id=product_id)
    if not deleted_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Saved Product not found"
        )
    return


@router.get("/{product_id}", response_model=ProductPublic)
async def get_product(product_id: int, product_crud: ProductCrud = Depends(ProductCrud)):
    product = await product_crud.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, product_crud: ProductCrud = Depends(ProductCrud)):
    deleted_product = await product_crud.delete_product(product_id)
    if not deleted_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return


@router.post("/saved-list")
async def save_product(
    saved_product_data: SavedProductCreate,
    user: User = Depends(current_active_user),
    product_crud: ProductCrud = Depends(ProductCrud),
):
    return await product_crud.save_product(user_id=user.id, product_id=saved_product_data.product_id)
