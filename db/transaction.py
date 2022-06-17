from datetime import datetime

"""
use linked list to store transactions
"""


class Transaction:
    def __init__(
        self,
        amount: int,
        to_account: int,
        created_at: datetime = datetime.now(),
    ):
        self.amount = amount
        self.created_at = created_at
        self.to_account = to_account
        self.child = None

    def insert(self, child: "Transaction"):
        if self.child is None:
            self.child = child
            return
        self.child.insert(child)

    def to_list(self):
        result = [self]
        if self.child is not None:
            result.extend(self.child.to_list())
        return result
