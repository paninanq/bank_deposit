from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String


Base = declarative_base()


class DepositModel(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True)
    first_summ = Column(Integer, nullable=False)
    rate =  Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)
    type_of_deposit = Column(String, nullable=False)
    exit_summ = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Deposits(id={self.id!r}, first_summ={self.first_summ!r}, rate={self.rate!r}, start_date={self.start_date!r}, finish_date={self.finish_date!r}, type_of_deposit={self.type_of_deposit!r}, exit_summ={self.exit_summ!r})'