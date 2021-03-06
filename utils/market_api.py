from config import MARKET_TOKEN, MARKET_API, DB_SCHEMA
import aiohttp
from loader import db
import json


def get_chart_string(percents: str) -> str:
    if float(percents) > 0:
        return f'{percents}%\U0001F4C8'
    return f'{percents}%\U0001F4C9'


class Market:
    @classmethod
    async def get_item(cls, item: str):
        headers = {
            'x-api-key': MARKET_TOKEN,
            'Content-Type': 'application/json'
        }
        post_data = {
            'q': item,
            'lang': 'ru'
        }
        instance = cls()
        async with aiohttp.ClientSession() as ses:
            async with ses.post(MARKET_API+'item', headers=headers, json=post_data) as resp:
                instance.items_json = await resp.json()
        instance.items = await Items.get_from_user_request(instance.items_json)
        return instance

    @classmethod
    async def get_all_items(cls):
        headers = {
            'x-api-key': MARKET_TOKEN
        }
        instance = cls()
        async with aiohttp.ClientSession() as ses:
            async with ses.get(MARKET_API+'items/all', headers=headers) as resp:
                instance.items_json = await resp.json()
                data = {'data': instance.items_json}
                success, res = await db.execute(
                    f"""select {DB_SCHEMA}.fn_update_itemlist({json.dumps(data).replace("'", "''")}) as result"""
                )
                if success:
                    print(res.status_text)
        return instance


class Items:
    @classmethod
    async def get_from_user_request(cls, items: list):
        instance = cls()
        instance.items = []
        for item in items:
            instance.items.append(ItemModel(item))
        instance.__get_item_str()
        return instance

    def __get_item_str(self):
        self.items_str = ''
        for item in self.items:
            self.items_str += item.description
            self.items_str += '\n===========================\n'


class ItemModel:
    def __init__(self, data: dict):
        self.__dict__ = data
        self.__get_str()

    def __get_str(self):
        self.description = f"??????: {self.name}\n" \
                           f"????. ??????: {self.shortName}\n" \
                           f"??????. ????????: {self.price}\n" \
                           f"?? ????. ???? 24 ??.: {self.avg24hPrice}\n" \
                           f"???????????????? ???? 24 ??.: {get_chart_string(self.diff24h)}\n" \
                           f"?? ????. ???? 7 ????.: {self.avg7daysPrice}\n" \
                           f"???????????????? ???? 7 ????.: {get_chart_string(self.diff7days)}\n" \
                           f"???????? ?? {self.traderName} - {self.traderPrice} {self.traderPriceCur}\n" \
                           f"????????????: {self.slots}\n" \
                           f"?????? ????????????????: {int(self.traderPrice) / int(self.slots)}\n" \
                           f"?????? ?????????????????? {int(self.avg24hPrice) / int(self.slots)}\n" \
                           f"????: <a href=\"{self.link}\"> ???????????? </a>\n" \
                           f"????????: <a href=\"{self.wikiLink}\"> ???????????? </a>\n"
