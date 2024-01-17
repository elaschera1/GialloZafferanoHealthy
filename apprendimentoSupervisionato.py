from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier, \
    AdaBoostClassifier, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, PrecisionRecallDisplay, RocCurveDisplay, \
    confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV, learning_curve
from sklearn import metrics
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from stop_words import get_stop_words
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier, MLPRegressor
import seaborn as sns
from matplotlib import pyplot as plt
import warnings

warnings.filterwarnings("ignore")

path_dataset = "Dataset/GialloZafferanoDatasetProlog.csv"

df = pd.read_csv(path_dataset)

vectorizer = CountVectorizer(stop_words=get_stop_words('it'))

df_testo_vettorizzato = pd.DataFrame(vectorizer.fit_transform(df['Ingredienti']).toarray(),
                                     columns=vectorizer.get_feature_names_out())
df_testo_vettorizzato2 = pd.DataFrame(vectorizer.fit_transform(df['Descrizione']).toarray(),
                                      columns=vectorizer.get_feature_names_out())

colonne = ['Grassi(g)', 'Carboidrati(g)', 'Proteine(g)', 'Energia(kcal)', 'GrassiSaturi(g)', 'Fibre(g)',
           'Colesterolo(g)', 'Sodio(g)', 'ricettaSalutare']

X = pd.concat([df[colonne], df_testo_vettorizzato], axis=1)
y = df['Vegano']

models = {
    'Logistic Regression': (LogisticRegression(), {'C': [0.001, 0.01, 0.1, 1, 10, 100]}),
    'Decision Tree': (DecisionTreeClassifier(), {'max_depth': [None, 5, 10, 15], 'min_samples_split': [2, 5, 10]}),
    'RandomForestClassifier': (RandomForestClassifier(), {'n_estimators': [50, 100], 'max_depth': [None, 5, 10]}),
    'GrandientBoostingClassifier': (GradientBoostingClassifier(), {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1, 0.2]}),
    'AdaBoostClassifier': (AdaBoostClassifier(), {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1, 0.2]})
}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Inizio Task 1: Classificazione")
print(" Eseguo Grid Search con Kfold-cross-validation")

best_models = {}

for model_name, (model, params) in models.items():
    print(" Valutazione modello", model_name)
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    grid_search = GridSearchCV(model, params, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_

    best_model = grid_search.best_estimator_

    test_accuracy = best_model.score(X_test, y_test)
    y_pred = best_model.predict(X_test)
    best_models[model_name] = {'model': best_model, 'best_params': best_params, 'test_accuracy': test_accuracy,
                               'report': classification_report(y_test, y_pred)}

    cm = confusion_matrix(y_test, y_pred, labels=best_model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_model.classes_)
    disp.plot()
    plt.savefig("Img/" + model_name + 'ConfusionMatrix.png')
    plt.show()

    RocCurveDisplay.from_estimator(best_model, X_test, y_test)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.savefig("Img/" + model_name + 'RocCurve.png')
    plt.show()

    PrecisionRecallDisplay.from_estimator(best_model, X_test, y_test)
    plt.savefig("Img/" + model_name + 'PrecisionRecallCurve.png')
    plt.show()

for model_name, info in best_models.items():
    print(f"Modello: {model_name}")
    print(f"Migliori parametri: {info['best_params']}")
    print(f"Accuratezza sul set di test: {info['test_accuracy']:.2f}")
    print(info['report'])
    print("=" * 50)

print("Fine Task 1")

print("Inizio Task 2: Classificazione multiclasse")

colonne = ['Cottura', 'Dosi', 'Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Proteine(g)', 'Grassi(g)',
           'GrassiSaturi(g)', 'Fibre(g)', 'Colesterolo(g)', 'Sodio(g)', 'SenzaGlutine', 'SenzaLattosio', 'Vegano']
df_combinato = pd.concat([df[colonne], df_testo_vettorizzato, df_testo_vettorizzato2], axis=1)

X = df_combinato[:]
y = df['Difficoltà']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest Classifier': RandomForestClassifier(),
    'Gradient Boosting Classifier': GradientBoostingClassifier(),
    'AdaBoostClassifier': AdaBoostClassifier()
}

