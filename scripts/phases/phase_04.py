
"""

Global market indices of interest:

    NSEI:  Nifty 50
    DJI:   Dow Jones Index
    IXIC:  Nasdaq
    HSI:   Hang Seng
    N225:  Nikkei 225
    GDAXI: Dax
    VIX:   Volatility Index

"""



# %% 0 - import required libraries
import pandas as pd
import numpy as np

from sklearn.metrics import classification_report, roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from cowboysmall.data.file import read_master_file
from cowboysmall.feature import ALL_COLS
from cowboysmall.feature.indicators import get_indicators, get_ratios
from cowboysmall.plots import plt, sns



# %% 1 -
FEATURES = ["IXIC_DAILY_RETURNS", "HSI_DAILY_RETURNS", "N225_DAILY_RETURNS", "VIX_DAILY_RETURNS", "DJI_RSI", "DJI_TSI"]



# %% 1 -
plt.plot_setup()
sns.sns_setup()



# %% 1 - read master data + create NSEI_OPEN_DIR
data = read_master_file()
data = get_ratios(data)
data = get_indicators(data)



# %% 1 -
data["NSEI_OPEN_DIR"] = np.where(data["NSEI_OPEN"] > data["NSEI_CLOSE"].shift(), 1, 0)
# data["NSEI_OPEN_DIR"] = np.where(data["NSEI_OPEN"] > data["NSEI_CLOSE"].shift(), 1, 0)


# %% 1 -
data = pd.concat([data["NSEI_OPEN_DIR"].shift(-1), data[ALL_COLS]], axis = 1)
data = data.dropna()




# %% 1 -
X = data[FEATURES]
y = data["NSEI_OPEN_DIR"]



# %% 4 -
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1337)



# %% 4 -
def model_metrics(X_train, X_test, y_train, y_test, model, description):
    model.fit(X_train, y_train)

    y_train_pred_prob = model.predict_proba(X_train)
    train_fpr, train_tpr, train_thresholds = roc_curve(y_train, y_train_pred_prob[:, 1])

    y_test_pred_prob = model.predict_proba(X_test)
    test_fpr, test_tpr, _ = roc_curve(y_test, y_test_pred_prob[:, 1])

    optimal_threshold  = round(train_thresholds[np.argmax(train_tpr - train_fpr)], 3)

    train_auc_roc      = round(roc_auc_score(y_train, y_train_pred_prob[:, 1]), 3)
    y_train_pred_class = np.where(y_train_pred_prob[:, 1] <= optimal_threshold,  0, 1)
    train_table        = pd.crosstab(y_train_pred_class, y_train)
    train_sensitivity  = round((train_table.iloc[1, 1] / (train_table.iloc[0, 1] + train_table.iloc[1, 1])) * 100, 2)
    train_specificity  = round((train_table.iloc[0, 0] / (train_table.iloc[0, 0] + train_table.iloc[1, 0])) * 100, 2)

    test_auc_roc      = round(roc_auc_score(y_test, y_test_pred_prob[:, 1]), 3)
    y_test_pred_class = np.where(y_test_pred_prob[:, 1] <= optimal_threshold,  0, 1)
    test_table        = pd.crosstab(y_test_pred_class, y_test)
    test_sensitivity  = round((test_table.iloc[1, 1] / (test_table.iloc[0, 1] + test_table.iloc[1, 1])) * 100, 2)
    test_specificity  = round((test_table.iloc[0, 0] / (test_table.iloc[0, 0] + test_table.iloc[1, 0])) * 100, 2)

    plt.roc_curve(train_fpr, train_tpr, f"{description} - Train Data")
    plt.roc_curve(test_fpr, test_tpr, f"{description} - Test Data")

    print()

    print(classification_report(y_train, y_train_pred_class))
    print(f"\nTrain Data - Confusion Matrix:\n{train_table}\n")

    print(classification_report(y_test, y_test_pred_class))
    print(f"\n Test Data - Confusion Matrix:\n{test_table}\n")

    print()

    print(f"Train Data - Sensitivity for cut-off {optimal_threshold}: {train_sensitivity}%")
    print(f" Test Data - Sensitivity for cut-off {optimal_threshold}: {test_sensitivity}%\n")

    print(f"Train Data - Specificity for cut-off {optimal_threshold}: {train_specificity}%")
    print(f" Test Data - Specificity for cut-off {optimal_threshold}: {test_specificity}%\n")

    print(f"Train Data - AUC ROC: {train_auc_roc}")
    print(f" Test Data - AUC ROC: {test_auc_roc}\n")


