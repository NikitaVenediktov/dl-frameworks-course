'''
итоговая работка на первую дз
'''

import optuna
import subprocess

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from datetime import datetime
from preprocess import load_data
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import json

# Load and split data
seed = 2023
df_pd = load_data()
X = df_pd['comment']
y = df_pd['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seed)

count_vect = CountVectorizer(stop_words='english')
transformer = TfidfTransformer(norm='l2', sublinear_tf=True)

x_train_counts = count_vect.fit_transform(X_train)
x_train_tfidf = transformer.fit_transform(x_train_counts)
x_test_counts = count_vect.transform(X_test)
x_test_tfidf = transformer.transform(x_test_counts)


def objective(trial, ):
    """Define the objective function"""

    params = {
        'objective': 'binary:logistic',
        'max_depth': trial.suggest_int('max_depth', 1, 9),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 1.0),
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_loguniform('gamma', 1e-8, 1.0),
        'subsample': trial.suggest_loguniform('subsample', 0.01, 1.0),
        'colsample_bytree': trial.suggest_loguniform('colsample_bytree', 0.01, 1.0),
        'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-8, 1.0),
        'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-8, 1.0),
        'eval_metric': 'logloss',
        'use_label_encoder': False
    }

    # Fit the model
    optuna_model = XGBClassifier(**params)
    optuna_model.fit(x_train_tfidf, y_train)

    # Make predictions
    y_pred = optuna_model.predict(x_test_tfidf)

    # Evaluate predictions
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Create and run the Optuna optimization
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=25)

# Get the best hyperparameters
best_params = study.best_params
best_accuracy = study.best_value

print('Best Parameters:', best_params)
print('Best Accuracy:', best_accuracy)

# Fit the pipeline with the best parameters on the entire dataset
model = XGBClassifier(**best_params)
model.fit(x_train_tfidf, y_train)
# Save model
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
model_filename = f'model/model_{timestamp}.joblib'
joblib.dump(model, model_filename)

# Create a report
report = {
    'Text': 'Никитос продолжай)!',
    'Model': 'XGBClassifier',
    'timestamp': timestamp,
    'best_params': best_params,
    'best_accuracy': best_accuracy,
    'model_version': model_filename
}

# Save the report as a JSON file
report_filename = f'report/report_{timestamp}.json'
with open(report_filename, 'w') as f:
    json.dump(report, f)


# DVC commands to track
subprocess.run(['dvc', 'add', report_filename])
subprocess.run(['dvc', 'add', model_filename])
subprocess.run(['dvc', 'commit', report_filename, model_filename])
subprocess.run(['dvc', 'push'])
