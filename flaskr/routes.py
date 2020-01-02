from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1230mmm@127.0.0.1:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Float)


def init_db():
    db.drop_all()
    db.create_all()
    book1 = Books(name='haha', price=2)
    book2 = Books(name='xixi', price=5)
    book3 = Books(name='heihei', price=3)
    book4 = Books(name='xiyou', price=1)
    book5 = Books(name='shuihu', price=6)
    book6 = Books(name='honglou', price=7)
    book7 = Books(name='ccc', price=7)
    book8 = Books(name='java', price=8)
    book9 = Books(name='python', price=32)
    book10 = Books(name='typescript', price=3)
    db.session.add_all([book1, book2, book3, book4, book5, book6, book7, book8, book9, book10])
    db.session.commit()


init_db()


@app.route('/')
def index():
    return "hi, world"


@app.route('/pages')
def pages():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)
    pagination = Books.query.order_by(Books.id.desc()).paginate(page, per_page)
    books = pagination.items
    return render_template('index.html', pagination=pagination, books=books)


# File Upload
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg']
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
UPLOAD_FLODER = './uploads'


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=["GET", "POST"])
def upload_filename():
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FLODER, filename))
            return "Upload Successfully!"
        else:
            return "Upload Failed"
    else:
        return render_template("upload.html")




if __name__ == '__main__':
    app.run()