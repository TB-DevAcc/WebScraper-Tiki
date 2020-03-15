from flask import Flask, render_template, request, redirect
import pandas as pd
import sqlite3

from scrape_tiki import create_db


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_input = ''
    if request.method == 'POST':
      search_input = request.form.get('search_input')

    try:
      f = open("tiki.db")
    except IOError:
      BASE_URL = 'https://tiki.vn/'
      conn = sqlite3.connect('tiki.db')
      c = conn.cursor()
      create_db(BASE_URL, conn, c)
    finally:
      f.close()
      conn = sqlite3.connect('tiki.db')

    df = pd.read_sql_query('SELECT * FROM categories', conn)    

    return render_template('home.html', data=df.to_html())
    
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=5000, debug=True)
  app.run(host='127.0.0.1', port=8000, debug=True)
   