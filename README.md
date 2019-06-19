# Budget Analysis


## Description

The project was created to be a simple method for looking at monthly expenses. The user can take all of the 
information for a single month and look at the areas for improvement. 

## How to use the tool

Enter all of the data into each tab. You can add new blocks if there are no data blocks that describe an
expense or net gain that you wish to showcase. There is NO need to enter a negative number, because each section
has an internal value for positive and negative.

```python
self._living_expenses = SectionWidget("Living Expenses", living_expenses, SectionType.NEGATIVE)
self._insurance = SectionWidget("Insurance", insurance, SectionType.NEGATIVE)
self._savings_investment = SectionWidget("Savings Investments", savings_investments, SectionType.NEGATIVE)
self._consumer_debt = SectionWidget("Consumer Debt", consumer_debt, SectionType.NEGATIVE)
self._gross_income = SectionWidget("Gross Income", gross_income, SectionType.POSITIVE)
self._other_net_income = SectionWidget("Other Net Income", other_net_income, SectionType.POSITIVE)
```

The totals for the values will be added correctly based on the NEGATIVE vs PSOTIVE aspect that is associated with that section.

```python
self.total.total = total * int(self._state)
```

Where the state is PSOTIVE or NEGATIVE

In the final tab, _Total_, take a look at the total expenses and determine what areas need improvement. If final
total for the month is not positive you MAY want to address this ! 

## Modules

- [ui](budget_analysis/ui) - The directory contains the MainWindow extension of the Qt MainWindow. Our main window will include all of the widgets.
- [widgets](budget_analysis/ui/widgets) - The directory contains the widgets to be displayed on screen.

## Execution

The installation of the module will also install the _ConfigCreator_ executable. Simply run the command:

```console
BudgetAnalysis
```

to run the program.

## Requirements

```console
Python3.6
PyQt5
QDarkStyle
```
