from flask import Flask, jsonify, abort
app = Flask(__name__)
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

@app.route('/')
def welcome():
   return 'up-to-date api :v1.0/nuse /media/api/v1.0'

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



#debug method
@app.route('/media/api/v1.0/books', methods = ['GET'])
def get_books():
    return jsonify({'books':stub_books})

if __name__ == '__main__':
   app.run(debug = True)
