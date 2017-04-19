import logging
from flask import Flask, request, session, redirect, url_for
from filemanager import storage, crud
from flask import render_template
import hashlib, uuid

app = Flask(__name__)
app.secret_key = 'F12Zr47j3yX R~X@lH!jmM]Lwf/,?KT'


@app.before_request
def session_management():
    session.permanent = True


"""
@Method_Name: index
@Description: This method renders login/dashboard based on the session state
"""


@app.route('/')
def index():
    if "user" in session:
        return render_template('filemanager/dashboard.html')
    return render_template('filemanager/login.html')


"""
@Method_Name: upload
@Description: This methods add a file to google cloud bucket and add an entry to data store
"""


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        if request.method == 'POST':
            file = request.files.get('file')
            if not file:
                return render_template("filemanager/failure.html")

            title = request.form['title']
            description = request.form['description']

            file_url = storage.store_file(file)
            crud.store_data(title=title, description=description, file_url=file_url, filename=file.filename,
                            size=len(file.read()))
            return render_template("filemanager/successful.html")
    except Exception as e:
        logging.exception(e)
        return render_template("filemanager/failure.html")

    return render_template("filemanager/upload.html")


"""
@Method_Name: files
@Description: This method returns the list of files in google cloud directory
"""


@app.route('/files', methods=['GET'])
def files():
    try:
        uploaded_files = crud.retrieve_files()
        text_files = []
        audio_files = []
        for uploaded_file in uploaded_files:
            if ".mp3" in uploaded_file['url']:
                audio_files.append(uploaded_file)
            else:
                text_files.append(uploaded_file)
    except Exception as e:
        logging.exception(e)
        return render_template("filemanager/failure.html")
    return render_template("filemanager/files.html", text_files=text_files, audio_files=audio_files)


"""
@Method_Name: login
@Description: This method validate user credentials
"""


@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        input_password = request.form['password']
        user = crud.get_user(email)
        salt = None
        stored_password = None
        for data in user:
            salt = data['salt']
            stored_password = data['password']
        hashed_password = hashlib.sha512(input_password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

        if hashed_password == stored_password:
            session.clear()
            session["user"] = email
            return render_template("filemanager/dashboard.html")
    except Exception as e:
        logging.exception(e)
    return render_template("filemanager/failure.html")


"""
@Method_Name: logout
@Description: This method delete the session attribute
"""


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))


"""
@Method_Name: register
@Description: This method allows the user to join the data store application
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            if request.form['password'] != request.form['confirmPassword']:
                return render_template("filemanager/failure.html")
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            crud.add(email=email, password=hashed_password, salt=salt)
            return render_template("filemanager/successful.html")
    except Exception as e:
        logging.exception(e)
        return render_template("filemanager/failure.html")
    return render_template("filemanager/register.html")


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return render_template("filemanager/failure.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
