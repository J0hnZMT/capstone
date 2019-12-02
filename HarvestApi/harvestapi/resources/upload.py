from flask import request
from flask_restful import Resource


class UploadApi(Resource):

    def post(self):
        upload = request.files
        print(upload)
        return {"message": upload}, 200



