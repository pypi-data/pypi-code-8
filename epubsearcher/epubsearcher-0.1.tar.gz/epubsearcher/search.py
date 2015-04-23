from flask import Flask
from flask import request
from flask import jsonify
from flask import g

from epubsearch import EpubIndexer
from epubsearch import EpubParser
from epubsearch import crossdomain

app = Flask(__name__)
epub = EpubParser("moby-dick")

index = EpubIndexer("whoosh")
index.load(epub)

@app.route("/")
def home():
    return "try /search?q=whale"

@app.route("/search", methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def search():
    query = request.args.get('q')
    results = index.search(query)
    print(results)
    return jsonify(**results)

if __name__ == "__main__":
    app.run(debug=True)

