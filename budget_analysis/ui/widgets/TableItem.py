class TableItem:
    """
    Class to hold the Title and the monthly dollar amount associated with the name
    """

    def __init__(self, title: str, amount: float = 0.0) -> None:
        """
        :param title: title of the expenditure such as Transportation or clothing
        :param amount: monthly dollar amount
        """
        self.name = title
        self.amount = amount
