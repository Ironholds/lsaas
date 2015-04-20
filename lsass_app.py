#!flask/bin/python
from flask  import Flask, jsonify, make_response
from random import choice
from data   import *
from papers import *

app = Flask(__name__, static_url_path='')

@app.route('/lsaas/')
def root():
  return app.send_static_file('index.html')

@app.route('/lsaas/api/data', methods=['POST'])
def rand_task():
  return jsonify({'dataset': choice(datasets)})

@app.route('/lsaas/api/data/<int:data_id>', methods=['POST'])
def get_task(data_id):
  dataset = [dataset for dataset in datasets if datasets['id'] == data_id]
  if len(dataset) == 0:
    abort(404)
  return jsonify({'dataset': dataset[0]})

@app.route('/lsaas/api/data', methods=['GET'])
def rand_paper():
  return jsonify({'paper': choice(papers)})

@app.route('/lsaas/api/papers/<int:paper_id>', methods=['POST'])
def get_paper(data_id):
  paper = [paper for paper in papers if papers['id'] == paper_id]
  if len(paper) == 0:
    abort(404)
  return jsonify({'dataset': paper[0]})

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)
