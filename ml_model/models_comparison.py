import sys
from os import chdir
from pandas import read_csv
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

f = open(r'C:\Users\CaptainSwing817\projects\final_year_project\ml_model\model_comparison.txt', 'w')
sys.stdout = f

chdir(r'C:\Users\CaptainSwing817\projects\final_year_project\ml_model');


data_frame = read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')
data_frame = data_frame.drop(labels = ['FILENAME', 'URL', 'Domain', 'TLD', 'Title'], axis = 1)


data_frame.dropna()

X = data_frame.drop(labels = 'label', axis = 1)
Y = data_frame['label']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)

ros = RandomOverSampler(random_state = 42)
X_train, Y_train = ros.fit_resample(X_train, Y_train)

knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train, Y_train)

Y_pred = knn.predict(X_test)
print('\nK Nearest Neighbors\nAccuracy Score: ' + str(accuracy_score(Y_test, Y_pred)))
print('Classification Report\n' + classification_report(Y_test, Y_pred))

dt = DecisionTreeClassifier(random_state = 42)
dt.fit(X_train, Y_train)

Y_pred = dt.predict(X_test)
print('\nDecision Tree\nAccuracy Score: ' + str(accuracy_score(Y_test, Y_pred)))
print('Classification Report\n' + classification_report(Y_test, Y_pred))

nb = GaussianNB()
nb.fit(X_train, Y_train)

Y_pred = nb.predict(X_test)
print('\nNaive Bayes\nAccuracy Score: ' + str(accuracy_score(Y_test, Y_pred)))
print('Classification Report\n' + classification_report(Y_test, Y_pred))

rf = RandomForestClassifier(n_estimators = 100, random_state = 42)
rf.fit(X_train, Y_train)

Y_pred = rf.predict(X_test)
print('\nRandom Forest\nAccuracy Score: ' + str(accuracy_score(Y_test, Y_pred)))
print('Classification Report\n' + classification_report(Y_test, Y_pred))

svm = SVC(kernel = 'linear')
svm.fit(X_train, Y_train)

Y_pred = svm.predict(X_test)
print('\nSupport Vector Machine\nAccuracy Score: ' + str(accuracy_score(Y_test, Y_pred)))
print('Classification Report\n' + classification_report(Y_test, Y_pred))

f.close()