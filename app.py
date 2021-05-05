from flask import Flask, render_template, request
from werkzeug.utils import secure_filename 
import os
import zipfile
from threading import Thread
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///zip.db"
db = SQLAlchemy(app)

class FileZip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isi_file = db.Column(db.String(250)) 

ALLOWED_EXTENSION = set(['zip'])
app.config['UPLOAD_FOLDER'] = 'hasil'

#pengecekan file degan menggunakan rsplit
def allowed_file(filename):
    threads = []
    for i in range(1):
        threads.append(Thread(target=allowed_file))
        threads[-1].start()
    for thread in threads:
        thread.join()
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/hasil', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        file = request.files['file']

        if 'file' not in request.files:
            return render_template('hasil.html')

        if file.filename == '':
            return render_template('hasil.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
            with zipfile.ZipFile('hasil'+'//'+filename) as zf:
                zf.extractall('hasil')

                zfile = zf.namelist()
                z = (", ".join(zfile))

                newFile = FileZip(isi_file=z)
                db.session.add(newFile)
                db.session.commit()
                            
            return 'file ' + filename +' di simpan' + ' <a href="/hasil">kembali</a>'

    return render_template('hasil.html')

if __name__ == '__main__':
    app.run(debug=True)