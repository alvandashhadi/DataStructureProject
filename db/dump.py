import pickle


def dump_data(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)
