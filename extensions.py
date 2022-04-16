import requests
import json
from config import currencies


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(original: str, result: str, quantity: str):

        try:
            original_key = currencies[original.lower()]
        except KeyError:
            raise APIException(f'Валюта {original} не найдена')

        try:
            result_key = currencies[result.lower()]
        except KeyError:
            raise APIException(f'Валюта {result} не найдена')


        if original == result:
            raise APIException('Невозможно перевести валюту саму в себя')

        try:
            quantity = float(quantity)
        except ValueError:
            raise APIException(f'Не удалось обработать колличество валюты "{quantity}"')

        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={original_key}_{result_key}&compact=ultra&apiKey=609590f5ef6ff491184c')
        coast = round(json.loads(r.content)[f'{original_key}_{result_key}'] * quantity, 2)
        answer = f'Стоимость {quantity} {original} в {result} : {coast}'
        return answer
