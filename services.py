import fastapi as _fastapi
import models as _models
import schemas as _schemas
import json

from cache_functions import cache_create, cache_delete, cache_update, cache_get

#import aioredis


def _add_tables():

    return _models.Base.metadata.create_all(bind=_models.engine)


async def get_instances(model: _models, schema: _schemas, **filter):
    name = f"{model.__name__}_list"
    res = await cache_get(name)
    if res:
        return res
    instances = _models.get_instances(model=model, schema=schema, filter=filter)
    await cache_create(name, list(map(dict, instances)))
    print('not from cache')

    return instances


async def get_instance(model: _models, schema: _schemas, **filter):
    name = f"{model.__name__}_{filter['id']}"
    res = await cache_get(name)
    if res:
        return res
    try:
        instance = schema.from_orm(_models.get_instance(model=model, filter=filter))
    except:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"{str(model.__tablename__)} not found"
        )
    await cache_create(name, instance.dict())
    print('not from cache')

    return instance


async def create_menu(menu: _schemas.Common):
    menu = _schemas.Menu.from_orm(_models.add_instance(_models.Menu(**menu.dict())))
    await cache_create(f"Menu_{menu.id}", menu.dict())

    return menu


async def delete_menu(menu: _schemas.Delete, **filter):
    try:
        _models.delete_instance(_models.Menu, filter=filter)
    except:
        raise _fastapi.HTTPException(status_code=404, detail="menu not found")
    menu.status = True
    menu.message = "The menu has been deleted"
    await cache_delete(f"Menu_{filter['id']}")
    return _schemas.Delete.from_orm(menu)


async def update_instance(
    model: _models, schema: _schemas, data: _schemas.Common, **filter
):
    tmp = _models.update_instance(model=model, data=data, filter=filter)
    if not tmp:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"{str(model.__tablename__)} not found"
        )
    await cache_update(f"{model.__name__}_{filter['id']}", data)

    return schema.from_orm(data)


async def create_submenu(submenu: _schemas.Common, **filter):
    submenu = _models.SubMenu(**{**submenu.dict(), **filter})
    _models.count_submenu_and_dishes(filter["menu_id"], 1)
    _models.add_instance(submenu)
    await cache_create(f"SubMenu_{submenu.id}", _schemas.SubMenu.from_orm(submenu).dict())

    return _schemas.SubMenu.from_orm(submenu)


async def delete_submenu(menu: _schemas.Delete, **filter):
    try:
        dishes_count = _models.delete_instance(_models.SubMenu, filter=filter)
    except:
        raise _fastapi.HTTPException(status_code=404, detail="submenu not found")
    _models.count_submenu_and_dishes(filter["menu_id"], -1, dishes_count)
    _models.commit
    menu.status = True
    menu.message = "The submenu has been deleted"
    await cache_delete(f"SubMenu_{filter['id']}")

    return _schemas.Delete.from_orm(menu)


async def create_dish(dish: _schemas.HandleDish, **filter):
    _models.count_submenu_and_dishes(filter["menu_id"], 1, None, filter["submenu_id"])
    del filter["menu_id"]
    dish = _models.Dish(**{**dish.dict(), **filter})
    _models.add_instance(dish)
    await cache_create(f"Dish_{dish.id}", _schemas.Dish.from_orm(dish).dict())

    return _schemas.Dish.from_orm(dish)


async def delete_dish(dish: _schemas.Delete, **filter):
    _models.count_submenu_and_dishes(filter["menu_id"], -1, None, filter["submenu_id"])
    del filter["menu_id"]
    try:
        _models.delete_instance(_models.Dish, filter=filter)
    except:
        _models.rollback()
        raise _fastapi.HTTPException(status_code=404, detail="dish not found")
    dish.status = True
    dish.message = "The dish has been deleted"
    await cache_delete(f"Dish_{filter['id']}")

    return _schemas.Delete.from_orm(dish)
