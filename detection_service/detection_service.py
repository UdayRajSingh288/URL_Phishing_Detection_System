from pandas import DataFrame
from feature_ext import extract_features
from joblib import load

def make_dataframe(features):
	features_subset = []
	idx = [0, 1, 3, 6, 7, 9, 10, 29, 30, 31]
	for i in range(len(features)):
		if i not in idx:
			features_subset.append(features[i])
	features_subset = [features_subset]
	return DataFrame(features_subset)

def url_detection(url, model):
	features = extract_features(url)
	data_frame = make_dataframe(features)
	return model.predict(data_frame)

