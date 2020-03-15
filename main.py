from flask import Flask, render_template, request, redirect

from scrape_tiki import create_db


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_input = ''
    if request.method == 'POST':
      search_input = request.form.get('search_input')

    create_db()

    return render_template('home.html', data=None)
    
if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=5000, debug=True)
  app.run(host='127.0.0.1', port=8000, debug=True)
   