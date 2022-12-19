from flask import Flask, render_template
from forms import RegisterForm 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)