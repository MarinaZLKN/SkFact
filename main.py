import telebot
from api import APIException, Convertor
from config import TOKEN, exchanges
import traceback



bot = telebot.TeleBot(TOKEN) #инициализируем обьект класса и передаем свой токен


#Message – это объект из Bot API, содержащий в себе информацию о сообщении. Полезные поля:
#message.chat.id – идентификатор чата
#message.from.id – идентификатор пользователя
#message.text – текст сообщения


@bot.message_handler(commands=['start', 'help']) #Декоратор @message_handler реагирует на входящие сообщение.
def start(message: telebot.types.Message):      #функция обработчик/ответ на команды
    text = "Приветствую!Чем я могу быть полезен?"
    bot.send_message(message.chat.id, text) #Функция send_message принимает идентификатор чата (берем его из сообщения)
    # и текст для отправки.

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message): #отображает доступные валюты
    text = 'Доступные валюты:'
    for i in exchanges.keys():  #проходим циклом по ключам словаря валют
        text = '\n'.join((text, i)) #выводим с новой строчки
    bot.reply_to(message, text)     #отвечаем на сообщение, reply_to отмечаем сообщение как отвеченное


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')    #присваиваем переменной введенные данные в списке
    try:        #делаем проверку на запрашиваемые валюты
        if len(values) != 3:        #если длина валюты не равна 3 символам
            raise APIException('Неверное количество параметров!')   #вызываем ошибку

        answer = Convertor.get_price(*values)   #вызываем метод конвертации распаковывая введенные данные
    except APIException as e:       #предполагаем ошибку команды
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:     
        traceback.print_tb(e.__traceback__) #для отслеживания опечаток
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)   #если не было ошибок возвращаем ответ



bot.polling()

