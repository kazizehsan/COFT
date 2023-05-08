from utils import load_data
import constants as constants

# load dataset
dataset_name = constants.DATASETS.STRATEGY_QA.value
split = 'train'
dataset_frn = f"datasets/{dataset_name}/{split}.jsonl"
dataset = load_data(dataset_frn)

# Fu et al. (https://arxiv.org/abs/2210.00720) suggests that
# questions length is an indicator of complexity of a sample
# for datasets that do not have annotated reasoning chains.
# question_lengths = [(length,id),...]
question_lengths = [
    (len(example["question"]), example["id"]) for example in dataset]
# sort by length
question_lengths.sort(reverse=True, key=lambda elem: elem[0])
question_ids = [elem[1] for elem in question_lengths]

# lets pick n longest questions
n = 15
complex_questions = [(example["id"], len(example["question"]), example['question'], example['answer'], example['facts'], example['decomposition'])
                     for example in dataset if example["id"] in question_ids[:n]]


for question in complex_questions:
    print(question, end='\n\n')
