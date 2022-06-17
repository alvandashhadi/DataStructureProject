import curses

from db import AccountNode, AccountRBTree, Transaction, dump_data, load_data
from heap import heap_sort

main_menu = """         Main Menu
1. Add Account
2. Update Account
3. Delete Account
4. Show Accounts
5. Show Account Details
6. Create Transaction
7. Exit"""


def get_account(stdscr, data: AccountRBTree):
    while True:
        stdscr.clear()
        curses.echo()
        stdscr.addstr(0, 0, 'Enter Account ID(enter "q" to return): ')
        account_id = 0
        character = stdscr.getch()
        if character == ord("q"):
            return
        while character != ord("\n"):
            if character == curses.KEY_BACKSPACE:
                account_id = account_id // 10
            else:
                account_id = account_id * 10 + character - ord("0")
            character = stdscr.getch()
        stdscr.clear()
        account: AccountNode | None = data.get_node(id=account_id)
        if account is None:
            stdscr.addstr(
                0,
                0,
                f"Account not found with id:{account_id}\n"
                "press any key to continue\n"
                'enter "q" to return',
            )
        else:
            stdscr.addstr(0, 0, f"id {account.id}\n")
            stdscr.addstr(f"name {account.name}\n")
            stdscr.addstr(f"balance {account.balance}\n")
            stdscr.addstr("transactions:\n")
            stdscr.addstr("account_id   value   created at\n")
            for transaction in account.get_transaction_list():
                stdscr.addstr(
                    f"{transaction.to_account}   {transaction.amount}"
                    f"   {transaction.created_at}\n"
                )
            stdscr.addstr(
                '\n\npress any key to continue\nenter "q" to return',
            )
        character = stdscr.getch()
        if character == ord("q"):
            return


def add_account(stdscr, data: AccountRBTree):
    while True:
        stdscr.clear()
        curses.echo()
        stdscr.addstr(0, 0, 'Enter Account Name(enter "q" to return): ')
        name = ""
        character = stdscr.getch()
        if character == ord("q"):
            return
        while character != ord("\n"):
            if character == curses.KEY_BACKSPACE:
                name = name[:-1]
            else:
                name += chr(character)
            character = stdscr.getch()
        stdscr.addstr(
            1, 0, 'Enter Account Initial Balance(enter "q" to return): '
        )
        balance = 0
        character = stdscr.getch()
        if character == ord("q"):
            return
        while character != ord("\n"):
            if character == curses.KEY_BACKSPACE:
                balance = balance // 10
            else:
                balance = balance * 10 + character - ord("0")
            character = stdscr.getch()
        new_id = data.get_max_id() + 1
        account = AccountNode(
            name, balance, new_id, left=data.NULL, right=data.NULL
        )
        data.insert_node(account)
        stdscr.clear()
        curses.noecho()
        stdscr.addstr(
            0,
            0,
            f"Account {name} added with id:{new_id}\n"
            "press any key to continue\n"
            'enter "q" to return',
        )
        character = stdscr.getch()
        if character == ord("q"):
            return


def update_account(stdscr, data: AccountRBTree):
    while True:
        stdscr.clear()
        curses.echo()
        stdscr.addstr(0, 0, 'Enter Account ID(enter "q" to return): ')
        account_id = 0
        character = stdscr.getch()
        if character == ord("q"):
            return
        while character != ord("\n"):
            if character == curses.KEY_BACKSPACE:
                account_id = account_id // 10
            else:
                account_id = account_id * 10 + character - ord("0")
            character = stdscr.getch()
        stdscr.clear()
        account: AccountNode | None = data.get_node(id=account_id)
        if account is None:
            stdscr.addstr(
                0,
                0,
                f"Account not found with id:{account_id}\n"
                "press any key to continue\n"
                'enter "q" to return',
            )
        else:
            stdscr.addstr(
                0,
                0,
                f"Enter Account New Name, current {account.name}\n"
                '(enter "q" to return and "\\n" to skip): ',
            )
            name = ""
            character = stdscr.getch()
            if character == ord("q"):
                return
            while character != ord("\n"):
                if character == curses.KEY_BACKSPACE:
                    name = name[:-1]
                else:
                    name += chr(character)
                character = stdscr.getch()
            if name != "":
                account.name = name
            stdscr.addstr(
                1,
                0,
                f"Enter Account Initial Balance, current {account.balance}\n"
                '(enter "q" to return, enter "s" to skip): ',
            )
            balance = 0
            character = stdscr.getch()
            if character == ord("q"):
                return
            if character == ord("s"):
                balance = account.balance
            else:
                while character != ord("\n"):
                    if character == curses.KEY_BACKSPACE:
                        balance = balance // 10
                    else:
                        balance = balance * 10 + character - ord("0")
                    character = stdscr.getch()
            account.balance = balance
            stdscr.clear()
            stdscr.addstr(
                0,
                0,
                f"Account {account} updated\n"
                "press any key to continue\n"
                'enter "q" to return',
            )
        character = stdscr.getch()
        if character == ord("q"):
            return


