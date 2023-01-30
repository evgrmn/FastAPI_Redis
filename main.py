from typing import List
import fastapi as _fastapi
import schemas as _schemas
import services as _services
from fastapi import Path
import description
import models as _models


app = _fastapi.FastAPI(title="FastAPI Application", description=description.description)


_services._add_tables()


@app.get("/api/v1/menus", response_model=List[_schemas.Menu], summary="Get menu list")
async def get_menus():

    return await _services.get_instances(model=_models.Menu, schema=_schemas.Menu)


@app.post(
    "/api/v1/menus",
    response_model=_schemas.Menu,
    status_code=201,
    summary="Create a new menu",
)
async def create_menu(
    menu: _schemas.Common,
):

    return await _services.create_menu(menu=menu)


@app.delete(
    "/api/v1/menus/{menu_id}", response_model=_schemas.Delete, summary="Delete menu"
)
async def delete_menu(
    menu_id: int = Path(),
):

    return await _services.delete_menu(menu=_schemas.Delete, id=menu_id)


@app.get("/api/v1/menus/{menu_id}", response_model=_schemas.Menu, summary="Get menu")
async def get_menu(
    menu_id: int = Path(),
):

    return await _services.get_instance(
        model=_models.Menu, schema=_schemas.Menu, id=menu_id
    )


@app.patch(
    "/api/v1/menus/{menu_id}", response_model=_schemas.Common, summary="Update menu"
)
async def update_menu(
    data: _schemas.Common,
    menu_id: int = Path(),
):

    return await _services.update_instance(
        model=_models.Menu, schema=_schemas.Common, data=data, id=menu_id
    )


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=_schemas.SubMenu,
    status_code=201,
    summary="Create a new submenu",
)
async def create_submenu(
    submenu: _schemas.Common,
    menu_id: int = Path(),
):

    return await _services.create_submenu(submenu=submenu, menu_id=menu_id)


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=_schemas.Delete,
    summary="Delete submenu",
)
async def delete_submenu(
    menu_id: int = Path(),
    submenu_id: int = Path(),
):

    return await _services.delete_submenu(
        menu=_schemas.Delete, menu_id=menu_id, id=submenu_id
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=List[_schemas.SubMenu],
    summary="Get submenu list",
)
async def get_submenus(
    menu_id: int = Path(),
):

    return await _services.get_instances(
        model=_models.SubMenu, schema=_schemas.SubMenu, menu_id=menu_id
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=_schemas.SubMenu,
    summary="Get submenu",
)
async def get_submenu(
    menu_id: int = Path(),
    submenu_id: int = Path(),
):

    return await _services.get_instance(
        model=_models.SubMenu, schema=_schemas.SubMenu, id=submenu_id, menu_id=menu_id
    )


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=_schemas.Common,
    summary="Update submenu",
)
async def update_submenu(
    data: _schemas.Common,
    menu_id: int = Path(),
    submenu_id: int = Path(),
):

    return await _services.update_instance(
        model=_models.SubMenu, schema=_schemas.Common, data=data, id=submenu_id
    )


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=_schemas.Dish,
    status_code=201,
    summary="Create a new dish",
)
async def create_dish(
    dish: _schemas.HandleDish,
    menu_id: int = Path(),
    submenu_id: int = Path(),
):

    return await _services.create_dish(
        dish=dish, menu_id=menu_id, submenu_id=submenu_id
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[_schemas.Dish],
    summary="Get dish list",
)
async def get_dishes(
    menu_id: int = Path(),
    submenu_id: int = Path(),
):

    return await _services.get_instances(
        model=_models.Dish, schema=_schemas.Dish, submenu_id=submenu_id
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=_schemas.Dish,
    summary="Get dish",
)
async def get_dish(
    menu_id: int = Path(),
    submenu_id: int = Path(),
    dish_id: int = Path(),
):

    return await _services.get_instance(
        model=_models.Dish, schema=_schemas.Dish, id=dish_id, submenu_id=submenu_id
    )


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=_schemas.Delete,
    summary="Delete dish",
)
async def delete_dish(
    menu_id: int = Path(),
    submenu_id: int = Path(),
    dish_id: int = Path(),
):

    return await _services.delete_dish(
        dish=_schemas.Delete, id=dish_id, menu_id=menu_id, submenu_id=submenu_id
    )


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=_schemas.HandleDish,
    summary="Update dish",
)
async def update_dish(
    data: _schemas.HandleDish,
    menu_id: int = Path(),
    submenu_id: int = Path(),
    dish_id: int = Path(),
):

    return await _services.update_instance(
        model=_models.Dish,
        schema=_schemas.HandleDish,
        data=data,
        id=dish_id,
        submenu_id=submenu_id,
    )
