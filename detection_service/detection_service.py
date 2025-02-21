from pandas import DataFrame
from feature_ext import extract_features
from joblib import load
from flask import Flask, jsonify, request
from flask_restful import Resource, Api


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
	if features:
		data_frame = make_dataframe(features)
		res = model.predict(data_frame)
		if res[0] == 1:
			return 'UNSAFE'
		else:
			return 'SAFE'
	else:
		return 'INVALID URL'

model = None

class Service(Resource):
	def post(self):
		data = request.get_json()
		st = url_detection(data['url'], model)
		return jsonify({'STATUS': st})


app = Flask(__name__)
api = Api(app)
api.add_resource(Service, '/')

if __name__ == '__main__':
	model = load('url_phishing_model.joblib')
	app.run(debug = True, port = 8080)