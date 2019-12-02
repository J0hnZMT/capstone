from marshmallow import fields, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from harvestapi.setup import config_opener

ma = Marshmallow()
db = SQLAlchemy()


class MetadataMonitor(db.Model):
    table = config_opener('setup.ini', 'tables')
    __tablename__ = table['api_table']
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    sha1 = db.Column(db.String(40), nullable=False)
    md5 = db.Column(db.String(32), nullable=False)

    def __init__(self, file_name, file_type, file_size, sha1, md5):
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.sha1 = sha1
        self.md5 = md5


class MetadataMonitorSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    file_name = fields.String(validate=validate.Length(1))
    file_type = fields.String(validate=validate.Length(1))
    file_size = fields.Integer()
    sha1 = fields.String(validate=validate.Length(1))
    md5 = fields.String(validate=validate.Length(1))


class HarvestMonitor(db.Model):
    table = config_opener('setup.ini', 'tables')
    __tablename__ = table['api_upload_table']
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150), nullable=False)
    app_url = db.Column(db.String(150), nullable=False)

    def __init__(self, file_name, app_url):
        self.file_name = file_name
        self.app_url = app_url


class HarvestMonitorSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    file_name = fields.String(validate=validate.Length(1))
    app_url = fields.String(validate=validate.Length(1))






