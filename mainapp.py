from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import shortuuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2000), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, long_url):
        self.long_url = long_url
        self.short_url = shortuuid.uuid()[:8]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('ori_url')  # Change 'long_url' to 'ori_url'
    if long_url:
        url = URL(long_url)
        db.session.add(url)
        db.session.commit()
        return render_template('result.html', short_url=url.short_url)
    return redirect(url_for('index'))

@app.route('/<short_url>')
def expand_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.long_url)
    return "URL not found."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
