# NOTE: Python3.6 will be used for PyQt5.
#!/usr/bin/python3

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QWidget, QTabWidget, QSizePolicy, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSlot, QObject, Qt, pyqtSignal
import sys
import qdarkstyle


NEGATIVE = -1
POSITIVE = 1


class TableItem:
    """
    Class to hold the Title and the monthly dollar amount associated with the name
    """

    def __init__(self, title: str, amount: float=0.0) -> None:
        """
        :param title: title of the expenditure such as Transportation or clothing
        :param amount: monthly dollar amount
        """
        self.name = title
        self.amount = amount


class SectionTotal(QObject):
    total = 0.0
    total_changed = pyqtSignal(str, float)


class TotalTab(QWidget):

    def __init__(self) -> None:
        """

        """
        super().__init__()
        self._sections = {}

        layout = QHBoxLayout()

        self._table = QTableWidget()
        """ Only allow title and amount columns for now """
        self._table.setColumnCount(2)
        """ Expand to fit the layout """
        self._table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self._table)

        """ Create the table and fill in all of the data including the custom and default values """
        self._set_table()

        self.setLayout(layout)

    def add_section(self, title: str) -> None:
        """
        Add the title if it is not already in the list - when adding here we will have a total value of 0.0
        :param title: name of section we wish to add
        :return: None
        """

        if self._sections.get(title) is None:
            self._sections[title] = 0.0

    def update(self, title: str, total: float) -> None:
        """
        Update the total value for this section if it exists
        :param title: name of the section to find
        :param total: value of the total for the section
        :return: None
        """
        if self._sections.get(title) is not None:
            self._sections[title] = total
            print("{} = {}".format(title, total))

        self._set_table()

    def _set_table(self) -> None:
        """
        Remove any items from the layout that were already there. Then recreate the entire table and
        add in the plus and minus buttons at the end of the layout.
        :return: None
        """
        self._table.setRowCount(0)

        for key, value in self._sections.items():
            self._table.setRowCount(self._table.rowCount() + 1)

            title_item = QTableWidgetItem(key)
            title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable);
            self._table.setItem(self._table.rowCount() - 1, 0, title_item)

            amount_item = QTableWidgetItem(str(value))
            amount_item.setTextAlignment(Qt.AlignRight)
            self._table.setItem(self._table.rowCount() - 1, 1, amount_item)

        self._table.move(0,0)
        self._table.resizeColumnsToContents()
        self._resize_columns()

    def _resize_columns(self) -> None:
        """
        resize the columns to match after we have determined which of the columns is the widest.
        Luckily, this will scale no matter how many columns we add
        :return: None
        """
        max_column_width = 0

        for i in range(self._table.columnCount()):
            max_column_width = self._table.columnWidth(i) if self._table.columnWidth(i) > max_column_width else max_column_width

        for i in range(self._table.columnCount()):
            self._table.setColumnWidth(i, max_column_width)


