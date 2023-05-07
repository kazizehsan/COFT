# Chain of Facts and Thoughts

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
1. Copy `env.example` to `.env` and update variables.

### View accuracy on current predictions
```
python src/report_accuracy.py
```

### View complex samples for Complex COT
```
python src/pick_samples_for_ccot.py
```
Note: In order to pick complex samples, we have followed the methodology from Complexity-Based Prompting For Multi-Step Reasoning by Fu et al. (https://arxiv.org/abs/2210.00720).

### Run predictions
```
python src/run_predictions.py
```
Note: On second run, new predictions will get appended to existing predictions file.
