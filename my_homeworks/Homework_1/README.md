## Установка зависимостей 

    poetry install
    poetry shell
    
Или
    
    conda create -n hw1 python=3.10
    conda activate hw1
    pip install -r requirements.txt


## 
# Домашнее задание для лекции/семинара "Experiment management" 

## Задача:
Проведите эксперимент с обучением модели, используя такие инструменты для оптимизации ML-моделей и отслеживания экспериментов, как *Optuna*, *Hyperopt*, *Pandas*, *Polars* и *DVC*.

## Шаги

### Dataset
- Датасет лежит на гуглдиске, DVC скачивает его во время прогона пайплайна.

### Model Selection
- Выберите модель/архитектуру. Выбрал - XGBClassifier, в ноутбучках тестил разное.

### Hyperparameter Optimization
- Выполнил поиск наилучших значений для гиперпараметров для моей модели с помощью Optuna.<br>
- Сделал эвалюацию моей модели/моделей в main.py. 

### Experiment Tracking with DVC
- Настройл DVC - репозиторий 
- Залогировал в нем все изменения, которые случились в ходе эксперимента: hyperparameters, evaluation metrics, dataset versions, model versions, etc
- Короткий summary report моих экспериментов в отдельном файле (json) - в папке report.

### Оценки - это я для себя):
- [x] Dataset loading and model selection: 5 points
- [x] Hyperparameter optimization: 5 points
- [x] DVC experiment tracking: 5 points
- [x] Evaluation and comparison: 5 points
- [x] Code organization and submission: 5 points
- [x] Summary report: 5 points

Итого: максимум 30 баллов

