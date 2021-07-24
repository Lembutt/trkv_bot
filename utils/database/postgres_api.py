import contextlib
import enum
import json
from typing import (Optional, Union, List, overload, Literal, final, Tuple, Any, Dict, Protocol, AsyncGenerator)
import asyncpg
from asyncpg.transaction import Transaction
from .result import Result
from config import DB_NAME, DB_HOST, DB_USER, DB_PASS
from loguru import logger


class FormatType(enum.Enum):
    OR_ = ' AND '
    AND_ = ' OR '


@enum.unique
class FetchType(enum.Enum):
    FETCH = {"fetch": True}
    FETCH_ROW = {"fetchrow": True}
    FETCH_VAL = {"fetchval": True}
    EXECUTE = {"execute": True}


class DBProto(Protocol):
    async def setup(self, *args: Any, **kwargs: Any) -> None: ...

    async def create_table(self) -> None: ...


class WithDefaultsValues(DBProto):
    async def add_defaults(self, *args: Any, **kwargs: Any) -> Any: ...


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseDB(metaclass=SingletonMeta):
    """Базовый класс базы данных"""

    def __init__(self, db_name: Optional[str] = None) -> None:
        self.pool: Optional[asyncpg.Pool] = None
        self.db_name = db_name if isinstance(db_name, str) else self.__class__.__name__.lower() + "s"

    @final
    @logger.catch
    async def create(self) -> None:
        self.pool: asyncpg.Pool = await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            database=DB_NAME
        )

    @contextlib.asynccontextmanager
    async def transaction(
            self,
    ) -> AsyncGenerator[Optional[Transaction], Any]:
        """ Yield an :class:`_asyncio.AsyncSessionTransaction` object. """
        async with self.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction():
                yield connection

    @overload
    async def execute(self,
                      command: str,
                      *args: Any,
                      fetch: Literal[True],
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False) -> Optional[List[asyncpg.Record]]:
        ...

    @overload
    async def execute(self,
                      command: str,
                      *args: Any,
                      fetch: bool = False,
                      fetchval: Literal[True],
                      fetchrow: bool = False,
                      execute: bool = False
                      ) -> Optional[asyncpg.Record]:
        ...

    @overload
    async def execute(self,
                      command,
                      *args: Any,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: Literal[True],
                      execute: bool = False
                      ) -> Optional[Any]:
        ...

    @overload
    async def execute(self,
                      command: str,
                      *args: Any,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: Literal[True]
                      ) -> str:
        ...

    @logger.catch
    async def execute(self, command: str, *args: Any,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ) -> Optional[Union[Any, List[asyncpg.Record], str]]:
        async with self.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction(isolation='read_committed'):
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def query(self, sql: str, fetch_type=FetchType.EXECUTE) -> Tuple[bool, Optional[Result]]:
        try:
            unparsed_res = await self.execute(sql, **fetch_type.value)
            logger.debug(f"unparsed_res -->> {unparsed_res}")
            values = [dict(record) for record in unparsed_res]
            logger.debug(f"dict values -->> {values}")
            parsed_res = {}
            if len(values) > 0:
                for key in values[0]:
                    parsed_res[key] = json.loads(values[0][key])
                res = Result(parsed_res)
                return True, res
            else:
                logger.error(f"Database sent unexpected result. SQL: {sql}. Result:{unparsed_res}.")
                return False, None
        except TypeError as te:
            logger.exception(f"Database sent unexpected result. SQL: {sql}. Result: {unparsed_res}. Exception: {te}")
            return False, None

        except Exception as e:
            logger.exception(f"SQL:{sql}. Exception in db.query() method: {e}")
            raise Exception('Ошибка в методе query\n' + str(e))

    @staticmethod
    def format_arguments(
            sql: str,
            parameters: Dict[str, Union[str, int, float]],
            format_type: FormatType = FormatType.AND_
    ) -> Tuple[str, tuple]:
        sql += f" {format_type.value} ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @logger.catch
    async def setup(self, *args: Any, **kwargs: Any) -> None:
        await self.create()
        # await self.create_table()