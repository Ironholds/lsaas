#!flask/bin/python
import markdown
from flask  import Flask, jsonify, make_response, Markup, render_template
from random import choice
from data   import *
from papers import *

app = Flask(__name__, static_url_path='')

@app.route('/lsaas/')
def index():
  index_content = """
Lip Service As A Service (LSAAS)
=======

A realistic open data API
-------
Everyone wants open data! We have oh-so-very-many APIs and open data sites, and somewhere between making them
RESTful and CRUDdy and SOA-based and TLA-full we forgot to make them actually work. Don't even talk to me
about "open publishing".

So I wrote a realistic open API, Lip Service As A Service. You're welcome.

Use
-------
LSAAS has two sorts of information, both provided as JSON. They are *papers* (academic publications)
and *data* (open datasets). Of course, this is actually a realistic API, so neither is genuinely provided.
That was just to get you in the door.

*Papers* can be accessed by pointing a GET request at <code>[http://ironholds.org/lsaas/papers/](./papers/)</code>.
Leaving the URL at that will just give you a randomly-selected item from our array of only-mostly-a-joke server responses, which contain
an ID number, a name and a result. If you point the request at <code>http://ironholds.org/lsaas/papers/id_number</code> you can get a specific item
rather than a randomly selected one.

*Data* can be accessed by pointing a POST request at <code>[http:/ironholds.org/lsaas/data/](./data/)</code>. We were going to have it use
GET requests too but the nice people from Oracle told us that GET requests weren't ISO compliant. Given how much they charged, they
*have* to know what they're talking about.

Data requests don't provide data, they provide errors. These take the form of an ID number, a nonsensical error code and
an error message. As with *papers*, appending an ID number to the URL will get you a specific error instead of a randomly-selected
one.

Contribute
-------
The source code [lives on GitHub](https://github.com/Ironholds/lsaas) and is written by, well, [Oliver](http://ironholds.org)
after a joke that [Scott Chamberlain](https://github.com/sckott) made on Twitter spiraled massively, massively out of control. Scope creep is a real thing.
If you'd like to submit new error messages or events, submit a pull request!

Render irrelevant
-------
If youre interested in making this an invalid pointless tool as well as just
a pointless tool:

* Get involved in groups that work on APIs, client- or server-side, like [rOpenSci](https://ropensci.org/)
* Teach your org to write good APIs. Check out [The Sunlight Foundation](http://sunlightfoundation.com/) for one of my favourites.
* Learn about and educate people about [the importance of open data](http://opendatahandbook.org/en/index.html).
"""
  index_content = Markup(markdown.markdown(index_content))
  return render_template('index.html', **locals())
  

@app.route('/lsaas/data/', methods=['POST'])
def rand_task():
  return jsonify({'dataset': choice(datasets)})

@app.route('/lsaas/data/<int:data_id>', methods=['POST'])
def get_task(data_id):
  dataset = [dataset for dataset in datasets if datasets['id'] == data_id]
  if len(dataset) == 0:
    abort(404)
  return jsonify({'dataset': dataset[0]})

@app.route('/lsaas/papers/', methods=['GET'])
def rand_paper():
  return jsonify({'paper': choice(papers)})

@app.route('/lsaas/papers/<int:paper_id>', methods=['GET'])
def get_paper(data_id):
  paper = [paper for paper in papers if papers['id'] == paper_id]
  if len(paper) == 0:
    abort(404)
  return jsonify({'dataset': paper[0]})

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

app.run(port=1955, debug=True)
