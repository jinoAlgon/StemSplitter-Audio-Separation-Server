from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import os
from pathlib import Path
import shutil
from audio_processing import separate, create_zip

from flask import Flask, request, jsonify
# from flask_cors import CORS
from flask_talisman import Talisman


app = Flask(__name__)
CORS(app, resources={r"/separate": {"origins": "localhost"}})


talisman = Talisman(app)

UPLOAD_FOLDER = 'uploads'
SEPARATED_FOLDER = 'separated'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEPARATED_FOLDER'] = SEPARATED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(SEPARATED_FOLDER):
    os.makedirs(SEPARATED_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/separate', methods=['POST'])
def separate_audio_file():
    print(request.files)  
    if 'file' not in request.files:
        return jsonify(error="No audio part in the request"), 400

    audio_file = request.files['file']
    if audio_file.filename == '':
        return jsonify(error='No selected file'), 400
    if audio_file and allowed_file(audio_file.filename):
        filename = audio_file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)

        # Audio separation logic
        output_dir = os.path.join(app.config['SEPARATED_FOLDER'], os.path.splitext(filename)[0])
        separate(filepath, output_dir)

        # Creating zip file and then cleanup
        zip_data = create_zip(output_dir, os.path.splitext(filename)[0])
        with open("test_output.zip", "wb") as f:
            f.write(zip_data.getvalue())

        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(output_dir)
                os.remove(filepath)
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response

        return send_file(zip_data, download_name=f"{os.path.splitext(filename)[0]}.zip", as_attachment=True)

    return jsonify(error='Invalid file format'), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))

