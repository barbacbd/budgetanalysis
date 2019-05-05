# NOTE: Python3.6 will be used for PyQt5.
#!/usr/bin/python3

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QWidget, QTabWidget, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, QObject, Qt
import sys
import qdarkstyle


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


class SectionWidget(QWidget):
    """

    """

    def __init__(self, defaults: []) -> None:
        """

        """
        super().__init__()

        layout = QHBoxLayout()

        self._table = QTableWidget()
        self._table.setColumnCount(2)
        self._table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._table.itemChanged.connect(self._item_changed)

        layout.addWidget(self._table)

        self._defaults = defaults

        self._set_table()

        self.setLayout(layout)

    @pyqtSlot(QTableWidgetItem)
    def _item_changed(self, item: QTableWidgetItem) -> None:
        """
        Determine if the value is valid, a dollar amount or a floating point value will suffice
        :param item: Table Widget Item that was changed
        :return: None
        """
        if item.column() == 1:
            try:
                converted = float(item.text())
            except ValueError:
                item.setText(str(0.0))

    def _set_table(self) -> None:
        """
        Remove any items from the layout that were already there. Then recreate the entire table and
        add in the plus and minus buttons at the end of the layout.
        :return: None
        """
        self._table.setRowCount(0)
        self._table.setRowCount(len(self._defaults))

        for i in range(len(self._defaults)):
            title_item = QTableWidgetItem(self._defaults[i].name)
            title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable);
            self._table.setItem(i, 0, title_item)

            amount_item = QTableWidgetItem(str(self._defaults[i].amount))
            amount_item.setTextAlignment(Qt.AlignRight)
            self._table.setItem(i, 1, amount_item)

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
        self._living_expenses = SectionWidget(living_expenses)

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
        self._insurance = SectionWidget(insurance)

        savings_investments = [
            TableItem("Savings"),
            TableItem("Non-Retirement Accouns"),
            TableItem("Education (529, ESA, UTMA)"),
            TableItem("IRS(s)"),
            TableItem("401(k)/403(b)/457"),
            TableItem("SEP/SIMPLE"),
            TableItem("Thrift Savings")
        ]
        self._savings_investment = SectionWidget(savings_investments)

        consumer_debt = [
            TableItem("Advance Pay"),
            TableItem("Credit Card(s)"),
            TableItem("Auto Loan(s)"),
            TableItem("Student Loan(s)"),
            TableItem("Personal Loan(s)")
        ]
        self._consumer_debt = SectionWidget(consumer_debt)

        gross_income = [
            TableItem("Federal Taxes"),
            TableItem("State/Local Taxes"),
            TableItem("Social Security/Payroll"),
            TableItem("Federal Taxes (Spouse)"),
            TableItem("State/Local Taxes (Spouse)"),
            TableItem("Social Security/Payroll (Spouse)")
        ]
        self._gross_income = SectionWidget(gross_income)

        other_net_income = [
            TableItem("Rental Income"),
            TableItem("Retirement Income"),
            TableItem("Child Support"),
            TableItem("Disability"),
            TableItem("Investment Income")
        ]
        self._other_net_income = SectionWidget(other_net_income)


        # Add tabs to the main window
        self._tabs.addTab(self._living_expenses, "Living Expenses")
        self._tabs.addTab(self._insurance, "Insurance")
        self._tabs.addTab(self._savings_investment, "Savings & Investment")
        self._tabs.addTab(self._consumer_debt, "Consumer Debt")
        self._tabs.addTab(self._gross_income, "Gross Income")
        self._tabs.addTab(self._other_net_income, "Other Income")

        # set the central widget to be the tabs widget
        self.setCentralWidget(self._tabs)


if __name__ == '__main__':
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

    app = QApplication(sys.argv)
    app.setStyleSheet(dark_stylesheet)

    main_window = MainWindow()
    main_window.setMinimumSize(800, 400)
    main_window.setWindowTitle('Budget Analysis')
    main_window.show()

    sys.exit(app.exec_())
