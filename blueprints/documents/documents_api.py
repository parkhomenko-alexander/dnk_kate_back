
import os
import json
from typing import TypedDict
from dataclasses import dataclass
from flask import Blueprint, make_response, request, send_file
from werkzeug.utils import secure_filename
from sqlalchemy import select 

from config import Config
from models.models import *
from models.setup import session

documents_api: Blueprint = Blueprint('documents_api',
                                    __name__,
                                    static_folder=Config.STATIC_URL_PATH,
                                    url_prefix='/documents') 
class DocumentNumber(TypedDict):
    name: str
    number: str

@dataclass
class ResponseDocument():
    id: int
    name: str
    numbers: List[str]
    files: List[str]

server_url = 'http://localhost:5000'

@documents_api.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', default='').lower()
    doc = session.query(Document).where(Document.name == name).scalar()
    if not doc is None or doc=='':
         return make_response({
            'Access-Control-Allow-Origin': '*',
        'msg': 'successfully added',
    }, 500)

    doc: Document | None = Document(name=name)
    session.add(doc)
    session.flush()
    files = request.files.getlist("file[]")

    response_document: ResponseDocument = ResponseDocument(doc.id, doc.name, [], []) 

    for i, f in enumerate(files):
        if not f.filename is None:
            fln = '/static/upload/doc' + str(doc.id) + 'file' + str(i) + '.' + f.filename.split('.')[-1]
            filename_s = os.getcwd() + fln
            filename_d = 'doc' + str(doc.id) + 'file' + str(i) + '.' + f.filename.split('.')[-1]
            print(filename_s)
            f.save(filename_s)
            doc_file: File = File(path=filename_d, document_id=doc.id)
            response_document.files.append(filename_d)
            session.add(doc_file)

    numbers_row = request.form.getlist('numbers[]')

    print('asd')
    print(request.form)
    # 
    # 
    # 
    if not numbers_row is None:
        # numbers: dict[str, DocumentNumber] = json.loads(numbers_row)
        print(numbers_row)
        for i,num in enumerate(numbers_row):
            number: UniqueNumber = UniqueNumber(number=num, document_id=doc.id)
            response_document.numbers.append(number.number)
            session.add(number)
    
    session.commit()
    return make_response({
        'msg': 'successfully added',
        'document': response_document
    }, 201)

@documents_api.route('/<int:id>', methods=['GET'])
def get_document(id):
    data = {}
    stmt = select(Document).where(Document.id==id)
    doc: Document | None = session.scalar(stmt)
    
    if not doc is None:
        files_paths = []
        unique_numbers = []

        for f in doc.files:
            print(f.path)
            files_paths.append(Config.PROD_IP+f.path)

        for unique_n in doc.numbers:
            unique_numbers.append(unique_n.number)

        data['files_paths'] = files_paths
        data['unique_numbers'] = unique_numbers
    else:
        ...

    return make_response({
        'msg': 'successfully',
        'data': data
    }, 200)

@documents_api.route('/', methods=['GET'])
def get_all():
    documents = []
    stmt = select(Document)
    docs: List[Document] = session.execute(stmt).scalars().all()
    print(docs)
    for d in docs:
        documents.append({
            'id': d.id,
            'name': d.name,
            'numbers': [n.number for n in d.numbers],
            'files': [f.path for f in d.files]
        })

    return documents

@documents_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    stmt = select(Document).where(Document.id==id)
    doc: Document = session.execute(stmt).scalars().first()
    doc_id = doc.id
    session.delete(doc)
    session.commit()

    return {
        'msg': 'successfully removed',
        'document_id': doc_id
    }

@documents_api.route('/download/<string:fln>', methods=['GET'])
def download(fln):
    return send_file(os.getcwd() + '\\static\\upload\\' + fln, as_attachment=True)