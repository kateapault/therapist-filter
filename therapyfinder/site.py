'''
'alpha' version using only web scraping - connects directly to the
scraping script. Enter city and state to get 5 therapists near that city.
'''

from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
import therapistscraper
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
#    insurance = SelectField(u'What insurance do you have?',choices=[('anthem','Anthem'),('bcbs','Blue Cross Blue Shield'),('fidelus','Fidelus'),('medicare','Medicare'),('medicaid','Medicaid'),('tricare','TriCare')])
#    mf = RadioField(u'Do you have a preference for a male or female doctor?', choices=[('f','Female'),('m','Male'),('np',"No preference")])
#    user_street = StringField(u'Enter your street address: ')
    user_city = StringField(u'Enter your city: ')
    user_state = SelectField(u'Enter your state: ',choices=state_tuples)
    ind_or_group = RadioField(u'Do you prefer an individual provider or a company/group?', choices=[('ind',"Individual"),('gr','Group'),('np','No Preference')])
#    remote = RadioField(u'Do you need a phone / video call / remote option?', choices=[('remote','Remote only'),('inperson','In-Person only'),('either','No preference (both)')])

    submit = SubmitField('Find Doctors')

######## flask pages ####################

@app.route('/',methods=['GET','POST'])
def home():

    form = FilterForm()
    if form.is_submitted():
        session['psychiatrist'] = form.psychiatrist.data
        session['psychologist'] = form.psychologist.data
        session['therapist'] = form.therapist.data
#        session['insurance'] = form.insurance.data
#        session['mf'] = form.mf.data
#        session['remote'] = form.remote.data
#        session['user_street'] = form.user_street.data
        session['user_city'] = form.user_city.data
        session['user_state'] = form.user_state.data
        session['ind_or_group'] = form.ind_or_group.data

        return redirect(url_for('result'))

    return render_template('home.html', form=form)

@app.route('/result')
def result():

    psychiatrist = session['psychiatrist']
    psychologist = session['psychologist']
    therapist = session['therapist']
#    insurance = session['insurance']
#    mf = session['mf']
#    remote = session['remote']
#    user_street = session['user_street']
    user_city = session['user_city']
    user_state = session['user_state']
    ind_or_group = session['ind_or_group']

    psychlist = therapistscraper.scrapeTherapy(user_city,user_state)

    return render_template('result.html',psychlist=psychlist)

if __name__ == '__main__':
    app.run(debug=True)
