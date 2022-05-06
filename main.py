from flask import Flask, flash, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'super-secret-key'
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME="aaabb29072002@gmail.com",
    MAIL_PASSWORD="ab@12345"
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/opencv'
app.config['UPLOAD_FOLDER'] = 'D:/Projects/open cv/Rana Sir project/static/uploads'

mail = Mail(app)


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
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))

        email = request.form.get("email")
        filesize = os.path.getsize("static/uploads/" + filename)

        entry = File(date=datetime.now(), email=email,
                     size=filesize, filename=filename)
        db.session.add(entry)
        db.session.commit()

        msg = Message(subject=filename, sender="divyamjain2907@gmail.com",
                      recipients=[email], body="Your file has been uploaded successfully\nFile Size: " + str(filesize/1025.14) + " KBs")
        with app.open_resource("static/uploads/" + filename) as fp:
            msg.attach(filename, "image/png", fp.read())
            mail.send(msg)

    return render_template("index.html")


app.run(debug=True)
