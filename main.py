from distutils.command.upload import upload
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google_drive_downloader import GoogleDriveDownloader as gdd

app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME="aaabb29072002@gmail.com",
    MAIL_PASSWORD="ab@12345"
)

basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/opencv'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

upload_dir=os.path.join(os.getcwd(),'static/uploads').replace(os.sep,'/')
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


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))

        email = request.form.get("email")
        filesize = os.path.getsize("static/uploads/" + filename)

        entry = File(date=datetime.now(), email=email,
                     size=filesize, filename=filename)
        db.session.add(entry)
        db.session.commit()

        # msg = Message(subject=filename, sender="aaabb29072002@gmail.com",
        #               recipients=[email], body="Your file has been uploaded successfully\nFile Size: " + str(filesize/1025.14) + " KBs")
        # with app.open_resource("static/uploads/" + filename) as fp:
        #     msg.attach(filename, "image/png", fp.read())
        #     mail.send(msg)

        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile(
                {'parents': [{'id': '1gB6cfJFNvWwS9CT3_c4KLpDIjvkU8g2u'}]})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile("static/uploads/" + upload_file)
            gfile.Upload()  # Upload the file.

        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(
            '1gB6cfJFNvWwS9CT3_c4KLpDIjvkU8g2u')}).GetList()
        for file in file_list:
            if file['title'] == "static/uploads/"+filename:
                file_id = file['id']
                print(file['title']+" : "+file['id'])

            print('title: %s, id: %s' % (file['title'], file['id']))

    return render_template("index.html")


app.run(debug=True)