def get_account_list(stdscr, data: AccountRBTree):
    sort_options = {
        "id": lambda x: x.id,
        "-id": lambda x: -x.id,
        "balance": lambda x: x.balance,
        "-balance": lambda x: -x.balance,
    }
    accounts = data.to_list()
    stdscr.clear()
    curses.noecho()
    stdscr.addstr(
        0,
        0,
        'input "a" for ascending and "d" for decending\n',
    )
    ascending = None
    character = stdscr.getch()
    if character == ord("a"):
        ascending = True
    elif character == ord("d"):
        ascending = False
    else:
        stdscr.clear()
        curses.noecho()
        stdscr.addstr(
            0,
            0,
            "invalid input\n",
        )
        stdscr.getch()
        return
    stdscr.addstr(
        'input "i" for id and "b" for balance\n',
    )
    sort_by = None
    character = stdscr.getch()
    if character == ord("i"):
        sort_by = "id"
    elif character == ord("b"):
        sort_by = "balance"
    else:
        stdscr.clear()
        curses.noecho()
        stdscr.addstr(
            0,
            0,
            "invalid input\n",
        )
        stdscr.getch()
        return
    sort_by = sort_by if ascending else f"-{sort_by}"
    heap_sort(accounts, sort_options[sort_by])
    stdscr.clear()
    stdscr.addstr(0, 0, "id  name  balance\n")
    for account in accounts:
        stdscr.addstr(
            f"{account.id}  {account.name}  {account.balance}\n",
        )
    stdscr.addstr("press any key to return")
    stdscr.getch()


def create_transaction(stdscr, data: AccountRBTree):
    stdscr.clear()
    curses.echo()
    stdscr.addstr(0, 0, 'Enter First Account ID(enter "q" to return): ')
    account_id1 = 0
    character = stdscr.getch()
    if character == ord("q"):
        return
    while character != ord("\n"):
        if character == curses.KEY_BACKSPACE:
            account_id1 = account_id1 // 10
        else:
            account_id1 = account_id1 * 10 + character - ord("0")
        character = stdscr.getch()
    stdscr.clear()
    account1: AccountNode | None = data.get_node(id=account_id1)
    if account1 is None:
        stdscr.addstr(0, 0, f"Account not found with id:{account_id1}\n")
        stdscr.getch()
        return
    stdscr.addstr(0, 0, 'Enter Second Account ID(enter "q" to return): ')
    account_id2 = 0
    character = stdscr.getch()
    if character == ord("q"):
        return
    while character != ord("\n"):
        if character == curses.KEY_BACKSPACE:
            account_id2 = account_id2 // 10
        else:
            account_id2 = account_id2 * 10 + character - ord("0")
        character = stdscr.getch()
    stdscr.clear()
    account2: AccountNode | None = data.get_node(id=account_id2)
    if account2 is None:
        stdscr.addstr(0, 0, f"Account not found with id:{account_id2}\n")
        stdscr.getch()
        return
    stdscr.addstr(0, 0, 'Enter Transaction Amount(enter "q" to return): ')
    amount = 0
    character = stdscr.getch()
    if character == ord("q"):
        return
    while character != ord("\n"):
        if character == curses.KEY_BACKSPACE:
            amount = amount // 10
        else:
            amount = amount * 10 + character - ord("0")
        character = stdscr.getch()
    stdscr.clear()
    if amount > account1.balance:
        stdscr.addstr(0, 0, "Insufficient balance\n")
        stdscr.getch()
    account1.insert_transaction(Transaction(-amount, account_id2))
    account2.insert_transaction(
        Transaction(
            amount,
            account_id1,
        )
    )
    stdscr.addstr(0, 0, "Done!\n")
    stdscr.getch()


def delete_account(stdscr, data: AccountRBTree):
    stdscr.clear()
    curses.echo()
    while True:
        stdscr.addstr('Enter Account ID(enter "q" to return): ')
        account_id = 0
        character = stdscr.getch()
        if character == ord("q"):
            return
        while character != ord("\n"):
            if character == curses.KEY_BACKSPACE:
                account_id = account_id // 10
            else:
                account_id = account_id * 10 + character - ord("0")
            character = stdscr.getch()
        stdscr.clear()
        data.delete_node(id=account_id)
        stdscr.addstr("Done!\n")


def main(stdscr):
    data = load_data("accounts.pickle")
    flag = True
    while flag:
        stdscr.clear()
        curses.noecho()
        stdscr.addstr(main_menu, curses.color_pair(22))
        char = stdscr.getch()
        if char == ord("1"):
            add_account(stdscr, data)
        elif char == ord("2"):
            update_account(stdscr, data)
        elif char == ord("3"):
            delete_account(stdscr, data)
        elif char == ord("4"):
            get_account_list(stdscr, data)
        elif char == ord("5"):
            get_account(stdscr, data)
        elif char == ord("6"):
            create_transaction(stdscr, data)
        elif char == ord("7"):
            flag = False
    dump_data(data, "accounts.pickle")


curses.wrapper(main)
