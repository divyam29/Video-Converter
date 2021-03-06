from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from grayscale import convert_to_grayscale
from movie import *

app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME="aaabb29072002@gmail.com",
    MAIL_PASSWORD="kbhicbsdwympyexp"
)

basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/opencv'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

upload_dir = os.path.join(os.getcwd(), 'static/uploads').replace(os.sep, '/')
app.config['UPLOAD_FOLDER'] = upload_dir

db = SQLAlchemy(app)
mail = Mail(app)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)


class File(db.Model):
    date = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    size = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(80), nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))

        email = request.form.get("email")
        resize = request.form.get("resize")
        grayscale = request.form.get("grayscale")

        modified_file=edit_video(filename,resize,grayscale)
        
        filesize = os.path.getsize(modified_file)
        entry = File(date=datetime.now(), email=email,
                     size=filesize, filename=filename)
        db.session.add(entry)
        db.session.commit()

        gfile = drive.CreateFile(
            {'parents': [{'id': '1gB6cfJFNvWwS9CT3_c4KLpDIjvkU8g2u'}]})
        # Read file and set it as the content of this instance.
        gfile.SetContentFile(modified_file)
        gfile.Upload()  # Upload the file.

        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(
            '1gB6cfJFNvWwS9CT3_c4KLpDIjvkU8g2u')}).GetList()
        # print()
        for file in file_list:
            if file['title'] == modified_file:
                # print(file['title']+" : "+file['id'])
                file_id=file['id']
                break
            # print('title: %s, id: %s' % (file['title'], file['id']))
        # print()

        msg = Message(subject="Here is your edited file", sender="aaabb29072002@gmail.com",
                      recipients=[email], body=f'Your file has been uploaded successfully\nFile Size: {str(round(filesize/1025140,2))} MBs\nHere is the link to your file:\nhttps://drive.google.com/file/d/{file_id}/view')
        # with app.open_resource("static/modified/" + filename) as fp:
        #     msg.attach(filename, "image/png", fp.read())
        mail.send(msg)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
