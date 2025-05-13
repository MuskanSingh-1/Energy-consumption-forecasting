This Streamlit web application predicts energy consumption (in kWh) based on user input: month, humidity, and wind speed. It also estimates the energy cost and optionally fetches real-time weather data using a location input.

🚀 Features
->Predict energy consumption using a trained machine learning model.
->Fetch live humidity and wind speed data via the WeatherAPI.
->Estimate electricity costs using user-defined rates.
->Download prediction reports in CSV format.
->Clean, responsive interface with customized styling.

📁 Project Structure
├── app.py                    # Main Streamlit app  
├── energy_model.pkl         # Trained machine learning model  
├── model_train.ipynb        # Jupyter notebook used to train the model  
├── weather-energy-data-update.csv # Dataset used for training  
├── README.md                # Project documentation  

🧠 Model Training
The model was trained using a regression algorithm on the following features:
->Month
->Humidity
->Wind Speed

Refer to model_train.ipynb for full training details.

🌐 Usage
To run the app:
Enter "python -m streamlit run app.py" in the command prompt of the folder where app.py is present.
*NOTE:* Save all the four files in same folder.

Use the sidebar to:
->Enter a location (optional) for live weather.
->Set month, humidity, and wind speed.
->Predict energy usage and estimate cost.
->Download the result as a CSV report.

🔐 Weather API
The app uses WeatherAPI for live weather data. Replace the placeholder key in app.py:
api_key = "your_api_key_here"
