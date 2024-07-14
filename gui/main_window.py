from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QLineEdit, QPushButton,
                             QMessageBox, QWidget, QHBoxLayout, QLabel, QComboBox)
from PyQt6.QtGui import QAction
from datetime import datetime, date
from Bank.Deposit import Term, Bonus, Capital


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Банк")
        self.setGeometry(860, 200, 500, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        full_box = QVBoxLayout()
        hbox_summ = QHBoxLayout()
        self.summ_deposit = QLineEdit()
        self.summ_deposit.setPlaceholderText("Сумма вклада")
        self.rouble_label = QLabel("руб")
        hbox_summ.addWidget(self.summ_deposit)
        hbox_summ.addWidget(self.rouble_label)
        self.hbox_summ = QWidget()
        self.hbox_summ.setLayout(hbox_summ)

        self.rate_label = QLabel("Ставка по вкладу: ")
        self.rate_deposit = QComboBox()
        self.create_rates(self.rate_deposit)

        self.start_date_label = QLabel("Дата открытия вклада: ")
        start_date_box = QHBoxLayout()
        self.start_day = QComboBox()
        self.add_day_item(self.start_day)
        self.start_month = QComboBox()
        self.add_month_item(self.start_month)
        self.start_year = QComboBox()
        self.add_year_item(self.start_year)
        start_date_box.addWidget(self.start_day)
        start_date_box.addWidget(self.start_month)
        start_date_box.addWidget(self.start_year)
        self.start_date_box = QWidget()
        self.start_date_box.setLayout(start_date_box)

        self.finish_date_label = QLabel("Дата закрытия вклада: ")
        finish_date_box = QHBoxLayout()
        self.finish_day = QComboBox()
        self.add_day_item(self.finish_day)
        self.finish_month = QComboBox()
        self.add_month_item(self.finish_month)
        self.finish_year = QComboBox()
        self.add_year_item2(self.finish_year)
        finish_date_box.addWidget(self.finish_day)
        finish_date_box.addWidget(self.finish_month)
        finish_date_box.addWidget(self.finish_year)
        self.finish_date_box = QWidget()
        self.finish_date_box.setLayout(finish_date_box)

        self.type_dep_label = QLabel("Тип вклада: ")
        self.type_deposit_choice = QComboBox()
        self.type_deposit_choice.addItem("Срочный")
        self.type_deposit_choice.addItem("Бонусный")
        self.type_deposit_choice.addItem("Вклад с капитализацией процентов")

        self.get_result = QPushButton("Получить сумму по окончании вклада")
        self.get_result.setStyleSheet('background: rgb(0, 128, 0)')
        self.get_result.clicked.connect(self.get_exit_summ)
        self.result_line_edit = QLineEdit()
        self.result_line_edit.setReadOnly(True)

        full_box.addWidget(self.hbox_summ)
        full_box.addWidget(self.rate_label)
        full_box.addWidget(self.rate_deposit)
        full_box.addWidget(self.start_date_label)
        full_box.addWidget(self.start_date_box)
        full_box.addWidget(self.finish_date_label)
        full_box.addWidget(self.finish_date_box)
        full_box.addWidget(self.type_dep_label)
        full_box.addWidget(self.type_deposit_choice)
        full_box.addWidget(self.get_result)
        full_box.addWidget(self.result_line_edit)

        self.full_box = QWidget()
        self.full_box.setLayout(full_box)
        central_widget = QWidget()
        central_widget.setLayout(full_box)
        self.setCentralWidget(central_widget)
        self.menu()
        self.show()

    def create_rates(self, combo_box: QComboBox):
        for rate in range(1, 16):
            combo_box.addItem(str(rate))

    def add_day_item(self, combo_box: QComboBox):
        for i in range(1, 32):
            combo_box.addItem(str(i))

    def add_month_item(self, combo_box: QComboBox):
        for i in range(1, 13):
            combo_box.addItem(str(i))

    def add_year_item(self, combo_box: QComboBox):
        for i in range(datetime.now().year, 1999, -1):
            combo_box.addItem(str(i))

    def add_year_item2(self, combo_box: QComboBox):
        for i in range(datetime.now().year, 2124):
            combo_box.addItem(str(i))

    def menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('Файл')
        exit_act = QAction('Выход', self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)
        help_menu = menu_bar.addMenu('Справка')
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        about_text = ("Банк\n"
                      "Приложение для рассчета вкладов.")
        QMessageBox.about(self, "О программе", about_text)

    async def get_exit_summ(self):
        all_good = True
        try:
            summ = float(self.summ_deposit.text())
            if summ < 1000:
                QMessageBox.about(self, "Ошибка", "Сумма вклада должна быть не меньше 1000")
                all_good = False
        except ValueError:
            QMessageBox.about(self, "Ошибка", "Сумма вклада должна представлять вещественные числа")
            all_good = False
        try:
            start_date = date(int(self.start_year.currentText()), int(self.start_month.currentText()),
                              int(self.start_day.currentText()))
        except ValueError:
            QMessageBox.about(self, "Ошибка", "Введенной даты не существует")
            all_good = False

        try:
            finish_date = date(int(self.finish_year.currentText()), int(self.finish_month.currentText()),
                               int(self.finish_day.currentText()))
        except ValueError:
            QMessageBox.about(self, "Ошибка", "Введенной даты не существует")
            all_good = False

        if all_good:
            if start_date < finish_date:
                await self.choice_dep_st_and_fi(self.type_deposit_choice.currentText(), summ,
                                          int(self.rate_deposit.currentText()), start_date, finish_date)
            else:
                QMessageBox.about(self, "Ошибка", "Дата открытия вклада должны быть раньше даты закрытия вклада")

    def choice_dep_st_and_fi(self, choice: str, s: float, r: int, st: date, fi: date):
        match choice:
            case "Срочный":
                dep = Term(s, r, st, fi)
                self.result_line_edit.setText(str(dep.exit_summ())+' руб.')
            case "Бонусный":
                dep = Bonus(s, r, st, fi)
                self.result_line_edit.setText(str(dep.exit_summ())+' руб.')

            case "Вклад с капитализацией процентов":
                dep = Capital(s, r, st, fi)
                self.result_line_edit.setText(str(dep.exit_summ())+' руб.')




