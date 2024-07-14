from datetime import date, timedelta
from abc import ABC, abstractmethod


class Percent:
    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return f'{self.value}%'


class Simple_Dep(type):
    def __new__(self, summ:int, rate: Percent | int, start: date = date.today(),
                 finish: date = date.today() + timedelta(days=365)):
        print(f'Вклад с суммой {summ} руб, ставкой {rate} %, началом срока - {start}, окончанием срока {finish} ')


class Deposit(ABC):
    def __init__(self, summ: int, rate: Percent | int, start: date = date.today(),
                 finish: date = date.today() + timedelta(days=365)):
        self.__summ = summ
        if isinstance(rate, Percent):
            self.__rate = rate.value
        else:
            self.__rate = rate
        self.__start = start
        self.__finish = finish

    @property
    def summ(self):
        return self.__summ

    @summ.setter
    def summ(self, value: int):
        self.__summ = value

    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, value: int):
        self.__rate = value

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value: int):
        self.__start = value

    @property
    def finish(self):
        return self.__finish

    @finish.setter
    def finish(self, value: int):
        self.__finish = value

    def __add__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("you can add only int")
        return self.__class__(self.summ + value, self.rate, self.start, self.finish)

    def __sub__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("you can sub only int")
        return self.__class__(self.summ - value, self.rate, self.start, self.finish)

    @abstractmethod
    def exit_summ(self):
        pass


class Mixin:
    def simple_interest(self):
        profit = 0
        for y in range(self.start.year, self.finish.year + 1):
            if y==self.finish.year and y==self.start.year:
                profit+= self.summ * self.rate * (self.finish - self.start).days / count_days(y) / 100
            elif y==self.start.year:
                profit+= self.summ * self.rate * (date(y,12, 31) - self.start).days / count_days(y) / 100
            elif y==self.finish.year:
                profit += self.summ * self.rate * (self.finish - date(y, 1, 1)).days / count_days(y) / 100
            else:
                profit += self.summ * self.rate * count_days(y) / count_days(y) / 100
        return profit


class Term(Deposit, Mixin):
    def __init__(self, summ: float, rate: int, start: date = date.today(),
                 finish: date = date.today() + timedelta(days=365)):
        super().__init__(summ, rate, start, finish)

    def exit_summ(self):
        return int(self.summ + self.simple_interest())


class Bonus(Deposit, Mixin):
    def __init__(self, summ: float, rate: int, start: date = date.today(),
                 finish: date = date.today() + timedelta(days=365)):
        super().__init__(summ, rate, start, finish)

    def exit_summ(self):
        if self.summ > 500000:
            return int(self.summ + self.simple_interest() + self.simple_interest() * 0.01)
        else:
            return int(self.summ + self.simple_interest())


class Capital(Deposit):
    def __init__(self, summ: float, rate: int, start: date = date.today(),
                 finish: date = date.today() + timedelta(days=365)):
        super().__init__(summ, rate, start, finish)

    def exit_summ(self):
        cnt_days = sum(count_days(y) for y in range(self.start.year, self.finish.year + 1))
        return int(self.summ * ((1 + self.rate / 100 / cnt_days)** (self.finish-self.start).days))


def count_days(year: int):
    if year % 4 == 0 and year % 100 != 0:
        return 366
    else:
        return 365

