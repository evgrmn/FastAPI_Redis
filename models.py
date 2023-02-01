from __future__ import annotations

import fastapi as _fastapi
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

from config import Config

DATABASE_URL = Config.DB_URL
engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base: _declarative = _declarative.declarative_base()


class Menu(Base):
    __tablename__ = 'menu'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    submenus_count = _sql.Column(_sql.Integer, default=0)
    dishes_count = _sql.Column(_sql.Integer, default=0)

    children = _orm.relationship(
        'SubMenu',
        cascade='all,delete',
        backref='parent',
    )


class SubMenu(Base):
    __tablename__ = 'submenu'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    menu_id = _sql.Column(_sql.Integer, _sql.ForeignKey('menu.id'))
    dishes_count = _sql.Column(_sql.Integer, default=0)

    children = _orm.relationship(
        'Dish',
        cascade='all,delete',
        backref='parent',
    )


class Dish(Base):
    __tablename__ = 'dish'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    submenu_id = _sql.Column(_sql.Integer, _sql.ForeignKey('submenu.id'))
    price = _sql.Column(_sql.String, index=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db = next(get_db())


def count_submenu_and_dishes(
    menu_id,
    addition,
    dishes_count=None,
    submenu_id=None,
):
    try:
        menu = get_instance(model=Menu, filter={'id': menu_id})
    except Exception:
        raise _fastapi.HTTPException(status_code=404, detail='menu not found')
    if not submenu_id:
        menu.submenus_count += addition
    if dishes_count:
        menu.dishes_count -= dishes_count
    submenu = None
    if submenu_id:
        try:
            submenu = get_instance(
                model=SubMenu,
                filter={'id': submenu_id, 'menu_id': menu_id},
            )
        except Exception:
            raise _fastapi.HTTPException(
                status_code=404,
                detail='submenu not found',
            )
        menu.dishes_count += addition
        submenu.dishes_count += addition
        db.add(submenu)
    db.add(menu)


def get_instance(model, filter):

    return db.query(model).filter_by(**filter).one()


def get_instances(model, schema, filter):

    return list(map(schema.from_orm, db.query(model).filter_by(**filter)))


def add_instance(data):
    db.add(data)
    db.commit()
    db.refresh(data)

    return data


def delete_instance(model, **filter):
    delete = get_instance(model, **filter)
    db.delete(delete)
    db.commit()

    if 'submenu_id' not in filter['filter']:
        return delete.dishes_count


def update_instance(model, data, filter):
    tmp = db.query(model).filter_by(**filter)
    res = tmp.update(data.dict(exclude_unset=True))
    db.commit()

    return res


def rollback():
    db.rollback()


def commit():
    db.commit()
