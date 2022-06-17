import pickle

from db.accounts import AccountRBTree


def load_data(filename):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        print(e)
        return AccountRBTree()
