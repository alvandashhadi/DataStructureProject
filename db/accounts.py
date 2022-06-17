from db.transaction import Transaction

"""
We use red and black tree to store accounts.
it's used because we can find any account in O(logN) time.
"""


class AccountNode:
    def __init__(
        self,
        name: str,
        balance: int,
        id: int | None = None,
        parent: "AccountNode" = None,
        left: "AccountNode" = None,
        right: "AccountNode" = None,
        transaction: Transaction = None,
        color: str = "red",
    ):
        self.name = name
        self.balance = balance
        self.left = left
        self.right = right
        self.transaction = transaction
        self.id = id
        self.parent = parent
        self.color = color

    def insert_transaction(self, transaction: Transaction):
        self.balance += transaction.amount
        if self.transaction is None:
            self.transaction = transaction
            return
        self.transaction.insert(transaction)

    def __str__(self):
        return f"{self.id}- {self.name} ({self.balance})"

    def __repr__(self):
        return f"{self.id}- {self.name} ({self.balance})"

    def to_list(self):
        result = []
        if self.left is not None and self.left.name != "NULL":
            result.extend(self.left.to_list())
        result.append(self)
        if self.right is not None and self.right.name != "NULL":
            result.extend(self.right.to_list())
        return result

    def get_transaction_list(self):
        if self.transaction is None:
            return []
        return self.transaction.to_list()


class AccountRBTree:
    def __init__(self):
        self.NULL = AccountNode(
            name="NULL",
            balance=0,
            id=0,
            color="black",
        )
        self.root = self.NULL

    def insert_node(self, node: AccountNode):
        node.color = "red"
        y = None
        x = self.root
        while x != self.NULL and x is not None:
            y = x
            if node.id < x.id:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.id < y.id:
            y.left = node
        else:
            y.right = node
        if node.parent is None:
            node.color = "black"
            return
        if node.parent.parent is None:
            return
        self.fixInsert(node)

    def LR(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def RR(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NULL and y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fixInsert(self, k):
        while k.parent.color == "red":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.RR(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.LR(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.LR(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.RR(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "black"

    def fixDelete(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.LR(x.parent)
                    s = x.parent.right
                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.RR(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.LR(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.RR(x.parent)
                    s = x.parent.left
                if s.right.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.LR(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.RR(x.parent)
                    x = self.root
        x.color = "black"

    def __rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node_helper(self, node, key):
        z = self.NULL
        while node != self.NULL and node is not None:
            if node.id == key:
                z = node
                break
            if node.id <= key:
                node = node.right
            else:
                node = node.left
        if z == self.NULL or z is None:
            return
        y = z
        y_original_color = y.color
        if z.left == self.NULL or z.left is None:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.NULL or z.right is None:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.fixDelete(x)

    def delete_node(self, id):
        self.delete_node_helper(self.root, id)

    def get_node(self, id):
        node = self.root
        while node != self.NULL and node is not None:
            if node.id == id:
                return node
            if node.id <= id:
                node = node.right
            else:
                node = node.left
        return None

    def get_max_id(self):
        node = self.root
        if node == self.NULL or node is None:
            return 0
        while node.right != self.NULL and node.right is not None:
            node = node.right
        return node.id

    def minimum(self, node):
        while node.left != self.NULL and node.left is not None:
            node = node.left
        return node

    def to_list(self):
        if self.root == self.NULL:
            return []
        return self.root.to_list()
