#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify
import psycopg2
import json

app = Flask(__name__)
test = 'hey'

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

            query = 'SELECT person_id, first_name, last_name, workout_location FROM public."Person" WHERE username = ' + "'" + user + "'" + ' AND pwd = ' + "'" + pwd + "'"           
            cursor.execute(query)
            rs = cursor.fetchall()            

            # If Logged in...
            if len(rs) > 0:
                user_id   = rs[0] # Gets user ID after login validation
                user_name = str(rs[0][1]).strip() + ' ' + str(rs[0][2]).strip() # Gets First Name / Last Name after login validation
                location  = rs[0][3]
                results, dates = [None],['']

                query = 'SELECT weigh_in, weigh_in_dt FROM public."Results" WHERE person_id = ' + "'" + str(user_id[0]) + "'"           
                cursor.execute(query)
                rs = cursor.fetchall()               

                for x in rs:
                    #print(x[0], ' | and | ' , x[1] )
                    results.append( float(x[0]) )
                    dates.append(  str(x[1]) )
                
                results.append( None )
                dates.append( '' )    

                print(dates)
                return render_template('main.html', data=results, labels=dates, user=user_name, location=location)
            
            # If Login Fails...
            else:
                return render_template('login.html', error='Invalid user / Incorrect Password')           

        except (Exception, psycopg2.Error) as error:
            exception = "Error while fetching data from PostgreSQL: " + error
            print (exception)
            return render_template('login.html', error=exception)
        #################################################################################