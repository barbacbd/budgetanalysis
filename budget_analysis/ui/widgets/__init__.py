from PyQt5.QtCore import pyqtSlot, QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QSizePolicy, QHBoxLayout, QPushButton
from .SectionType import SectionType
from .TableItem import TableItem


class SectionTotal(QObject):
    """
    Simple class that will hold a total and a signal when the total
    has changed. The other widgets can tie into this signal
    """
    total = 0.0
    total_changed = pyqtSignal(str, float)


class TotalTab(QWidget):

    def __init__(self) -> None:
        """
        Class/Tab to hold totals of all other section widgets
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

        self._set_table()

    def update(self, title: str, total: float) -> None:
        """
        Update the total value for this section if it exists
        :param title: name of the section to find
        :param total: value of the total for the section
        :return: None
        """
        if self._sections.get(title) is not None:
            self._sections[title] = total

        self._set_table()

    def _set_table(self) -> None:
        """
        Remove any items from the layout that were already there. Then recreate the entire table and
        add in the plus and minus buttons at the end of the layout.
        :return: None
        """
        self._table.setRowCount(0)

        total = 0.0

        for key, value in self._sections.items():
            self._table.setRowCount(self._table.rowCount() + 1)

            title_item = QTableWidgetItem(key)
            title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(self._table.rowCount() - 1, 0, title_item)

            amount_item = QTableWidgetItem(str(value))
            amount_item.setTextAlignment(Qt.AlignRight)
            amount_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
            self._table.setItem(self._table.rowCount() - 1, 1, amount_item)

            total = total + value

        """ Add in a total of all totals value """
        self._table.setRowCount(self._table.rowCount() + 1)
        total_item = QTableWidgetItem("Monthly Savings")
        total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
        self._table.setItem(self._table.rowCount() - 1, 0, total_item)
        total_amount_item = QTableWidgetItem(str(total))
        total_amount_item.setTextAlignment(Qt.AlignRight)
        total_amount_item.setFlags(total_amount_item.flags() & ~Qt.ItemIsEditable)
        self._table.setItem(self._table.rowCount() - 1, 1, total_amount_item)

        self._table.move(0, 0)
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

    def __init__(self, title: str, defaults: [], state: SectionType) -> None:
        """
        This class will contain the layout for each of the customizeable tabs
        The tabs will be sections that detail an area of personal finance. The
        user can change the values by adding their own too.
        """
        super().__init__()

        self.title = title

        if not isinstance(state, SectionType):
            self._state = SectionType.NEGATIVE
        else:
            self._state = state

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

        self.total.total = total * int(self._state)
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


