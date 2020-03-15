from bs4 import BeautifulSoup
import requests
import sqlite3
import re
import time

BASE_URL = 'https://tiki.vn/'

conn = sqlite3.connect('tiki.db')
c = conn.cursor()

def create_db():
    """ Creates database with alle categories from tiki.vn
        Contains:
                - Classes & Methods: 
                    Category for a Category of Items on Tiki
                        save_to_db saves entry to the database

                - Functions: 
                    init_categories to initialize the SQL table with all Category instances
                    select to run SQL SELECT on DB with default all
                    delete_all to delete the whole db

                    get_soup to safely request URL with sleep time and error catching % BS4 conversion
                    find_main_tiki to find all of tiki's main prodcut categories
                    find_children to recursively find the child categories of the main categories
                              
    """
    def init_categories():
        query = """
                CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255),
                url TEXT, 
                parent_id INT, 
                create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
        """
        try:
                c.execute(query)
        except Exception as err:
                print('ERROR BY CREATE TABLE', err)

    class Category:
        def __init__(self, name, url, cat_id=None, parent_id=None):
                self.name = name            # NAME
                self.url = url              # URL
                self.cat_id = cat_id        # ID
                self.parent_id = parent_id  # PARENT
                self.save_into_db()         # Write to DB

        def __repr__(self):
                return  """
                        ID: {},
                        Name: {}, 
                        URL: {}, 
                        Parent_id: {}
                        """.format(self.cat_id, self.name, self.url, self.parent_id)

        def save_into_db(self):
                query = """
                INSERT INTO categories (name, url, parent_id)
                VALUES (?, ?, ?);
                """
                val = (self.name, self.url, self.parent_id)
                try:
                    c.execute(query, val)
                    self.cat_id = c.lastrowid
                except Exception as err:
                    print('ERROR BY INSERT:', err)
                
                conn.commit()

    init_categories() # Bootstraping table

    def get_soup(url):
        time.sleep(1.5)
        try:
            req = requests.get(url).text
            soup = BeautifulSoup(req, 'html.parser')
            return soup
        except Exception as err:
            print('ERROR BY REQUEST:', err)

    def find_main_tiki(): 
        soup = get_soup(BASE_URL)

        main_cats = []
        for cat in soup.find_all('a', {'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
            main_cats.append(Category(cat.text, cat['href']))
        
    find_main_tiki() #TESTING

def select(selection='*', name=None):
    if name != None:
        name = f' WHERE name=={name}' # TODO
    return c.execute(f'SELECT {selection} FROM categories{name if name else ""};').fetchall()

def delete_all():
    return c.execute('DROP TABLE IF EXISTS categories;')

create_db() #TESTING
#print(select(name='Điện Thoại'))