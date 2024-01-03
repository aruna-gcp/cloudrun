from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import pandas as pd
from google.cloud import storage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Google Cloud Storage Configuration
GCS_BUCKET_NAME = 'your-gcs-bucket-name'
GCS_PROJECT_ID = 'your-project-id'

storage_client = storage.Client(project=GCS_PROJECT_ID)

# Form for file upload
class UploadForm(FlaskForm):
    file = FileField('Upload Excel File')

# Route to handle file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        # Save file with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename_with_timestamp = f"{timestamp}_{filename}"

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_with_timestamp))

        # Upload to Google Cloud Storage
        bucket = storage_client.get_bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(filename_with_timestamp)
        blob.upload_from_filename(os.path.join(app.config['UPLOAD_FOLDER'], filename_with_timestamp))

        return redirect(url_for('success'))

    return render_template('upload.html', form=form)

# Success route
@app.route('/success')
def success():
    return 'File uploaded successfully!'
