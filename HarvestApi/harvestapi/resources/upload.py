import os
from flask import request
from flask_restful import Resource
from harvestapi.data_retrieve import metadatas
from harvestapi.model import db, MetadataMonitor, MetadataMonitorSchema

api_schema = MetadataMonitorSchema()
dl_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')


class UploadApi(Resource):

    def post(self):
        upload = request.files['file']
        file_binary = upload.read()
        file_name = upload.filename
        if not os.path.exists(dl_path):
            os.makedirs(dl_path)
        os.chdir(dl_path)
        try:
            if not os.path.exists(file_name):
                with open(file_name, "w+b") as file:
                    file.write(file_binary)
                json_data = metadatas(dl_path, file_name)
                # Validate and deserialize input
                data, errors = api_schema.load(json_data)
                if errors:
                    return errors, 422
                query_insert = MetadataMonitor.query.filter_by(file_name=data['file_name']).first()
                if query_insert:
                    return {'message': 'File already exist'}, 400
                query_insert = MetadataMonitor(
                    file_name=json_data['file_name'],
                    file_type=json_data['file_type'],
                    file_size=json_data['file_size'],
                    sha1=json_data['sha1'],
                    md5=json_data['md5']
                )
                db.session.add(query_insert)
                db.session.commit()
                result = api_schema.dump(query_insert).data
                return {'message': 'success', 'data': result}, 201
            else:
                return {'message': 'File already exist'}, 400
        except TypeError as e:
            return {'message': 'File does not exist'}, 400



