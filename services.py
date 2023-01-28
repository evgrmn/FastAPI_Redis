import fastapi as _fastapi
import models as _models
import schemas as _schemas


def _add_tables():

    return _models.Base.metadata.create_all(bind=_models.engine)


async def get_instances(model: _models, schema: _schemas, **filter):
    instances = _models.get_instances(model=model, schema=schema, filter=filter)

    return instances


async def get_instance(model: _models, schema: _schemas, **filter):
    try:
        substance = _models.get_instance(model=model, filter=filter)
    except:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"{str(model.__tablename__)} not found"
        )

    return schema.from_orm(substance)


async def create_menu(menu: _schemas.Common):
    menu = _models.add_instance(_models.Menu(**menu.dict()))

    return _schemas.Menu.from_orm(menu)


async def delete_menu(menu: _schemas.Delete, **filter):
    try:
        _models.delete_instance(_models.Menu, filter=filter)
    except:
        raise _fastapi.HTTPException(status_code=404, detail="menu not found")
    menu.status = True
    menu.message = "The menu has been deleted"
    return _schemas.Delete.from_orm(menu)


async def update_instance(
    model: _models, schema: _schemas, data: _schemas.Common, **filter
):
    tmp = _models.update_instance(model=model, data=data, filter=filter)
    if not tmp:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"{str(model.__tablename__)} not found"
        )

    return schema.from_orm(data)


async def create_submenu(submenu: _schemas.Common, **filter):
    submenu = _models.SubMenu(**{**submenu.dict(), **filter})
    _models.count_submenu_and_dishes(filter["menu_id"], 1)
    _models.add_instance(submenu)

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

    return _schemas.Delete.from_orm(menu)


async def create_dish(dish: _schemas.HandleDish, **filter):
    _models.count_submenu_and_dishes(filter["menu_id"], 1, None, filter["submenu_id"])
    del filter["menu_id"]
    dish = _models.Dish(**{**dish.dict(), **filter})
    _models.add_instance(dish)

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

    return _schemas.Delete.from_orm(dish)
