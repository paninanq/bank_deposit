from Database.connect import get_db_sessionmaker
from Bank.Deposit import *
from Database.models.base import DepositModel
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from exceptions.db_error import DatabaseError


class DepositController:
    def __init__(self) -> None:
        self.db_session_maker = get_db_sessionmaker()

    async def deposit_insert(self, deposit: Deposit, type_of_dep: str):
        try:
            async with self.db_session_maker.begin() as session:
                session.add(DepositModel(first_summ=deposit.summ,
                                        rate=deposit.rate,
                                        start_date=deposit.start,
                                        finish_date=deposit.finish,
                                        type_of_deposit=type_of_dep,
                                        exit_summ=deposit.exit_summ())
                                        )
                await session.commit()
        except DBAPIError as e:
            await session.rollback()
            raise DatabaseError() from e

    async def select_deposit(self, id) -> DepositModel:
        try:
            async with self.db_sessionmaker.begin() as session:
                return await session.scalar(
                    select(DepositModel).where(DepositModel.id == id)
                )
        except DBAPIError as e:
            raise DatabaseError() from e