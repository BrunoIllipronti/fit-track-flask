#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/main', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        user = request.form["user"]
        pwd  = request.form["pwd"]

        # Login Validation
        #################################################################################
        try:
            conn = psycopg2.connect(database='hcbnahwh',user='hcbnahwh',password='R8BCNISNf2ZrLA-C-kurJrpjRr8gAET7',
                                    host='rajje.db.elephantsql.com',port=5432)

            cursor = conn.cursor()

            query = 'SELECT person_id, first_name, last_name FROM public."Person" WHERE username = ' + "'" + user + "'" + ' AND pwd = ' + "'" + pwd + "'"           
            cursor.execute(query)
            rs = cursor.fetchall()            

            if len(rs) > 0:
                user_id   = rs[0] # Gets user ID after login validation
                user_name = str(rs[0][1]).strip() + ' ' + str(rs[0][2]).strip() # Gets First Name / Last Name after login validation
                query = 'SELECT * FROM public."Results" WHERE person_id = ' + "'" + str(user_id[0]) + "'"           
                cursor.execute(query)
                rs = cursor.fetchall()

                return render_template('main.html', data=rs, user=user_name)
            else:
                return render_template('login.html', error='Invalid user / Incorrect Password')           

        except (Exception, psycopg2.Error) as error:
            exception = "Error while fetching data from PostgreSQL: " + error
            print (exception)
            return render_template('login.html', error=exception)
        #################################################################################