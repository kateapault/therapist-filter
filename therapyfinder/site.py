from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from therscrap import getPsychData
import pymysql
import pymysql.cursors

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeholder_secret_key'


###### functions and prework ########

def make_doubled_list_tuples(li):
    out = []
    for item in li:
        out.append((item,item))
    return out
#states including DC
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
state_tuples = make_doubled_list_tuples(states)

######## forms #######################

class FilterForm(FlaskForm):

    psychiatrist = BooleanField(u'Psychiatrist')
    psychologist = BooleanField(u'Psychologist')
    therapist = BooleanField(u'Therapist')
    insurance = SelectField(u'What insurance do you have?',choices=[('anthem','Anthem'),('bcbs','Blue Cross Blue Shield'),('fidelus','Fidelus'),('medicare','Medicare'),('medicaid','Medicaid'),('tricare','TriCare')])
    mf = RadioField(u'Do you have a preference for a male or female doctor?', choices=[('f','Female'),('m','Male'),('np',"No preference")])
    user_street = StringField(u'Enter your street address: ')
    user_city = StringField(u'Enter your city: ')
    user_state = SelectField(u'Enter your state: ',choices=state_tuples)
    remote = RadioField(u'Do you need a phone / video call / remote option?', choices=[('remote','Remote only'),('inperson','In-Person only'),('either','No preference (both)')])

    submit = SubmitField('Find Doctors')

######## flask pages ####################

@app.route('/',methods=['GET','POST'])
def home():
# should links to other pages be via python or html?
    return render_template('home.html')


@app.route('/search',methods=['GET','POST'])
def search():

    form = FilterForm()
    if form.is_submitted():
        session['psychiatrist'] = form.psychiatrist.data
        session['psychologist'] = form.psychologist.data
        session['therapist'] = form.therapist.data
        session['insurance'] = form.insurance.data
        session['mf'] = form.mf.data
        session['remote'] = form.remote.data
        session['user_street'] = form.user_street.data
        session['user_city'] = form.user_city.data
        session['user_state'] = form.user_state.data
        return redirect(url_for('result'))

    return render_template('search.html',form=form)


@app.route('/result')
def result():

#   temp data to pass into database queries after database is set up
    psychiatrist = session['psychiatrist']
    psychologist = session['psychologist']
    therapist = session['therapist']
    insurance = session['insurance']
    mf = session['mf']
    remote = session['remote']
    user_street = session['user_street']
    user_city = session['user_city']
    user_state = session['user_state']

#   connect to mySQL
#   Currently using test_docs as test db connection since scraped database isn't built yet
    host = 'localhost'
    user = 'root'
    password='9sthsmrscrthn?'
    dbname='test_docs'
    charset='utf8mb4'
    cursorclass=pymysql.cursors.DictCursor

    connection = pymysql.connect(host='127.0.0.1',
                        user='root',
                        password='9sthsmrscrthn?',
                        db='test_docs',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
#   reading data to existing database
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `name` FROM 'test_docs'  WHERE `job_title`=%s"
            cursor.execute(sql, ('psychiatrist',))
            doc_name = cursor.fetchone()
            print(doc_name)

#   close connection
    finally:
        connection.close()


    return render_template('result.html',doc_name=doc_name)

#page with advice on how to approach therapy; currently empty and will be just text
@app.route('/advice')
def advice():
    return render_template('advice.html')

if __name__ == '__main__':
    app.run(debug=True)
