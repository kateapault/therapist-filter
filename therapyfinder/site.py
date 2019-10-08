from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeholder_secret_key'
class FilterForm(FlaskForm):

#    user_street = StringField('Enter your street address: ')
#    user_city = StringField('Enter your city: ')
    user_state = StringField('Enter your state: ',validators=[DataRequired()])
    submit = SubmitField('Find Therapists')

# home page
@app.route('/',methods=['GET','POST'])
def home():

    form = FilterForm()
    if form.validate_on_submit():
        session['user_state'] = form.user_state.data
        return redirect(url_for('result'))

    return render_template('home.html',form=form)

@app.route('/result')
def result():

#   SQL stuff here
#   temp data:
    name = 'Dr. Example'
    phone = '555-555-5555'
    hours = '8am - 8pm'

    return render_template('result.html',name=name,phone=phone,hours=hours)

#page with advice on how to approach therapy
@app.route('/advice')
def advice():
    return render_template('advice.html')

if __name__ == '__main__':
    app.run(debug=True)
