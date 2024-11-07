from os import chdir
from pandas import read_csv

chdir(r'C:\Users\CaptainSwing817\projects\final_year_project\ml_model');

data_frame = read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')

'''
TO OBTAIN DATASET INFORMATION IN A FILE

import sys
dset_info_file = open('dataset_info.txt', 'w')
sys.stdout = dset_info_file
data_frame.info()
dset_info_file.close()
'''