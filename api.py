import json
import requests
from config import exchanges


class APIException(Exception):  #создаем класс ошибки работы с API
    pass


class Convertor:    #создаем класс переводчика валюты
    @staticmethod
    def get_price(base, sym, amount):   #метод конвертации - просим базовую, конвертируемую валюты и сумму
        try:
            base_key = exchanges[base.lower()]  #проверяем на наличие в словаре базовой валюты(проводим к нижнему регистру)
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]    #проверяем на наличие в словаре конверт.валюты(проволдим к нижнему регистру)
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:     #если пользователь вводит одинаковые валюты
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)  #проверка на тип данных суммы конвертации, используем ValueError
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}')
        #запрашиваем информацию с сервера
        resp = json.loads(r.content)    #переводим в нужный тип данных для удобной работы
        new_price = resp[sym_key] * amount     #ищем нужную валюту и умножаем на конвертируемую сумму
        new_price = round(new_price, 3) #округляем до 3 знаков после запятой
        message = f"Цена {amount} {base} в {sym} : {new_price}"     #результат сохраняем в переменную
        return message  #возвращаем переменную

