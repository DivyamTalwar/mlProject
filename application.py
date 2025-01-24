from flask import Flask, request, render_template 
import numpy as np  
import pandas as pd 
from sklearn.preprocessing import StandardScaler 
from src.Pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__) #Just for the deployment purpose as the eb requires application.py as entry point
app = application  # Initialize the Flask application


@app.route('/')
def index():
    return render_template('index.html')  # Ren der the index.html template

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    
    else:  # If the request is POST (form submission)
        data = CustomData( 
            gender=request.form.get('gender'),  #Used To Fetch The Form Data
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))
        )
        pred_df = data.get_data_as_data_frame()  # Convert the input data to a DataFrame
        print(pred_df)
        print("Before Prediction")
        
        predict_pipeline = PredictPipeline()  # Create an object of the prediction pipeline
        print("Mid Prediction")  # Debug message
        results = predict_pipeline.predict(pred_df)
        print("after Prediction")  # Debug message
        
        return render_template('home.html', results=results[0])  # Render the home.html template with the prediction result

if __name__ == "__main__":
    app.run(host="0.0.0.0")