class SectionWidget(QWidget):

    def __init__(self, title: str, defaults: [], state: int) -> None:
        """
        This class will contain the layout for each of the customizeable tabs
        The tabs will be sections that detail an area of personal finance. The
        user can change the values by adding their own too.
        """
        super().__init__()

        self.title = title

        self._state = state if state == POSITIVE or state == NEGATIVE else NEGATIVE
        self.total = 0.0
        self.total = SectionTotal()

        layout = QHBoxLayout()

        self._table = QTableWidget()
        """ Only allow title and amount columns for now """
        self._table.setColumnCount(2)
        """ Expand to fit the layout """
        self._table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._table.itemChanged.connect(self._item_changed)
        self._table.itemSelectionChanged.connect(self._save_selection)

        layout.addWidget(self._table)

        """ default values where only the amount can change """
        self._defaults = defaults
        """ user entered custom values for this section """
        self._custom = []
        """ list of selected items """
        self._selected = []

        """ Create the table and fill in all of the data including the custom and default values """
        self._set_table()

        self.setLayout(layout)

    @pyqtSlot(QTableWidgetItem)
    def _item_changed(self, item: QTableWidgetItem) -> None:
        """
        Determine if the value is valid, a dollar amount or a floating point value will suffice
        :param item: Table Widget Item that was changed
        :return: None
        """
        converted = 0.0

        if item.column() == 1:
            try:
                converted = float(item.text())
            except ValueError:
                item.setText(str(0.0))

        if item.row() < len(self._defaults):
            if item.column() == 0:
                self._defaults[item.row()].name = item.text()
            elif item.column() == 1:
                self._defaults[item.row()].amount = converted
        else:
            if item.column() == 0:
                self._custom[item.row() - len(self._defaults)].name = item.text()
            elif item.column() == 1:
                self._custom[item.row() - len(self._defaults)].amount = converted

        self._set_total()

    def _set_total(self) -> None:
        """
        Get the total for all of the items in this list
        :return: none
        """
        total = 0.0
        for i in range(self._table.rowCount()):
            total += float(self._table.item(i, 1).text()) if self._table.item(i, 1) else 0.0

        self.total.total = total
        self.total.total_changed.emit(self.title, self.total.total)

    def _set_table(self) -> None:
        """
        Remove any items from the layout that were already there. Then recreate the entire table and
        add in the plus and minus buttons at the end of the layout.
        :return: None
        """
        self._table.setRowCount(0)

        for i in range(len(self._defaults)):
            self._table.setRowCount(self._table.rowCount() + 1)

            title_item = QTableWidgetItem(self._defaults[i].name)
            title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable);
            self._table.setItem(self._table.rowCount() - 1, 0, title_item)

            amount_item = QTableWidgetItem(str(self._defaults[i].amount))
            amount_item.setTextAlignment(Qt.AlignRight)
            self._table.setItem(self._table.rowCount() - 1, 1, amount_item)

        for i in range(len(self._custom)):
            self._table.setRowCount(self._table.rowCount() + 1)

            title_item = QTableWidgetItem(self._custom[i].name)
            self._table.setItem(self._table.rowCount() - 1, 0, title_item)

            amount_item = QTableWidgetItem(str(self._custom[i].amount))
            amount_item.setTextAlignment(Qt.AlignRight)
            self._table.setItem(self._table.rowCount() - 1, 1, amount_item)

        self._table.move(0,0)
        self._table.resizeColumnsToContents()
        self._resize_columns()
        self._add_buttons()

        self._set_total()

    def _resize_columns(self) -> None:
        """
        resize the columns to match after we have determined which of the columns is the widest.
        Luckily, this will scale no matter how many columns we add
        :return: None
        """
        max_column_width = 0

        for i in range(self._table.columnCount()):
            max_column_width = self._table.columnWidth(i) if self._table.columnWidth(i) > max_column_width else max_column_width

        for i in range(self._table.columnCount()):
            self._table.setColumnWidth(i, max_column_width)

    def _add_buttons(self) -> None:
        """
        Add in the plus and minus buttons so that the user can add and remove items as they wish.
        :return: None
        """
        self._table.setRowCount(self._table.rowCount() + 1)

        plus = QPushButton()
        plus.setText("+")
        plus.clicked.connect(self._add_entry)
        self._table.setCellWidget(self._table.rowCount() - 1, 0, plus)

        minus = QPushButton()
        minus.setText("-")
        minus.clicked.connect(self._remove_entry)
        self._table.setCellWidget(self._table.rowCount() - 1, 1, minus)

    @pyqtSlot()
    def _add_entry(self) -> None:
        """
        Add a new entry to the custom values so that the user can add custom fields that they can also remove
        :return: None
        """
        self._custom.append(TableItem(""))
        self._set_table()

    @pyqtSlot()
    def _remove_entry(self) -> None:
        """
        Attempt to remove the item(s) from the list. Note: We should ONLY be able to remove the
        items that we have added (defaults can not be removed).
        :return: None
        """
        self._selected.sort(reverse=True)

        for row in self._selected:
            for x in self._custom:
                if self._table.item(row, 0) and x.name == self._table.item(row, 0).text():
                    self._custom.remove(x)

            self._table.removeRow(row)

        self._selected = []
        self._set_total()

    @pyqtSlot()
    def _save_selection(self) -> None:
        """
        We cannot press the minus button without changing the current selection, so we need to save
        the previous valid selections. We will not save any row that was in the defaults range. This
        way the user can delete custom entries when they later press the - button
        :return: None
        """
        indexes = self._table.selectedIndexes()

        temp_indexes = []

        """ 
        Make sure the index is NOT the final row (containing the buttons) 
        It is NOT alreadyy in the list
        It is NOT a default
        """
        for index in indexes:
            if len(self._defaults) <= index.row() < self._table.rowCount()-1 and index.row() not in temp_indexes:
                temp_indexes.append(index.row())
            elif index.row() == self._table.rowCount() - 1:
                return

        self._selected = temp_indexes


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        """

        """
        super().__init__()

        self._tabs = QTabWidget()

        living_expenses = [
            TableItem("Mortgage/Rent"),
            TableItem("Home Repairs/Maintenance"),
            TableItem("Utilities"),
            TableItem("Groceries"),
            TableItem("Personal Goods"),
            TableItem("Entertainment/Dining"),
            TableItem("Clothing"),
            TableItem("Gifts"),
            TableItem("Transportation"),
            TableItem("Child Care"),
            TableItem("Cable & Internet"),
            TableItem("Cell Phone"),
            TableItem("Homeowner Fees"),
            TableItem("Hobbies"),
            TableItem("Children's Activities")
        ]
        self._living_expenses = SectionWidget("Living Expenses", living_expenses, NEGATIVE)

        insurance = [
            TableItem("Auto Insurance"),
            TableItem("Life Insurance"),
            TableItem("Disability"),
            TableItem("Long Term Care"),
            TableItem("Medical"),
            TableItem("Dental"),
            TableItem("Vision"),
            TableItem("Flexible Spending Account"),
            TableItem("Liability Coverage")
        ]
        self._insurance = SectionWidget("Insurance", insurance, NEGATIVE)

        savings_investments = [
            TableItem("Savings"),
            TableItem("Non-Retirement Accouns"),
            TableItem("Education (529, ESA, UTMA)"),
            TableItem("IRS(s)"),
            TableItem("401(k)/403(b)/457"),
            TableItem("SEP/SIMPLE"),
            TableItem("Thrift Savings")
        ]
        self._savings_investment = SectionWidget("Savings Investments", savings_investments, NEGATIVE)

        consumer_debt = [
            TableItem("Advance Pay"),
            TableItem("Credit Card(s)"),
            TableItem("Auto Loan(s)"),
            TableItem("Student Loan(s)"),
            TableItem("Personal Loan(s)")
        ]
        self._consumer_debt = SectionWidget("Consumer Debt", consumer_debt, NEGATIVE)

        gross_income = [
            TableItem("Monthly Income"),
            TableItem("Monthly Income (Spouse)")
        ]
        self._gross_income = SectionWidget("Gross Income", gross_income, POSITIVE)

        other_net_income = [
            TableItem("Rental Income"),
            TableItem("Retirement Income"),
            TableItem("Child Support"),
            TableItem("Disability"),
            TableItem("Investment Income"),
            TableItem("Federal Taxes"),
            TableItem("State/Local Taxes"),
            TableItem("Social Security/Payroll"),
            TableItem("Federal Taxes (Spouse)"),
            TableItem("State/Local Taxes (Spouse)"),
            TableItem("Social Security/Payroll (Spouse)")
        ]
        self._other_net_income = SectionWidget("Other Net Income", other_net_income, POSITIVE)

        self._total_tab = TotalTab()
        self._total_tab.add_section(self._living_expenses.title)
        self._total_tab.add_section(self._insurance.title)
        self._total_tab.add_section(self._savings_investment.title)
        self._total_tab.add_section(self._consumer_debt.title)
        self._total_tab.add_section(self._gross_income.title)
        self._total_tab.add_section(self._other_net_income.title)

        self._living_expenses.total.total_changed.connect(self.update)
        self._insurance.total.total_changed.connect(self.update)
        self._savings_investment.total.total_changed.connect(self.update)
        self._consumer_debt.total.total_changed.connect(self.update)
        self._gross_income.total.total_changed.connect(self.update)
        self._other_net_income.total.total_changed.connect(self.update)

        # Add tabs to the main window
        self._tabs.addTab(self._living_expenses, self._living_expenses.title)
        self._tabs.addTab(self._insurance, self._insurance.title)
        self._tabs.addTab(self._savings_investment, self._savings_investment.title)
        self._tabs.addTab(self._consumer_debt, self._consumer_debt.title)
        self._tabs.addTab(self._gross_income, self._gross_income.title)
        self._tabs.addTab(self._other_net_income, self._other_net_income.title)
        self._tabs.addTab(self._total_tab, "Total")

        # set the central widget to be the tabs widget
        self.setCentralWidget(self._tabs)

    def update(self, title: str, total: float) -> None:
        """

        :param title:
        :param total:
        :return:
        """
        if self._total_tab is not None:
            self._total_tab.update(title, total)

if __name__ == '__main__':
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

    app = QApplication(sys.argv)
    app.setStyleSheet(dark_stylesheet)

    main_window = MainWindow()
    main_window.setMinimumSize(800, 400)
    main_window.setWindowTitle('Budget Analysis')
    main_window.show()

    sys.exit(app.exec_())
