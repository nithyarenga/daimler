import pandas as pd
from tabulate import tabulate
#import xlrd
#import time
from datetime import datetime
import hashlib
import os
import pickle

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

def fn_read_pdxls(filename):
    xl = pd.ExcelFile(filename)
    all_sheets = xl.sheet_names
    all_sheets_data = {}
    for ind_sheet in all_sheets:
        all_sheets_data[ind_sheet] = pd.read_excel(filename, index_col=0, sheet_name=ind_sheet)
    return all_sheets_data
# Setup
working_dir = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(working_dir, 'data')
xls_filename = 'alexa_questions.xlsx'
sheet_db = fn_read_pdxls(os.path.join(data_path, xls_filename))

# Watson NLU
key = 'dC-x1imeqNO8U2FQ_eC0tc6IKwWf6DcTVsBcf-XX1uhe'
gateway = 'https://gateway.watsonplatform.net/natural-language-understanding/api'

service = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url=gateway,
    iam_apikey=key)

def fn_write_pdxls(data, filename):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter', options={'strings_to_urls': False})
    for ind_sheet, df in data.items():
        df.to_excel(writer, ind_sheet, engine='xlsxwriter')
    writer.save()
    return True



def get_nlu_response(statement, cutoff = 0.5):
    hash_code = str(hashlib.sha224(statement.encode('utf-8')).hexdigest()) + '.pickle'
    hash_filepath = os.path.join(data_path, hash_code)
    if os.path.isfile(hash_filepath):
        print("loading Cache")
        response = pickle.load(open(hash_filepath, 'rb'))
    else:
        response = service.analyze(text=statement,
                features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions())).get_result()
        pickle.dump(response, open(hash_filepath, 'wb'))
    entities = []
    for ind_entity in response['entities']:
        if ind_entity['relevance'] > cutoff:
            entities.append(ind_entity['text'])
    keywords = []
    for ind_keyword in response['keywords']:
        if ind_keyword['relevance'] > cutoff:
            keywords.append(ind_keyword['text'])
    return ', '.join(entities), ', '.join(keywords)


def fnget_recent_solutions(no_transactions=1):
    sheet_name = 'Solutions'
    sheet_db[sheet_name]['Datetime'] = pd.to_datetime(sheet_db[sheet_name]['Datetime'])
    reqd_data = sheet_db[sheet_name].sort_values(by=['Datetime'], ascending=False).head(no_transactions)
    soln = reqd_data['Solution'].tolist()[0]
    keywords = reqd_data['Keywords'].tolist()[0]
    return soln, keyword


def fnwrite_solution(probid, new_solution):
    try:
        entities, keywords = get_nlu_response(new_solution)
    except:
        entities = 'Missing'
        keywords = 'Fuel Injector'
    sheet_name = 'Solutions'
    actual_time = datetime.now()
    sheet_db[sheet_name] = pd.concat([sheet_db[sheet_name], pd.DataFrame([{'ProblemID': probid, 'Solution': new_solution,
                                                                           'Datetime': actual_time, 'Keywords': keywords,
                                                                           'Entities': entities}])],
                                             ignore_index=True, sort=False)
    fn_write_pdxls(sheet_db, os.path.join(data_path, xls_filename))


def fnget_question(probid):
    sheet_name = 'Questions'
    reqd_sheet = sheet_db[sheet_name]
    reqd_ques = reqd_sheet[reqd_sheet['ProbID']==probid]['Question'].tolist()[0]
    return reqd_ques


def fnget_imgurls(probid):
    sheet_name = 'Images'
    reqd_sheet = sheet_db[sheet_name]
    reqd_imgurl = reqd_sheet[reqd_sheet['ProbID'] == probid]['Images'].tolist()[0]
    return reqd_imgurl




if __name__ == "__main__":
    recent = fnget_recent_solutions(10)
    print(tabulate(recent.head(50), headers='keys', tablefmt='psql'))
    recent_ques = fnget_question(2)
    print(recent_ques)
    recent_ques = fnget_imgurls(2)
    print(recent_ques)
    response = "Stark has a Freightliner Trucks (Model 114SD AB) If there are just gummy deposits in the injector body, you can clean them. Carb cleaner can do this very well for you, but you need to actuate the injector to get the carb cleaner in there to clean out anything which may be causing issues. If you pull the injector out of the bore to clean it, you should consider getting a rebuilt kit, which in most cases gives your a new screen (located in the top of the injector ... if so equipped), as well as the O-rings. In most cases, you don't want to reuse the o-rings because they will tend to leak. If they are older, they will most likely tear as you try to put them back into the injector bore, even if you coat them with oil. Besides, depending on the age, newer o-rings will not be susceptible to getting ate up by ethanol."
    fnwrite_solution(1, response)
