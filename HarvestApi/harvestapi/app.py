import os
from flask import Blueprint, Flask
from flask_restful import Api
from harvestapi.resources.metadata import MetadataApi, MetadataList
from harvestapi.resources.upload import UploadApi


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'downloads')
ALLOWED_EXTENSIONS = {'jpeg', 'png', 'gif', 'bmp', 'ico', 'mp4', 'mpeg', 'ogg', 'epub', 'zip', 'tar', 'rar', 'gz',
                      'pdf', 'exe'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route
api.add_resource(MetadataList, '/')
api.add_resource(MetadataApi, '/<hash>')
api.add_resource(UploadApi, '/upload')


