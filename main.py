# Ниже в коде используется только dt.datetime, имеет смысл импортировать только его: from datetime import datetime
import datetime as dt


# У класса нет док-стринг поясняющих что это за класс и для чего он нужен.
class Record:
    # Т.к. не используются аннотации типов, то лучше использовать имя параметра date_str, вместо date.
    # Во первых, это устраняет неясность с типом параметра (ожидается date объект, или строка).
    # Во вторых, далее из этого параметра создается атрибу date который как раз уже имеет тип date.
    def __init__(self, amount, comment, date=''):
        # У метода нет док-стринг с описанием параметров.
        self.amount = amount
        # Создание этого атрибута лучше всего вынести в отдельный метод,
        # а использование тернарного if в данном случае только ухудшает читаемость кода
        self.date = (
            dt.datetime.now().date() if
            not
            # Небезопасное создание объекта, если формат строки date будет отличаться от '%d.%m.%Y' то будет ошибка
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


# У класса нет док-стринг поясняющих что это за класс и для чего он нужен.
class Calculator:
    def __init__(self, limit):
        # У метода нет док-стринг с описанием параметров.
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # В качестве переменной цикла использован класс Record из глобальной области видимости, такой подход может привести к непредсказуемым последствиям
        # вплоть до подмены глобального объекта
        for Record in self.records:
            # Т.к. здесь дата вычисляется каждый раз заново то существует вероятность получения разных дат на разных итерациях цикла,
            # что может привести к ошибкам в расчетах.
            # Оптимальным подходом будет задать дату как атрибут при инициализации self.calculation_date, тем более что она используется в еще одном методе ниже
            if Record.date == dt.datetime.now().date():
                # Используйте today_stats += Record.amoun
                today_stats = today_stats + Record.amoun
        return today_stats

    # Методы get_week_stats и get_today_stats выполняют по сути одну и туже функциональность и отличаются только временным
    # диапозоном который используется для расчета расходов. Поэтому вместо этих двух методов имеет смысл сделать один,
    # например get_stats_for_days(days_number: int),
    # который будет принимать на вход количество дней относительно текущей даты за которые нужно посчитать расходы.
    # Например для сегодняшнего дня get_stats_for_days(0), за неделю get_stats_for_days(7).
    # Для определения диапозона  можно использовать объект datetime.timedelta.
    def get_week_stats(self):
        week_stats = 0
        # Как указано выше значение today лучше перенести в атрибут задаваемый при инициализации
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


# У класса нет док-стринг поясняющих что это за класс и для чего он нужен.
class CaloriesCalculator(Calculator):
    # Комментарий перенести в док-стринг для метода
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Старайтесь избегать названий переменных вида x,y,data,i,j и т.п.
        # Название переменной должно отображать то что в ней содержиться
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Бэкслеши для переносов не применяются. - см. требования к коду.
            # Переносы с правильными отступами. - см. требования к коду.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else излишний
        else:
            return('Хватит есть!')


# У класса нет док-стринг поясняющих что это за класс и для чего он нужен.
class CashCalculator(Calculator):
    # Для денежных едениц пердпочтительней использовать Decimal вместо float
    # Так как float это число с плавающей точкой которое может давать погрешность при операциях.
    # В итоге может накапливаться ошибка, а как бы вы восприняли, если бы на вашем банковском счете стала появляться ошибка?:)
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Наименование параметров в lowercase по PEP8
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Для валюты, вместо использования переменных currency_type, currency
        # лучше использовать класс Enum как class Currency(Enum), при этом экземпляр этого класса передавать как currency.
        # Тогда человекочитаемое обозначение валюты можно будет получить через currency.value, избежав создание дополнительной
        # переменной currency_type и постоянное ее изменение, что увеличивает вероятность ошибки.
        # С if/else будут большие проблемы при добавлении новых валют т.к. в итоге получится огромная простыня из этих блоков
        # Поэтому оптимальнее будет создать словарь rates, где ключи это классы Currency(Enum), а значения - курс.
        # таким образом вместо проверки if/else мы сможем получить нужный курс как rates.get(currency).
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # elif излишний
        elif cash_remained < 0:
            # Бэкслеши для переносов не применяются. - см. требования к коду.
            # Переносы с правильными отступами. - см. требования к коду.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        # Вызывать super не нужно, так как мы используем наследование, то метод будет автоматически унаследован
        # от родительского класса.
        # Кроме того, такое переопределение создало ошибку т.к.в родительском классе возвращается значение stats,
        # а в данном случен метод вернет None
        super().get_week_stats()
