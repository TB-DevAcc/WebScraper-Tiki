import os.path

from flask import Flask, render_template, request, redirect
import pandas as pd
import sqlite3

from scrape_tiki import create_db


app = Flask(__name__)

BASE_URL = 'https://tiki.vn/'
# Check if Database was already created
if not os.path.isfile('tiki.db'):
  conn = sqlite3.connect('tiki.db')
  c = conn.cursor()
  create_db(BASE_URL, conn, c, verbose=True)
else:
  conn = sqlite3.connect('tiki.db')
  c = conn.cursor()

pd.set_option('colheader_justify', 'center')
df = pd.read_sql_query("""
                        SELECT p.id AS ID, p.name AS Name, p.url AS URL, c.name AS Parent, p.parent_id AS [Parent ID] FROM 
                        categories p LEFT JOIN categories c ON p.parent_id=c.id                        
                        """, conn)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_input = ''
    if request.method == 'POST':
      search_input = request.form.get('search_input')  
      data = df.loc[df['Name']==search_input].to_html()
    else:
      data = df.to_html()

    return render_template('home.html', data=data)
    
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=5000, debug=True)
  app.run(host='127.0.0.1', port=8000, debug=True)
   