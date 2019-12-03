import hashlib
import logging
import os
import requests

logger = logging.getLogger(__name__)


def md5_hash(file_to_hash):
    try:
        block_size = 65536
        hash_md5 = hashlib.md5()
        # getting the md5 hashes of files
        with open(file_to_hash, 'rb') as hash_file:
            buf = hash_file.read(block_size)
            while len(buf) > 0:
                hash_md5.update(buf)
                buf = hash_file.read(block_size)
        return hash_md5.hexdigest()
    except FileNotFoundError as e:
        logger.exception(e)


def sha1_hash(file):
    try:
        block_size = 65536
        hash_sha1 = hashlib.sha1()
        # getting the sha1 hashes of files
        with open(file, 'rb') as hash_file:
            buf = hash_file.read(block_size)
            while len(buf) > 0:
                hash_sha1.update(buf)
                buf = hash_file.read(block_size)
        return hash_sha1.hexdigest()
    except FileNotFoundError as e:
        logger.exception(e)


def metadatas(path):
    file_names = os.listdir(path)
    for file_name in file_names:
        file_with_path = os.path.join(path, file_name)
        file_size = os.path.getsize(file_with_path)
        # get the hashes of the files
        md5_file_hash = md5_hash(file_with_path)
        sha1_file_hash = sha1_hash(file_with_path)
        # store the data in a dictionary
        report = {'file_name': file_name.rsplit('.')[0], 'file_type': file_name.rsplit('.')[1],
                  'file_size': file_size, 'md5': md5_file_hash, 'sha1': sha1_file_hash}
        requests.post('http://127.0.0.1:5000/harvest/', report)
