
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



# %% 1 - import required libraries
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression

from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler

from cowboysmall.data.file import read_master_file
from cowboysmall.feature import COLUMNS, INDICATORS, RATIOS
from cowboysmall.feature.indicators import get_indicators, get_ratios
from cowboysmall.model.imbalance import imbalance_remedy_evaluation



# %% 2 -
ALL_COLS = COLUMNS + RATIOS + INDICATORS
FEATURES = ["IXIC_DAILY_RETURNS", "HSI_DAILY_RETURNS", "N225_DAILY_RETURNS", "VIX_DAILY_RETURNS", "DJI_RSI", "DJI_TSI"]



# %% 2 -
master = read_master_file()



# %% 2 -
master["NSEI_OPEN_DIR"] = np.where(master["NSEI_OPEN"] > master["NSEI_CLOSE"].shift(), 1, 0)



# %% 2 -
master = get_ratios(master)
master = get_indicators(master)



# %% 2 -
counts = master['NSEI_OPEN_DIR'].value_counts().reset_index()
counts.columns = ['NSEI_OPEN_DIR', 'Freq']
print(counts)
#    NSEI_OPEN_DIR  Freq
# 0              1  1064
# 1              0   499



# %% 2 -
print((counts["Freq"][0] / (counts["Freq"][0] + counts["Freq"][1])).round(3))
# 0.681



# %% 3 -
data = pd.concat([master["NSEI_OPEN_DIR"].shift(-1), master[ALL_COLS]], axis = 1)
data.dropna(inplace = True)
data.head()



# %% 3 -
X = data.loc[:, FEATURES]
y = data.loc[:, "NSEI_OPEN_DIR"]


# %% 3 -
results = imbalance_remedy_evaluation(None, LogisticRegression(max_iter = 1000, class_weight = "balanced"), X, y)

print()
print(' LogisticRegression - class_weight: balanced')
print()
print(f'     AUC ROC: {results['AUC']:.3f}')
print()
print(f'   Threshold: {results['THRESHOLD']}')
print()
print(f'    Accuracy: {results['ACCURACY']:.3f}')
print(f" Sensitivity: {results['SENSITIVITY']:.3f}%")
print(f" Specificity: {results['SPECIFICITY']:.3f}%")
print()

#  LogisticRegression - class_weight: balanced
# 
#      AUC ROC: 0.749
# 
#    Threshold: 0.403
# 
#     Accuracy: 0.780
#  Sensitivity: 87.980%
#  Specificity: 56.700%


# %% 3 -
results = imbalance_remedy_evaluation(RandomUnderSampler(random_state = 0), LogisticRegression(max_iter = 1000), X, y)

print()
print(' RandomUnderSampler')
print()
print(f'     AUC ROC: {results['AUC']:.3f}')
print()
print(f'   Threshold: {results['THRESHOLD']}')
print()
print(f'    Accuracy: {results['ACCURACY']:.3f}')
print(f" Sensitivity: {results['SENSITIVITY']:.3f}%")
print(f" Specificity: {results['SPECIFICITY']:.3f}%")
print()

#  RandomUnderSampler
# 
#      AUC ROC: 0.742
# 
#    Threshold: 0.461
# 
#     Accuracy: 0.689
#  Sensitivity: 81.610%
#  Specificity: 58.720%



# %% 3 -
results = imbalance_remedy_evaluation(RandomOverSampler(random_state = 0), LogisticRegression(max_iter = 1000), X, y)

print()
print(' RandomOverSampler')
print()
print(f'     AUC ROC: {results['AUC']:.3f}')
print()
print(f'   Threshold: {results['THRESHOLD']}')
print()
print(f'    Accuracy: {results['ACCURACY']:.3f}')
print(f" Sensitivity: {results['SENSITIVITY']:.3f}%")
print(f" Specificity: {results['SPECIFICITY']:.3f}%")
print()

#  RandomOverSampler
# 
#      AUC ROC: 0.719
# 
#    Threshold: 0.419
# 
#     Accuracy: 0.680
#  Sensitivity: 82.690%
#  Specificity: 53.140%


# %% 3 -
results = imbalance_remedy_evaluation(SMOTE(random_state = 0), LogisticRegression(max_iter = 1000), X, y)

print()
print(' SMOTE')
print()
print(f'     AUC ROC: {results['AUC']:.3f}')
print()
print(f'   Threshold: {results['THRESHOLD']}')
print()
print(f'    Accuracy: {results['ACCURACY']:.3f}')
print(f" Sensitivity: {results['SENSITIVITY']:.3f}%")
print(f" Specificity: {results['SPECIFICITY']:.3f}%")
print()

#  SMOTE
# 
#      AUC ROC: 0.721
# 
#    Threshold: 0.396
# 
#     Accuracy: 0.684
#  Sensitivity: 85.100%
#  Specificity: 51.690%


# %% 3 -
results = imbalance_remedy_evaluation(ADASYN(random_state = 0), LogisticRegression(max_iter = 1000), X, y)

print()
print(' ADASYN')
print()
print(f'     AUC ROC: {results['AUC']:.3f}')
print()
print(f'   Threshold: {results['THRESHOLD']}')
print()
print(f'    Accuracy: {results['ACCURACY']:.3f}')
print(f" Sensitivity: {results['SENSITIVITY']:.3f}%")
print(f" Specificity: {results['SPECIFICITY']:.3f}%")
print()


#  ADASYN
# 
#      AUC ROC: 0.729
# 
#    Threshold: 0.503
# 
#     Accuracy: 0.663
#  Sensitivity: 62.790%
#  Specificity: 69.860%
