import os
import sys
import jsonlines
import openai
from dotenv import load_dotenv
from tqdm import tqdm

from utils import load_data
import constants

# env
load_dotenv()

# api keys
openai.api_key = os.getenv('OPENAI_API_KEY')

# model
model_name = constants.LLM_MODEL_NAMES.TEXT_DAVINCI_003.value

# prompt file version
# careful, new predictions might get appended to existing predictions file
prompt_file_version = 'ccoft'

# question separator in prompt
question_separator = '\n\n'

# load dataset
dataset_name = constants.DATASETS.STRATEGY_QA.value
# Using the 'dev' split to test because the original
# COT paper has some samples from the 'test' split in their prompt.
# But we chose our prompt samples from the 'train' split.
split = 'dev'
dataset_frn = f"datasets/{dataset_name}/{split}.jsonl"
dataset = load_data(dataset_frn)

# prepare output file
output_dir = f"output_dir/{dataset_name}/{split}/{model_name}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_fwn = f"{output_dir}/predictions_{prompt_file_version}.jsonl"

# prompt prefix
prompt_prefix = ''
prompt_path = f"prompt/{dataset_name}/{prompt_file_version}.txt"
with open(prompt_path, 'r', encoding='utf-8') as fr:
    prompt_prefix = fr.read()

# initialize batch variables
# using batches to optimize around OpenAI RPM limits instead of implementing retries
batch_prompts = []
batch_question_ids = []
batch_questions = []
batch_gold_answers = []
batch_size = 2
total_samples_num = 4
predictions = []

# prediction loop
for i, example in tqdm(enumerate(dataset), file=sys.stdout):
    if i >= total_samples_num:
        # only run for total_samples_num samples
        break

    question = example["question"]
    question_id = int(example["id"])
    batch_question_ids.append(question_id)
    batch_questions.append(question)
    batch_gold_answers.append(example["answer"])
    batch_prompts.append(f"{prompt_prefix}{question_separator}Q: {question}\n")

    if i % batch_size == batch_size-1:
        # batch is ready
        # pass the current batch to OpenAI API
        response = openai.Completion.create(
            model=model_name,
            prompt=batch_prompts,
            max_tokens=1000,
            temperature=0,
            stop=question_separator
        )
        # store batch predictions
        for choice in response.choices:
            row = {"id": batch_question_ids[choice.index],
                   "question": batch_questions[choice.index],
                   "answer": choice.text,
                   "gold_answer": batch_gold_answers[choice.index],
                   }
            predictions.append(row)
        # empty batch arrays
        batch_prompts = []
        batch_question_ids = []
        batch_questions = []
        batch_gold_answers = []

# append predictions to file
with open(output_fwn, 'a') as fw:
    writer = jsonlines.Writer(fw, flush=True)
    for row in predictions:
        writer.write(row)
