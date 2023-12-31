import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import tempfile
from boxDetection import getImagesForOCR
from ocr import get_convos
from excelWriter import write_to_excel
import constants
from s3 import get_dir_names, bucket, get_excel_file

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/convos/names", methods=["GET"])
def get_conversation_names():
    if request.method == "GET":
        return jsonify(conversationNames=get_dir_names())


@app.route("/convos/upload", methods=["POST"])
def upload_conversation():
    if request.method == "POST":
        file = request.files.get("file")
        conversationName = request.form.get("conversationName")
        senderName = request.form.get("senderName")
        receiverName = request.form.get("receiverName")
        darkMode = json.loads(request.form.get("darkMode"))
        if file:
            dirName = conversationName + "_" + senderName + "_" + receiverName
            bucket.put_object(Key=dirName + "/")
            temp_dir = tempfile.TemporaryDirectory()
            filename = secure_filename(file.filename)
            file.save(os.path.join(temp_dir.name, filename))
            getImagesForOCR(
                os.path.join(temp_dir.name, filename),
                dirName,
                senderName,
                receiverName,
                darkMode,
            )
            temp_dir.cleanup()
        return jsonify(conversationNames=get_dir_names())
    return jsonify("error")


@app.route("/convos/excel", methods=["GET"])
def send_excel_file():
    convos = get_convos()
    # for convo in convos:
    #     print(convo.getDictRepresentation())
    #     print("\n\n")
    write_to_excel(convos)
    with tempfile.TemporaryDirectory() as tmpdirname:
        get_excel_file(tmpdirname)
        return send_from_directory(tmpdirname, constants.FILE)
