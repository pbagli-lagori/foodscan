import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import llm as llm

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploaded_images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

# Simple user class for demo
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Mock user (you can add a database later)
users = {'testuser': {'password': 'password123'}}

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Allowed file type check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route: Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('upload_image'))
        else:
            flash('Invalid credentials, please try again.')
    
    return render_template('login.html')

# Route: Upload image page (only accessible after login)
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extracted_text = process_image(file_path)
            # result_string = ""
            return render_template('result.html', text=extracted_text)
    return render_template('upload.html')
# Function to simulate the LLM or use pytesseract for OCR

def process_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        text = llm.llm_process(image_bytes)
        return text
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Route: Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Main entry point
if __name__ == '__main__':
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
