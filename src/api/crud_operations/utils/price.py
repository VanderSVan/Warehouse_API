from typing import NoReturn

from src.api.models.price import PriceModel
from src.api.schemas.price.base_schemas import (PricePatchSchema,
                                                PricePostSchema)
from src.api.crud_operations.utils.warehouse_group import check_warehouse_group_existence
from src.api.crud_operations.utils.product import check_product_existence
from src.utils.exceptions.base import CRUDException


def check_input_price_data_for_patch(func):
    async def wrapper(
            self,
            new_data: PricePatchSchema | PricePostSchema,
            id_: int,
            *args,
            **kwargs
    ):
        """
        Checks input data for patch `price` object.
        """
        old_obj: PriceModel = await self.find_by_id_or_404(id_)
        old_data: PricePatchSchema = PricePatchSchema(**old_obj.__dict__)
        data_to_update: dict = new_data.dict(exclude_unset=True)
        merged_data: PricePatchSchema = old_data.copy(update=data_to_update)

        await check_product_existence(merged_data.product_id, self.db)
        await check_warehouse_group_existence(merged_data.warehouse_id, self.db)
        await _check_price_duplicate(self, merged_data)

        return await func(self, new_data, id_, *args, **kwargs)

    return wrapper


def check_input_price_data_for_post(func):
    async def wrapper(
            self,
            new_data: PricePatchSchema | PricePostSchema,
            *args,
            **kwargs
    ):
        """
        Checks input data for post `price` object.
        """
        await check_product_existence(new_data.product_id, self.db)
        await check_warehouse_group_existence(new_data.warehouse_id, self.db)
        await _check_price_duplicate(self, new_data)

        return await func(self, new_data, *args, **kwargs)

    return wrapper


async def _check_price_duplicate(
        self,
        new_data: PricePatchSchema | PricePostSchema
) -> NoReturn:
    """
    Searches for existing data, if found then raise an exception.
    """
    duplicate: PriceModel | None = await self.find_all_by_params(
        from_dt=new_data.datetime,
        to_dt=new_data.datetime,
        product_id=new_data.product_id,
        warehouse_id=new_data.warehouse_id
    )
    if duplicate:
        CRUDException.raise_duplicate_err(self.model_name)
