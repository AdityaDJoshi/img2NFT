from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, request, render_template, flash
import os
from datetime import datetime
from a import post_to_nftport

app = Flask(__name__)

UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'AJDJRJS24$($(#$$33--'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/uploaded', methods=['GET', 'POST'])
def upload():
    print(request.files)
    print(request.form)
    print(request.form['nft_name'])
    if request.method == 'POST':

        if 'image' not in request.files:
            flash('No image found')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(datetime.now())+secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = post_to_nftport(name=request.form['nft_name'], description=request.form['nft_desc'], img_path=os.path.join(
                app.config['UPLOAD_FOLDER'], filename), wallet_address=request.form['wallet'])
            print(result)
            if 'response' in result:
                if result['response'] == 'OK':
                    return render_template("uploaded.html", filename=filename, veri_url=result['transaction_external_url'])
                else:
                    return render_template("error.html")
            else:
                return render_template("error.html")

            # return render_template("uploaded.html", filename=filename)
    return render_template("error.html")


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
