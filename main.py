from flask import Flask, flash, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/opencv'
app.config['UPLOAD_FOLDER'] = 'D:/Projects/open cv/Rana Sir project/static/uploads'


class File(db.Model):
    date = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    size = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(80), nullable=False)


@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        # flash(filename)

        email = request.form.get("email")
        filesize = request.form.get("filesize")

        entry = File(date=datetime.now(), email=email, size=filesize, filename=filename)
        db.session.add(entry)
        db.session.commit()

    return render_template("index.html")


app.run(debug=True)
