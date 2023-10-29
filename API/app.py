import pandas as pd
import sqlite3
import os
from flask import Flask
from flask import jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

#import all function from DataCleaning.py file
from DataCleaning import *

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

current_directory = os.path.dirname(os.path.abspath(__file__))

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: "API Documentation for Data Processing"),
        'version' : LazyString(lambda: "1.0.0"),
        'description' : LazyString(lambda: "Dokumentasi API untuk Data Processing dan Modeling"),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint": "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    #request to input text
    text = request.form['text']

    #run Clean(text) fuction from CleanData.py to clean input text
    clean_text = Clean(text)

    #connect sqlite database 
    conn = sqlite3.connect(current_directory + "\DataBase\Database_processing.db")
    cursor = conn.cursor()

    #input query to store input file into database
    query1 = "INSERT INTO input_text VALUES('{t}')".format(t = text)
    cursor.execute(query1)

    #input query to store input file into database
    query2 = "INSERT INTO output_text VALUES('{t}')".format(t = clean_text)
    cursor.execute(query2)

    #commit all query
    conn.commit()
    
    json_response = {
        'status_code': 200,
        'description': "Teks cleaning process is successful",
        'data': Clean(text)
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/processing_file.yml", methods=['POST'])
@app.route('/processing-file', methods=['POST'])
def text_processing_file():

    #CSV File 
	#Upload single CSV File 
    file = request.files['file']

    #connect sqlite database 
    conn = sqlite3.connect(current_directory + "\DataBase\Database_processing.db")
    #cursor = conn.cursor()

    #read CSV file
    df_fileInput = pd.read_csv(file, encoding='latin1')
    
    #Filter column Tweet column
    df_tweet= pd.DataFrame(df_fileInput[['Tweet']])
    
    #store all rows from filter column in csv file 
    #into Database_processing.db in 'input_Tweet' table
    df_tweet.to_sql('input_Tweet', conn, if_exists='append', index = False)

    #apply data cleaning fucntion from DataCleaning
    df_tweet['Tweet'] = df_tweet['Tweet'].apply(lambda x: ' '.join(map(str, clean_data(x))))

    #Drop the duplicate from previous clean data
    df_tweet.drop_duplicates(subset = 'Tweet', keep = 'first', inplace = True)

    #store file values into Database_processing.db in 'input_Tweet' table
    df_tweet.to_sql('clean_Tweet', conn, if_exists='append', index = False)

    # #Convert text that want to process into list
    # text_file = df['Tweet'].to_list()

    # #Running cleaning data function (Clean)
    # clean_Tweet = []
    # for text in text_file:
    #      clean_Tweet.append(Clean(text))

    json_response = {
        'status_code': 200,
        'description': "Teks cleaning process is successful",
        'data': "process cleaning text from CSV file has succeed"
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()