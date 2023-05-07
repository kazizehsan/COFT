import json
import csv


def load_data(frn):
    '''Load data from a file.
    :param frn (str): The dataset file name.

    :return: The dataset (a list of examples, each as a dictionary).
    '''
    if frn.endswith(".jsonl"):
        with open(frn) as fr:
            return [json.loads(line) for line in fr.readlines() if line]
    elif frn.endswith(".csv"):
        with open(frn) as fr:
            reader = csv.DictReader(fr)
            return [line for line in reader]


def is_correct(prediction, gold):
    # check if both are of the same type
    if type(prediction) == type(gold):
        return prediction == gold
    else:
        raise Exception(
            f"type mismatch. prediction: {type(prediction)}; gold: {type(gold)};")
