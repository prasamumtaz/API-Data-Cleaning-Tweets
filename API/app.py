import re
import pandas as pd
import sqlite3
from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import os

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

#Fucntion to Clean tweet data
def Clean(Tweet):
    #lowercase for every word
    Tweet = Tweet.lower()

    #Clean Pattern
    #remove USER
    Tweet = re.sub(r'user|user:', ' ', Tweet)
    #remove 'RT'
    Tweet = re.sub(r'^rt[\s]+| rt', ' ', Tweet)
    #remove 'URL'
    Tweet = re.sub(r'^url[\s]+| url', ' ', Tweet)
    #remove HTTPS
    Tweet = re.sub(r'https\S+|https', ' ', Tweet)
    #remove HTTP
    Tweet = re.sub(r'http\S+|http', ' ', Tweet)
    #remove &amp
    Tweet = re.sub(r'&amp', ' ', Tweet)

    #Clean_Unnecessary_Character
    #remove \n or every word afte '\' with space
    Tweet = re.sub(r'\\n|\\[a-zA-Z0-9]+', ' ', Tweet)
    #remove text emoji
    Tweet = re.sub(r'[^a-zA-Z0-9\s]{2,}|:[a-zA-Z0-9]{0,}', ' ', Tweet)
    #remove all unnecessary character 
    Tweet = re.sub(r'[^0-9a-zA-Z\s]+', ' ', Tweet)
    #remove extra space
    Tweet = re.sub(r'  +', ' ', Tweet)
    #remove space at the start or the end of string
    Tweet = re.sub(r'^ +| +$', '', Tweet)
    
    return Tweet

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    #request to input text
    text = request.form.get('text')

    #run Clean(text) fuction to clean input text
    clean_text = Clean(text)

    #connect sqlite database 
    conn = sqlite3.connect(current_directory + "\DataBase\Database_processing.db")
    cursor = conn.cursor()

    #input query to store input file into database
    query1 = """INSERT INTO input_text VALUES('{t}')""".format(t = text)
    cursor.execute(query1)

    #input query to store input file into database
    query2 = """INSERT INTO output_text VALUES('{t}')""".format(t = clean_text)
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
    file = request.files('file')

    #connect sqlite database 
    conn = sqlite3.connect(current_directory + "\DataBase\Database_processing.db")
    #cursor = conn.cursor()

    #read CSV file
    df = pd.read_csv(file, encoding='latin1')
    #Filter column Tweet column
    df2= pd.DataFrame(df[['Tweet']])
    df2.to_sql('input_Tweet', conn, if_exists='append', index = False)

    #Convert text that want to process into list
    text_file = df['Tweet'].to_list()

    #Running cleaning data function (Clean)
    clean_Tweet = []
    for text in text_file:
         clean_Tweet.append(Clean(text))

    json_response = {
        'status_code': 200,
        'description': "Teks cleaning process is successful",
        'data': "process cleaning text from CSV file has succeed"
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()