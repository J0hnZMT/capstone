import os
from flask import Blueprint, Flask
from flask_restful import Api
from harvestapi.data_retrieve import metadatas
from harvestapi.resources.metadata import MetadataApi, MetadataList
from harvestapi.resources.upload import UploadApi


app = Flask(__name__)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(MetadataList, '/')
api.add_resource(MetadataApi, '/<hash>')
api.add_resource(UploadApi, '/upload')


