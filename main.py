import os.path

from flask import Flask, render_template, request, redirect
import pandas as pd
import sqlite3

from scrape_tiki import create_db


app = Flask(__name__)

BASE_URL = 'https://tiki.vn/'
conn = sqlite3.connect('tiki.db')
c = conn.cursor()

if not os.path.isfile('tiki.db'):
  create_db(BASE_URL, conn, c, verbose=True)

#pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')
df = pd.read_sql_query('SELECT * FROM categories', conn)

def select(selection='*', name=None):
    if name != None:
        name = f' WHERE name=={name}' # TODO
    return c.execute(f'SELECT {selection} FROM categories{name if name else ""};').fetchall()

def delete_all():
    return c.execute('DROP TABLE IF EXISTS categories;')


@app.route('/', methods=['GET', 'POST'])
def index():
    search_input = ''
    if request.method == 'POST':
      search_input = request.form.get('search_input')  

    return render_template('home.html', data=df.to_html())
    
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=5000, debug=True)
  app.run(host='127.0.0.1', port=8000, debug=True)
   