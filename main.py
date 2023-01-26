import pict_in_db
from pict_in_db.pict_in_db import start_stop
from pict_in_db.equally import equally
from pict_in_db.del_temp import del_Temp
from pict_in_db.pict_delete import pict_delete


# # Инициализируем бот и диспетчер
# bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
# dp: Dispatcher = Dispatcher(bot)

if __name__ == '__main__':
    try:
        # Запускаем функцию main
        # equally()
        print('   ------ Версия от 25 января 2023 -----   ')
        choice = (input('Выберите действие: \n'
                           '1 - скачивание картинок (не используется),\n'
                           '2 - Поиск товара в БД и загрузка картинки в БД (Для Энского В.Е.), \n'
                           '3 - Сопоставить товары Электра - Русский Свет, \n'
                           '4 - Удалить некорректную картинку, \n'
                           '0 - Очистить папку Temp, \n'
                           '9 - Выход (или любая клавиша), \n'
                           'x - Заменить изображение для товара (требуется Код производителя) пока нет \n'))

        if choice == '1':
            print('В разработке')
        elif choice == '2':
            start_stop()
        elif choice == '3':
            equally()
        elif choice == '4':
            pict_delete()
        elif choice == '0':
            del_Temp()
        elif choice == 'x':
            pass
            # pict_delete()
            # equally()
        else:
            print('С П А С И Б О')
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        print('Непредвиденная ошибка')
