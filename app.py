from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Ensure an 'uploads' folder exists to store the files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csv_file' not in request.files:
        return "No file part"
    
    file = request.files['csv_file']
    
    if file.filename == '':
        return "No selected file"

    if file and file.filename.endswith('.csv'):
        # Save the file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Read the CSV using Pandas to prove it works
        df = pd.read_csv(filepath)
        
        # Return a simple preview of the data
        return f"File uploaded successfully! <br><br> Data Preview:<br> {df.head().to_html()}"
    
    return "Invalid file type. Please upload a CSV."

if __name__ == '__main__':
    app.run(debug=True)