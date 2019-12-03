import os
from flask import request
from flask_restful import Resource
from harvestapi.resources.data_retrieve import metadatas


def download(binary, name):
    # download the file
    dl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)
    os.chdir(dl_path)
    try:
        with open(name, "wb") as file:
            file.write(binary)
        metadatas(dl_path)
        return {'message': 'success', 'file': name}, 200
    except TypeError as e:
        return {'message': 'File does not exist'}, 400


class UploadApi(Resource):

    def post(self):
        upload = request.files['file']
        file_binary = upload.read()
        file_name = upload.filename
        value = download(file_binary, file_name)
        return value



