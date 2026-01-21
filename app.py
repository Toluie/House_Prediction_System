from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the saved model
model = joblib.load('model/house_price_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect inputs from the form
        data = {
            'OverallQual': [int(request.form['OverallQual'])],
            'GrLivArea': [float(request.form['GrLivArea'])],
            'TotalBsmtSF': [float(request.form['TotalBsmtSF'])],
            'GarageCars': [int(request.form['GarageCars'])],
            'YearBuilt': [int(request.form['YearBuilt'])],
            'Neighborhood': [request.form['Neighborhood']]
        }
        input_df = pd.DataFrame(data)
        prediction = model.predict(input_df)[0]
        return render_template('index.html', prediction=f"${prediction:,.2f}")
    except:
        return render_template('index.html', prediction="Error: Please check your inputs.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
