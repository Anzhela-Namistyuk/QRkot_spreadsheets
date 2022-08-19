from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import FinancialBase


class Donation(FinancialBase):
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Пользователем {self.user_id} '
            f'внесена сумма пожертвование {self.full_amount}'
        )
