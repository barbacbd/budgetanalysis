from PyQt5.QtWidgets import QMainWindow, QTabWidget
from .widgets import TableItem, SectionWidget, TotalTab
from .widgets.SectionType import SectionType
from .widgets.TableItem import TableItem


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        """
        Create the tabs and add them to the tab widet. These will consist of the default values,
        and the user can add in whatever other values that they wish too enter while the application
        is running.
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
        self._living_expenses = SectionWidget("Living Expenses", living_expenses, SectionType.NEGATIVE)

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
        self._insurance = SectionWidget("Insurance", insurance, SectionType.NEGATIVE)

        savings_investments = [
            TableItem("Savings"),
            TableItem("Non-Retirement Accouns"),
            TableItem("Education (529, ESA, UTMA)"),
            TableItem("IRS(s)"),
            TableItem("401(k)/403(b)/457"),
            TableItem("SEP/SIMPLE"),
            TableItem("Thrift Savings")
        ]
        self._savings_investment = SectionWidget("Savings Investments", savings_investments, SectionType.NEGATIVE)

        consumer_debt = [
            TableItem("Advance Pay"),
            TableItem("Credit Card(s)"),
            TableItem("Auto Loan(s)"),
            TableItem("Student Loan(s)"),
            TableItem("Personal Loan(s)")
        ]
        self._consumer_debt = SectionWidget("Consumer Debt", consumer_debt, SectionType.NEGATIVE)

        gross_income = [
            TableItem("Monthly Income"),
            TableItem("Monthly Income (Spouse)")
        ]
        self._gross_income = SectionWidget("Gross Income", gross_income, SectionType.POSITIVE)

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
        self._other_net_income = SectionWidget("Other Net Income", other_net_income, SectionType.POSITIVE)

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
        A connected function when the total of one of the tabs changes this function will
        be hit, and the totals tab will be updated
        :param title: name of the tab that should be updated
        :param total: the new total amount
        :return: None
        """
        if self._total_tab is not None:
            self._total_tab.update(title, total)