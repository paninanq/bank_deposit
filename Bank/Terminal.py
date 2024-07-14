from datetime import date, datetime
from .Deposit import Term, Bonus, Capital
from Database.controllers.deposit import DepositController
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)


async def choice_dep_st_and_fi(choice, s, r, st, fi):
    match choice:
        case 1:
            dep = Term(s, r, st, fi)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Базовый")

        case 2:
            dep = Bonus(s, r, st, fi)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Бонусный")

        case 3:
            dep = Capital(s, r, st, fi)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Вклад с капитализацией процентов")
        case _:
            print('Неверный выбор.')


async def choice_dep_st(choice, s, r, st):
    match choice:
        case 1:
            dep = Term(summ=s, rate=r, start=st)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Базовый")

        case 2:
            dep = Bonus(summ=s, rate=r, start=st)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Бонусный")
        case 3:
            dep = Capital(summ=s, rate=r, start=st)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Вклад с капитализацией процентов")
        case _:
            print('Неверный выбор.')


async def choice_dep_fi(choice, s, r, fi):
    match choice:
        case 1:
            dep = Term(summ=s, rate=r, finish=fi)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Базовый")
            
        case 2:
            dep = Bonus(summ=s, rate=r, finish=fi)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Вклад с капитализацией процентов") 

        case 3:
            dep = Capital(summ=s, rate=r, finish=fi)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Вклад с капитализацией процентов")  
        case _:
            print('Неверный выбор')


async def choice_dep_noone(choice, s, r):
    match choice:
        case 1:
            dep = Term(summ=s, rate=r)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Базовый")
        case 2:
            dep = Bonus(summ=s, rate=r)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Бонусный")           
        case 3:
            dep = Capital(summ=s, rate=r)
            print(dep.exit_summ())
            dep_contr  = DepositController()
            await DepositController.deposit_insert(dep_contr, dep, "Вклад с капитализацией процентов")
        case _:
            print('Неверный выбор.')


def is_int(s):
    try:
        return int(s)
    except ValueError:
        return False


def is_date(s: list):
    param = True
    for i in s:
        try:
            int(i)
        except ValueError:
            param = False
            break
    if param:
        d = (int(i) for i in s[::-1])
        try:
            date(*d)
            return True
        except ValueError:
            return False


def is_int_rate(s):
    try:
        s = int(s)
        if 1 <= s <= 15:
            return True
        else:
            return False
    except ValueError:
        return False


def true_summ(func):
    def _wrapper():
        try:
            summ = float(func())
            if summ >= 1000:
                return float(summ)
            else:
                _wrapper()
        except ValueError:
            _wrapper()
    return _wrapper


def choice_rate():
    rate = input('Введите ставку, по которой хотите оформить вклад (целое число от 1 до 15%): ')
    while not is_int_rate(rate):
        rate = input('При вводе произошла ошибка \n'
                     'Повторите попытку. Введите ставку, по которой хотите оформить вклад (целое число от 1 до 15%): ')
    return int(rate)


@true_summ
def input_summ():
    summa = input('Введите сумму в рублях, на которую хотите оформить вклад (сумма должна быть не менее 1000 руб): ')
    return summa


def input_date():
    d = input('Введите дату, в формате "число месяц год": ').split()
    while not(is_date(d)):
        d = input('Введенные параметры не являются датой.Введите дату, в формате "число месяц год": ').split()
    d = [int(i) for i in d[::-1]]
    return date(*d)


def registry(func):
    async def _wrapper():
        start_time = datetime.now().time()
        await func()
        finish_time = datetime.now().time()
        print(f'Начало подбора вклада приложением "Банк" - {start_time} \n' 
            f'Конец подбора вклада приложением "Банк" - {finish_time}.')
    return _wrapper


class TerminalCom:
    @staticmethod
    @registry
    async def community():
        s = pool.apply_async(input_summ).get()
        r = pool.apply_async(choice_rate).get()
        while True:
            try:
                ans = input("Вы хотите открыть вклад сегодня? (Ответьте да или нет): ").strip().lower()
                assert ans in ["да", "нет"]
                break
            except AssertionError:
                continue

        if ans == 'нет':
            st = input_date()
            while st < date.today():
                print('Дата открытия вклада не может быть раньше сегодняшней даты.')
                st = input_date()

        else:
            st = None

        while True:
            try:
                ans = input("Вы хотите закрыть вклад через год после открытия? (Ответьте да или нет): ")
                assert ans.lower().strip() in ["да", "нет"]
                break
            except AssertionError:
                print("Данные некорректны.")
                continue

        if ans=='нет':
            fi = input_date()
            if st:
                while fi <= st:
                    print('Дата окончания вклада должна быть посже даты начала.')
                    fi = input_date()
            else:
                while fi <= date.today():
                    print('Дата окончания вклада должна быть позже даты начала.')
                    fi = input_date()
        else:
            fi = None
        print('Типы вкладов: \n'
            '1. Срочный вклад: расчет прибыли осуществляется по формуле простых процентов\n'
            '2. Бонусный вклад: бонус начисляется в конце периода как % от прибыли, если вклад больше 500000 руб\n'
            '3. Вклад с капитализацией процентов\n'
            '4. Я передумал-(а) рассчитывать вклад')
        while True:
            choice = input('Введите номер-(a) вклада, сумму по окончании которого-(ых) хотите посчитать: ').split()
            choices = []
            i = 0
            while i<=len(choice)-1:
                while not is_int(choice[i]):
                    choice = input('Номер-(a) вклада был введен с ошибкой, повторите попытку: ').split()
                    choices = []
                    i = 0
                else:
                    choices+=[int(choice[i])]
                    i+=1
            cont = True
            for ind in range(len(choices)):
                if choices[ind]==4:
                    cont = False
                    print('Расчет вклада завершен.')
                    break
                if st and fi:
                    await choice_dep_st_and_fi(choices[ind], s, r, st, fi)
                elif st:
                    await choice_dep_st(choices[ind], s, r, st)
                elif fi:
                    await choice_dep_fi(choices[ind], s, r, fi)
                else:
                    await choice_dep_noone(choices[ind], s, r)
            if not cont:
                break

