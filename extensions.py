import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if quote == base:
            raise APIException('Введена одна и та же валюта')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюты {base} нет в списке возможных валют')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюты {quote} нет в списке возможных валют')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректный ввод суммы {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={quote_ticker}&base={base_ticker}')
        total_base = round(json.loads(r.content).get('rates').get(quote_ticker) * float(amount), 2)

        return total_base
