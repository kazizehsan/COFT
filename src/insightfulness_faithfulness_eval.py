import random
import constants as constants
from utils import load_data

# load predictions
shuffle = True
sample_size = 50
dataset_name = constants.DATASETS.STRATEGY_QA.value
split = 'dev'
model_name = constants.LLM_MODEL_NAMES.TEXT_DAVINCI_003.value
prediction_file_name = 'predictions_ccoft_2023-05-06.jsonl'
predictions_frn = f"output_dir/{dataset_name}/{split}/{model_name}/{prediction_file_name}"
predictions = load_data(predictions_frn)

insightful_scores = []
faithful_scores = []

if shuffle:
    random.shuffle(predictions)

for row in predictions[:sample_size]:
    facts = []
    thoughts = []
    model_prediction = None
    for line in row['answer'].split("\n"):
        if line.startswith("(fact)"):
            facts.append(line[len("(fact) "):])
        elif line.startswith("(thought)"):
            thoughts.append(line[len("(thought) "):])
        elif line.startswith("So the answer is"):
            processed_answer = line[-4:].strip().lower()
            if processed_answer in ['no.', 'yes.']:
                if processed_answer == 'no.':
                    model_prediction = False
                elif processed_answer == 'yes.':
                    model_prediction = True

    print("question: ", row["question"])
    print("facts: ", facts)
    print("thoughts: ", thoughts)

    insightful_score = int(
        input("Are all thoughts logical based only on these facts? Enter 1 for yes, 0 for no. "))
    insightful_scores.append(insightful_score)
    if model_prediction is not None:
        human_prediction = int(input(
            "What should the answer be based only on these thoughts? Enter 1 for yes, 0 for no. ")) == 1
        faithful_scores.append(1 if human_prediction ==
                               model_prediction else 0)
    else:
        print("The model failed to predict for this sample, skipping faithfulness test for this sample.")
    print('\n\n')

insightfulness = (sum(insightful_scores) / len(insightful_scores)) * 100
print(
    f"insightfulness score: {insightfulness} ; total samples evaluated: {len(insightful_scores)}")
faithfulness = (sum(faithful_scores) / len(faithful_scores)) * 100
print(
    f"faithfulness score: {faithfulness} ; total samples evaluated: {len(faithful_scores)}")
