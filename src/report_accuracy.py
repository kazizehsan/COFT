import constants as constants
from utils import is_correct, load_data

# load predictions
dataset_name = constants.DATASETS.STRATEGY_QA.value
split = 'dev'
model_name = constants.LLM_MODEL_NAMES.TEXT_DAVINCI_003.value
prediction_file_name = 'predictions_ccoft_2023-05-06.jsonl'
predictions_frn = f"output_dir/{dataset_name}/{split}/{model_name}/{prediction_file_name}"
predictions = load_data(predictions_frn)

# initialize counts
total_count = 0
complete_correct_count = 0
complete_incorrect_count = 0
incomplete_answer_count = 0
for row in predictions:
    # initialize answer
    answer = None

    # process answer specific to dataset
    if dataset_name == constants.DATASETS.STRATEGY_QA.value:
        # answers in StrategyQA end in 'So the answer is no.' or 'So the answer is yes.'
        if row['answer'] and type(row['answer']) == str:
            processed_answer = row['answer'][-4:].strip().lower()
            if processed_answer in ['no.', 'yes.']:
                if processed_answer == 'no.':
                    answer = False
                elif processed_answer == 'yes.':
                    answer = True

    # counts
    if answer is not None:
        if is_correct(answer, row['gold_answer']):
            complete_correct_count = complete_correct_count + 1
        else:
            complete_incorrect_count = complete_incorrect_count + 1
    else:
        incomplete_answer_count = incomplete_answer_count + 1

    total_count = total_count + 1

print('total_count:', total_count)
print('correct_count:', complete_correct_count)
print('incorrect_count:', complete_incorrect_count+incomplete_answer_count)
acc = round(complete_correct_count / total_count * 100, 1)
print('accuracy:', acc)
print('complete_answer_count:', complete_correct_count+complete_incorrect_count)
print('incomplete_answer_count:', incomplete_answer_count)
