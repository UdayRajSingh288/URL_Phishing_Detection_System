# import sys
from pandas import read_csv
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
#from joblib import dump


# fl = open('final_model.txt', 'w')
# sys.stdout = fl

data_frame = read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')
data_frame = data_frame.drop(labels = ['FILENAME', 'URL', 'Domain', 'TLD', 'URLSimilarityIndex', 'TLDLegitimateProb', 'URLCharProb', 'Title', 'DomainTitleMatchScore', 'URLTitleMatchScore'], axis = 1)

data_frame.dropna()

X = data_frame.drop(labels = 'label', axis = 1)
Y = data_frame['label']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)

ros = RandomOverSampler(random_state = 42)
X_train, Y_train = ros.fit_resample(X_train, Y_train)

rf = RandomForestClassifier(n_estimators = 100, random_state = 42)
rf.fit(X_train, Y_train)

Y_pred = rf.predict(X_test)
print('\nRandom Forest\nAccuracy Score: ' + str(accuracy_score(Y_test, Y_pred)))
print('Classification Report\n' + classification_report(Y_test, Y_pred))

# fl.close()

#dump(rf, 'url_phishing_model.joblib')