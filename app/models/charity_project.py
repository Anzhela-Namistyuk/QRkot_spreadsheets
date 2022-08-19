from sqlalchemy import Column, String, Text

from app.core.db import FinancialBase


class CharityProject(FinancialBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f'Название проекта {self.name}, '
                f'описание {self.description}')
