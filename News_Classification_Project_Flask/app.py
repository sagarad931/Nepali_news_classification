from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import pickle
import sklearn
import numpy as np

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                             InputRequired(), Length(min=4, max=20)])

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)])

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError
            ('That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)])

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)])

    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html' , username=current_user.username)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username = request.form.get('username')
    password = request.form.get('password')

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)




# Load the pickled model
with open('news_pred_vectorizer.pickle', 'rb') as handle:
    vectorizer = pickle.load(handle)

with open('news_pred_model.pickle','rb') as handle:
    model=pickle.load(handle)

# @app.route('/home')
# def index():
#     return render_template('home.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
  
    name  = request.form['data'].encode('utf-8').decode('utf-8')
    # name = np.array([name]).reshape(-1, 1)

    classes= {'Agriculture': 0,
                'automobiles': 1,
                'bank': 2,
                'business': 3,
                'economy': 4,
                'education': 5,
                'entertainment': 6,
                'health': 7,
                'politics': 8,
                'sports': 9,
                'technology': 10,
                'tourism': 11,
                'world': 12}

    prd = model.predict(vectorizer.transform(
    [
      name
    ])
            ) 
    nprd = []
    for k,v in classes.items():
        for p in prd:
            if v==p:
                nprd.append(k)


    # Render a template with the prediction
    return render_template('dashboard.html', prediction=nprd[0])







if __name__ == "__main__":
    app.run(debug=True, port=8000)
