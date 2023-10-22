import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

class CustomFlaskAppWithEncoder(Flask):
	json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'This is your secret key to utilize session in Flask'

swagger_template = dict(
	info = {
		'titlle': LazyString(lambda: "API Documentation for Data Cleaning"),
		'version': LazyString(lambda: "1.0.0"),
		'description': LazyString(lambda: "Dokumentasi API untuk Data Processing dan Modeling"),
	},
	host = LazyString(lambda: request.host)
)

swagger_config = {
	"headers" : [],
	"specs" : [
		{
			"endpoint": "docs",
			"route": "/docs.json",
		}
	],
	"static_url_path": "/flasgger_statis",
	# "static_folder": "static", #must be set by user
	"swagger_ui": True,
	"specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

@swag_from("docs/csv_upload.yml", methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def uploadFile():
	json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': "Halo, apa kabar semua?",
    }
	if request.method == 'POST':
	# upload file flask
		f = request.files.get('file')

		# Extracting uploaded file name
		data_filename = secure_filename(f.filename)
		basedir = os.path.abspath(os.path.dirname(__file__))

		f.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'],
							data_filename))

		session['uploaded_data_file_path'] = os.path.join(basedir, app.config['UPLOAD_FOLDER'], data_filename)

		return render_template('index2.html')
	#return render_template("index.html")
	response_data = jsonify(json_response)
	return response_data


@app.route('/show_data')
def showData():
	# Uploaded File Path
	data_file_path = session.get('uploaded_data_file_path', None)
	# read csv
	uploaded_df = pd.read_csv(data_file_path,
							encoding='unicode_escape')
	# Converting to html Table
	uploaded_df_html = uploaded_df.to_html()
	return render_template('show_csv_data.html',
						data_var=uploaded_df_html)


if __name__ == '__main__':
	app.run(debug=True)