# %% 4 -
model = LogisticRegression(max_iter = 1000, random_state = 1337)
model_metrics(X_train, X_test, y_train, y_test, model, "Logistic Regression")
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.53      0.68      0.60       391
#          1.0       0.83      0.72      0.77       829
# 
#     accuracy                           0.71      1220
#    macro avg       0.68      0.70      0.68      1220
# weighted avg       0.73      0.71      0.71      1220
# 
# 
# Train Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0              265  233
# 1              126  596
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.53      0.65      0.58        97
#          1.0       0.82      0.73      0.77       208
# 
#     accuracy                           0.70       305
#    macro avg       0.67      0.69      0.67       305
# weighted avg       0.72      0.70      0.71       305
# 
# 
#  Test Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0               63   57
# 1               34  151
# 
# 
# Train Data - Sensitivity for cut-off 0.684: 71.89%
#  Test Data - Sensitivity for cut-off 0.684: 72.6%
# 
# Train Data - Specificity for cut-off 0.684: 67.77%
#  Test Data - Specificity for cut-off 0.684: 64.95%
# 
# Train Data - AUC ROC: 0.753
#  Test Data - AUC ROC: 0.752



# %% 4 -
model = GaussianNB()
model_metrics(X_train, X_test, y_train, y_test, model, "Naive Bayes")
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.63      0.51      0.56       391
#          1.0       0.79      0.86      0.82       829
# 
#     accuracy                           0.75      1220
#    macro avg       0.71      0.68      0.69      1220
# weighted avg       0.74      0.75      0.74      1220
# 
# 
# Train Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0              199  117
# 1              192  712
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.61      0.51      0.55        97
#          1.0       0.79      0.85      0.82       208
# 
#     accuracy                           0.74       305
#    macro avg       0.70      0.68      0.69       305
# weighted avg       0.73      0.74      0.73       305
# 
# 
#  Test Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0               49   31
# 1               48  177
# 
# 
# Train Data - Sensitivity for cut-off 0.65: 85.89%
#  Test Data - Sensitivity for cut-off 0.65: 85.1%
# 
# Train Data - Specificity for cut-off 0.65: 50.9%
#  Test Data - Specificity for cut-off 0.65: 50.52%
# 
# Train Data - AUC ROC: 0.739
#  Test Data - AUC ROC: 0.721



# %% 4 -
scaler = StandardScaler()
scaler.fit(X_train)

model = KNeighborsClassifier(leaf_size = 10, n_neighbors = 30)
model_metrics(scaler.transform(X_train), scaler.transform(X_test), y_train, y_test, model, "KNN")
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.50      0.70      0.59       391
#          1.0       0.83      0.68      0.74       829
# 
#     accuracy                           0.68      1220
#    macro avg       0.67      0.69      0.67      1220
# weighted avg       0.72      0.68      0.69      1220
# 
# 
# Train Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0              274  269
# 1              117  560
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.51      0.67      0.58        97
#          1.0       0.82      0.70      0.76       208
# 
#     accuracy                           0.69       305
#    macro avg       0.67      0.69      0.67       305
# weighted avg       0.72      0.69      0.70       305
# 
# 
#  Test Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0               65   62
# 1               32  146
# 
# 
# Train Data - Sensitivity for cut-off 0.7: 67.55%
#  Test Data - Sensitivity for cut-off 0.7: 70.19%
# 
# Train Data - Specificity for cut-off 0.7: 70.08%
#  Test Data - Specificity for cut-off 0.7: 67.01%
# 
# Train Data - AUC ROC: 0.765
#  Test Data - AUC ROC: 0.733





# %% 4 -
model = DecisionTreeClassifier(max_depth = 10, min_samples_split = 0.4, splitter = "random", random_state = 1337)
model_metrics(X_train, X_test, y_train, y_test, model, "Decision Tree")
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.46      0.76      0.57       391
#          1.0       0.83      0.58      0.68       829
# 
#     accuracy                           0.64      1220
#    macro avg       0.65      0.67      0.63      1220
# weighted avg       0.71      0.64      0.65      1220
# 
# 
# Train Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0              296  350
# 1               95  479
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.47      0.78      0.59        97
#          1.0       0.86      0.60      0.70       208
# 
#     accuracy                           0.66       305
#    macro avg       0.67      0.69      0.65       305
# weighted avg       0.73      0.66      0.67       305
# 
# 
#  Test Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0               76   84
# 1               21  124
# 
# 
# Train Data - Sensitivity for cut-off 0.794: 57.78%
#  Test Data - Sensitivity for cut-off 0.794: 59.62%
# 
# Train Data - Specificity for cut-off 0.794: 75.7%
#  Test Data - Specificity for cut-off 0.794: 78.35%
# 
# Train Data - AUC ROC: 0.715
#  Test Data - AUC ROC: 0.725



