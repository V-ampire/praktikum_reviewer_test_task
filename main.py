# Ниже в коде используется только dt.datetime, имеет смысл импортировать только его: from datetime import datetime
import datetime as dt


# У класса нет док-стринг поясняющих что это за класс и для чего он нужен.
class Record:
    # Т.к. не используются аннотации типов, то лучше использовать имя параметра date_str, вместо date.
    # Во первых, это устраняет неясность с типом параметра (ожидается date объект, или строка).
    # Во вторых, далее из этого параметра создается атрибут класса date который как раз уже имеет тип date.
    def __init__(self, amount, comment, date=''):
        # У метода нет док-стринг с описанием параметров.
        self.amount = amount
        # Создание этого атрибута лучше всего вынести в отдельный метод, а использование тернарного if только ухудшает читаемость кода
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
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
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
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
