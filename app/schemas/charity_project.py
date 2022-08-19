import datetime as dt
from typing import Optional

from pydantic import (BaseModel, Extra, Field, PositiveInt, root_validator,
                      validator)


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_lenght=1, max_lenght=100)
    description: str = Field(..., min_lenght=1)
    full_amount: PositiveInt

    @validator('name')
    def check_lenght_name(cls, value):
        if len(value) > 100:
            raise ValueError(
                'Значение в поле name не должно быть'
                ' длиннее 100 знаков!'
            )
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass

    @root_validator(skip_on_failure=True)
    def check_fields_if_empty(cls, values):
        if None or '' in [values['name'], values['description']]:
            raise ValueError('Заполните обязательные поля!')
        return values


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_lenght=1, max_lenght=100)
    description: Optional[str] = Field(None, min_lenght=1)
    full_amount: Optional[int] = Field(None, gt=0)

    @root_validator(skip_on_failure=True)
    def check_fields_if_empty(cls, values):
        if '' in [values['name'], values['description']]:
            raise ValueError(
                'При редактировании проекта нельзя назначать'
                ' пустое имя, описание или цель фонда!'
            )
        return values


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt.datetime
    close_date: Optional[dt.datetime]

    class Config:
        orm_mode = True
