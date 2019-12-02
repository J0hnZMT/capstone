from flask import request
from flask_restful import Resource
from harvestapi.model import db, MetadataMonitor, MetadataMonitorSchema

api_many_schema = MetadataMonitorSchema(many=True)
api_schema = MetadataMonitorSchema()


class MetadataApi(Resource):

    # read the metadata of a file from db based on the hash given
    def get(self, file_hash):
        data = {"hash": file_hash}
        if len(file_hash) == 32:
            select_hash = MetadataMonitor.query.filter_by(md5=data['hash'])
            result = api_many_schema.dump(select_hash).data
            return {'status': 'success', 'data': result}, 200
        elif len(file_hash) == 40:
            select_hash = MetadataMonitor.query.filter_by(sha1=data['hash'])
            result = api_many_schema.dump(select_hash).data
            return {'status': 'success', 'data': result}, 200

    # update the meat data of a file based on the hash given
    def put(self, file_hash):
        search_data = {"hash": file_hash}
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = api_schema.load(json_data)
        if errors:
            return errors, 422
        if len(file_hash) == 32:
            hash_file = MetadataMonitor.query.filter_by(md5=search_data['hash']).first()
            if not hash_file:
                return {'message': 'File does not exist'}, 400
            hash_file.file_name = data['file_name']
            hash_file.file_type = data['file_type']
            hash_file.file_size = data['file_size']
            hash_file.sha1 = data['sha1']
            db.session.commit()
            result = api_schema.dump(hash_file).data
            return {"status": 'success', 'data': result}, 200
        elif len(file_hash) == 40:
            hash_file = MetadataMonitor.query.filter_by(sha1=search_data['hash']).first()
            if not hash_file:
                return {'message': 'File does not exist'}, 400
            hash_file.file_name = data['file_name']
            hash_file.file_type = data['file_type']
            hash_file.file_size = data['file_size']
            hash_file.md5 = data['md5']
            db.session.commit()
            result = api_schema.dump(hash_file).data
            return {"status": 'success', 'data': result}, 200

    def delete(self, file_hash):
        data = {"hash": file_hash}
        if len(file_hash) == 32:
            MetadataMonitor.query.filter_by(md5=data['hash']).delete()
            db.session.commit()
            # delete also the existing file
            return {"status": 'success', "message": 'file deleted'}, 200
        elif len(file_hash) == 40:
            MetadataMonitor.query.filter_by(sha1=data['hash']).delete()
            db.session.commit()
            # delete also the existing file
            return {"status": 'success', "message": 'file deleted'}, 200


class MetadataList(Resource):

    def get(self):
        select_all = MetadataMonitor.query.all()
        result = api_many_schema.dump(select_all).data
        return {'status': 'success', 'data': result}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = api_schema.load(json_data)
        if errors:
            return errors, 422
        query_insert = MetadataMonitor.query.filter_by(file_name=data['file_name']).first()
        if query_insert:
            return {'message': 'Job already exists'}, 400
        query_insert = MetadataMonitor(
            file_name=json_data['job_id'],
            file_type=json_data['file_type'],
            file_size=json_data['file_size'],
            sha1=json_data['sha1'],
            md5=json_data['md5']
        )
        db.session.add(query_insert)
        db.session.commit()
        result = api_schema.dump(query_insert).data
        return {"status": 'success', 'data': result}, 201
