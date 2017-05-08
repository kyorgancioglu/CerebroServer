import os
from flask import Flask, request, jsonify, abort, send_file
from werkzeug.utils import secure_filename
from clarifai.rest import ClarifaiApp
import psycopg2
app = Flask(__name__)
clf = ClarifaiApp()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, './uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])

conn_str = """host='ec2-54-247-99-159.eu-west-1.compute.amazonaws.com'
dbname='d83m8s9ccqk1ru' user='hizrwppkmzlubk'
password='8a13659658a5082c25bb5fcefaef12e33f1d0f594332d19b302c56332ac24eab'"""

conn = psycopg2.connect(conn_str)
cursor = conn.cursor()

#os.environ['CLARIFAI_APP_ID'] = 'boEFgeb2dA1OyON3PcXRd_Fle1r0jP-FyzIa1aqn'
#os.environ['CLARIAI_APP_SECRET'] = 'ZSe1ekDr4lXddODOzZJYYpudcMw8A_k4OlzLMt0w'
#book stubs
stub_books = [
    {
        'id':1,
        'name': u'kurk mantolu madonna',
        'goodreads_link': u'/book/show/220826.K_rk_Mantolu_Madonna'
    },
    {
        'id':2,
        'name': u'kuyucakli yususf',
        'goodreads_link': u'/book/show/220826.K_rk_Mantolu_Madonna'
    }

]

stub_movies = [
    {
        'id':3,
        'name': u'Titanic',
        'imdb_link': u'/title/tt0120338/'
    },
    {
        'id':4,
        'name': u'G.O.R.A',
        'imdb_link': u'/title/tt0384116/'
    }

]

def select_with_url(pstr):
    cursor.execute("SELECT imdbid FROM movies WHERE posterurl = \'" + pstr + "\';")
    res = cursor.fetchall()
    return res

@app.route('/')
def welcome():
   return 'up-to-date api :v1.0 use /media/api/v1.0'

@app.route('/media/api/v1.0/books/<int:id>', methods = ['GET'])
def search_book_by_id(id):
    #stub method needs to be replaced by database query
    results = [book for book in stub_books if book['id'] == id]
    if len(results) <= 0:
        abort(404)
    return jsonify({'books':results})

@app.route('/media/api/v1.0/movies/<int:id>', methods = ['GET'])
def search_movie_by_id(id):
    results = [movie for movie in stub_movies if movie['id'] == id]
    if len(results) <= 0:
        abort(404)
    return jsonify({'movies':results})

@app.route('/debug/see')
def see_file():
    return send_file('./uploads/upload.bmp')

#debug method
@app.route('/media/api/v1.0/books', methods = ['GET'])
def get_books():
    return jsonify({'books':stub_books})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def search_in_clarifai(file):
    res = clf.inputs.search_by_image(fileobj=file, per_page = 1)
    return res[0].url

@app.route('/media/api/v1.0/movies/s', methods = ['POST'])
def search_movie_by_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'no file part'
        file = request.files['file']
        if file.filename == '':
            return 'no filename'
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            res_url = search_in_clarifai(file)
            found = select_with_url(res_url)
            if len(found) == 0:
                return 'no matches found'
            else:
                return found[0][0]
        else:
            return 'file extension not allowed'

if __name__ == '__main__':
    app.run(debug = True)