param_grid = {
    'Logistic Regression': {'estimator__C': [0.001, 0.01, 0.1, 1, 10, 100]},
    'Decision Tree': {'estimator__max_depth': [None, 5, 10, 15], 'estimator__min_samples_split': [2, 5, 10]},
    'Random Forest Classifier': {'estimator__n_estimators': [50, 100], 'estimator__max_depth': [None, 5, 10]},
    'Gradient Boosting Classifier': {'estimator__n_estimators': [50, 100],
                                     'estimator__learning_rate': [0.01, 0.1, 0.2]},
    'AdaBoostClassifier': {'estimator__n_estimators': [50, 100], 'estimator__learning_rate': [0.01, 0.1, 0.2]}
}

best_models = {}

for model_name, model in models.items():
    print(" Valutazione modello", model_name)
    params = param_grid[model_name]
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    grid_search = GridSearchCV(OneVsRestClassifier(model), params, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_

    best_model = grid_search.best_estimator_

    test_accuracy = best_model.score(X_test, y_test)
    y_pred = best_model.predict(X_test)
    best_models[model_name] = {'model': best_model, 'best_params': best_params, 'test_accuracy': test_accuracy,
                               'report': classification_report(y_test, y_pred)}

    cm = confusion_matrix(y_test, y_pred, labels=best_model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_model.classes_)
    disp.plot()
    plt.savefig('Img/OneVsRestClassifier' + model_name + 'ConfusionMatrix.png')
    plt.show()

for model_name, info in best_models.items():
    print(f"OneVsRestClassifier con modello: {model_name}")
    print(f"Migliori parametri: {info['best_params']}")
    print(f"Accuratezza sul set di test: {info['test_accuracy']:.2f}")
    print(info['report'])
    print("=" * 50)

print("Fine Task 2")

print("Inizio Task 3: Regressione Lineare")

colonne = ['Grassi(g)', 'Carboidrati(g)', 'Proteine(g)', 'Energia(kcal)', 'GrassiSaturi(g)', 'Fibre(g)',
           'Colesterolo(g)', 'Sodio(g)']

X = pd.concat([df[colonne], df_testo_vettorizzato], axis=1)
y = df['Zuccheri(g)']

models = {
    'Linear Regression': (LinearRegression(), {}),
    'Decision Tree': (DecisionTreeRegressor(), {'max_depth': [None, 5, 10, 15], 'min_samples_split': [2, 5, 10]}),
    'RandomForestRegressor': (RandomForestRegressor(), {'n_estimators': [50, 100], 'max_depth': [None, 10, 20]}),
    'GradientBoostingRegressor': (GradientBoostingRegressor(), {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1, 0.2]}),
    'AdaBoostClassifier': (AdaBoostRegressor(), {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1, 0.2]})
}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(" Eseguo Grid Search con Kfold-cross-validation")
# Esegui la grid search per ciascun modello


best_models = {}

for model_name, (model, params) in models.items():
    print(" Valutazione modello", model_name)
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    grid_search = GridSearchCV(model, params, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_

    best_model = grid_search.best_estimator_

    test_accuracy = best_model.score(X_test, y_test)
    y_pred = best_model.predict(X_test)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = metrics.r2_score(y_test, y_pred)

    best_models[model_name] = {'model': best_model, 'best_params': best_params, 'test_accuracy': test_accuracy,
                               'MSE': mse, 'RMSE': rmse, 'R2': r2}

for model_name, info in best_models.items():
    print(f"Modello: {model_name}")
    print(f"Migliori parametri: {info['best_params']}")
    print(f"Accuratezza sul set di test: {info['test_accuracy']:.2f}")
    print(f"MSE: {info['MSE']:.2f}")
    print(f"RMSE: {info['RMSE']:.2f}")
    print(f"R2: {info['R2']:.2f}")
    print("=" * 50)

print("Fine Task 3")