# %% 4 -
model = RandomForestClassifier(max_depth = 10, min_samples_split = 0.2, random_state = 1337)
model_metrics(X_train, X_test, y_train, y_test, model, "Random Forest")
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.53      0.75      0.62       391
#          1.0       0.85      0.68      0.76       829
# 
#     accuracy                           0.71      1220
#    macro avg       0.69      0.72      0.69      1220
# weighted avg       0.75      0.71      0.72      1220
# 
# 
# Train Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0              294  262
# 1               97  567
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.50      0.70      0.58        97
#          1.0       0.83      0.67      0.74       208
# 
#     accuracy                           0.68       305
#    macro avg       0.66      0.68      0.66       305
# weighted avg       0.72      0.68      0.69       305
# 
# 
#  Test Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0               68   69
# 1               29  139
# 
# 
# Train Data - Sensitivity for cut-off 0.721: 68.4%
#  Test Data - Sensitivity for cut-off 0.721: 66.83%
# 
# Train Data - Specificity for cut-off 0.721: 75.19%
#  Test Data - Specificity for cut-off 0.721: 70.1%
# 
# Train Data - AUC ROC: 0.783
#  Test Data - AUC ROC: 0.746



# %% 4 -
model = SVC(C = 1, kernel = "linear", probability = True, random_state = 1337)
model_metrics(X_train, X_test, y_train, y_test, model, "SVC")
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.54      0.66      0.60       391
#          1.0       0.82      0.74      0.78       829
# 
#     accuracy                           0.71      1220
#    macro avg       0.68      0.70      0.69      1220
# weighted avg       0.73      0.71      0.72      1220
# 
# 
# Train Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0              259  219
# 1              132  610
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.54      0.65      0.59        97
#          1.0       0.82      0.75      0.78       208
# 
#     accuracy                           0.71       305
#    macro avg       0.68      0.70      0.69       305
# weighted avg       0.73      0.71      0.72       305
# 
# 
#  Test Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0               63   53
# 1               34  155
# 
# 
# Train Data - Sensitivity for cut-off 0.682: 73.58%
#  Test Data - Sensitivity for cut-off 0.682: 74.52%
# 
# Train Data - Specificity for cut-off 0.682: 66.24%
#  Test Data - Specificity for cut-off 0.682: 64.95%
# 
# Train Data - AUC ROC: 0.753
#  Test Data - AUC ROC: 0.743



# %% 4 -
scaler = MinMaxScaler()
scaler.fit(X_train)

model = MLPClassifier(alpha = 0.001, max_iter = 1000, random_state = 1337)
model_metrics(scaler.transform(X_train), scaler.transform(X_test), y_train, y_test, model, "MLP")
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.57      0.62      0.60       391
#          1.0       0.81      0.78      0.80       829
# 
#     accuracy                           0.73      1220
#    macro avg       0.69      0.70      0.70      1220
# weighted avg       0.74      0.73      0.73      1220
# 
# 
# Train Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0              242  180
# 1              149  649
# 
#               precision    recall  f1-score   support
# 
#          0.0       0.56      0.63      0.59        97
#          1.0       0.82      0.77      0.79       208
# 
#     accuracy                           0.72       305
#    macro avg       0.69      0.70      0.69       305
# weighted avg       0.73      0.72      0.73       305
# 
# 
#  Test Data - Confusion Matrix:
# NSEI_OPEN_DIR  0.0  1.0
# row_0                  
# 0               61   48
# 1               36  160
# 
# 
# Train Data - Sensitivity for cut-off 0.665: 78.29%
#  Test Data - Sensitivity for cut-off 0.665: 76.92%
# 
# Train Data - Specificity for cut-off 0.665: 61.89%
#  Test Data - Specificity for cut-off 0.665: 62.89%
# 
# Train Data - AUC ROC: 0.753
#  Test Data - AUC ROC: 0.736
