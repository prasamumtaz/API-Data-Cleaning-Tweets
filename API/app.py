import re
import pandas as pd
from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: "API Documentation for Data Processing and Modeling"),
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

    text = request.form.get('text')

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
	#Upload CSV File 
    file = request.files.getlist('file')[0]
    # Import/read CSV file using pandas
    df = pd.read_csv(file)
    #Convert text that want to process into list
    text_file = df.text.to_list()

    #Running cleaning data function (Clean)
    clean_text = []
    for text in text_file:
        clean_text.append(Clean(text))

    json_response = {
        'status_code': 200,
        'description': "Teks cleaning process is successful",
        'data': clean_text,
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()