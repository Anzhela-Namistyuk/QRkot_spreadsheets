import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationForUserDB(DonationBase):
    id: int
    create_date: dt.datetime

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt.datetime
    close_date: Optional[dt.datetime]

    class Config:
        orm_mode = True
