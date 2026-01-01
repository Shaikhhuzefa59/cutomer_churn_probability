from flask import Flask, render_template, request
from flask import send_file
import pandas as pd
import pickle
import os, sys
from preprocess.preprocess import preprocess
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model & scaler
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

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

    if file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        return f"File uploaded successfully!<br><br>{df.head().to_html()}"

    return "Invalid file type"

@app.route('/predict', methods=['POST'])
def predict_file():
    file = request.files['csv_file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    pro_df = preprocess(filepath, scaler)
    predictions = model.predict(pro_df)

    scale_cols = ['Age', 'Tenure', 'Usage Frequency','Support Calls','Payment Delay','Avg_monthly_spend','Total Spend','Contract_month','Last Interaction']
    pro_df[scale_cols] = scaler.inverse_transform(pro_df[scale_cols])

    pro_df['Churn'] = predictions
    

    output_path = os.path.join(UPLOAD_FOLDER, 'predictions.csv')
    pro_df.to_csv(output_path, index=False)
    return f"""
        <h3>Prediction Completed ✅</h3>
        <a href="/download">⬇ Download Predictions CSV</a>
        <br><br>
        {pro_df.head().to_html()}
    """

@app.route('/download')
def download_file():
    return send_file(
        os.path.join(UPLOAD_FOLDER, 'predictions.csv'),as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
