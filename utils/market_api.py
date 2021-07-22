from config import MARKET_TOKEN, MARKET_API
import requests

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
        r = requests.post(
            MARKET_API + 'item',
            headers=headers,
            json=post_data
        )
        instance = cls()
        instance.items_json = r.json()
        instance.items = Items(instance.items_json)
        return instance

class Items:
    def __init__(self, items: list):
        self.items = []
        for item in items:
            self.items.append(ItemModel(item))
        self.get_item_str()

    def get_item_str(self):
        self.items_str = ''
        for item in self.items:
            self.items_str += item.description
            self.items_str += '\n===========================\n'

class ItemModel:
    def __init__(self, data: dict):
        self.__dict__ = data
        self.get_str()

    def get_str(self):
        self.description = f"Имя: {self.name}\n" \
                           f"Кр. имя: {self.shortName}\n" \
                           f"Баз. цена: {self.price}\n" \
                           f"В ср. за 24 ч.: {self.avg24hPrice}\n" \
                           f"В ср. за 7 дн.: {self.avg7daysPrice}\n" \
                           f"Цена у {self.traderName} - {self.traderPrice} {self.traderPriceCur}\n" \
                           f"Слотов: {self.slots}\n" \
                           f"ЦЗС торговец: {int(self.traderPrice) / int(self.slots)}\n" \
                           f"ЦЗС барахолка {int(self.avg24hPrice) / int(self.slots)}\n" \
                           f"ТМ: {self.link}\n" \
                           f"Вики: {self.wikiLink}\n"
