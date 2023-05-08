# Chain of Facts and Thoughts (COFT)

## Usage
### Installation (Mac)
1. Make sure `virtualenv` is installed on `PATH`. Then create an environment.
```
virtualenv venv
```
2. Activate environment
```
source venv/vin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```

### Create .env
1. Copy `env.example` to `.env`.
2. Insert OpenAI API Key.

### View accuracy on current predictions
```
python src/report_accuracy.py
```
Note: By default, accuracy of the Complex COFT predictions from 2023-05-06 will be printed.

### Participate in an insightfulness and faithfulness evaluation
```
python src/insightfulness_faithfulness_eval.py
```
Note: You will be presented with a set of randomly picked 50 COFT prediction samples one by one. For each question, you will be shown the model generated facts and thoughts. First, you will have to answer if the thoughts are insightful based on the facts shown. Second, you will have to guess the model's prediction based on the thoughts shown. After running through all the samples, you will be presented with an insightfulness and faithfulness score for this sample set.

### View complex samples for prompt crafting
```
python src/pick_complex_samples.py
```
Note: In order to pick complex samples, we have followed the methodology from Complexity-Based Prompting For Multi-Step Reasoning by Fu et al. (https://arxiv.org/abs/2210.00720).

### Run predictions
```
python src/run_predictions.py
```
Note: On second run, new predictions will get appended to existing predictions file. By default, the Complex COFT prompt will be used.
