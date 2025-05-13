import pandas as pd
import numpy as np
import streamlit as st
import pickle
import requests

# Set Streamlit page configuration
st.set_page_config(
    page_title="Energy Consumption Prediction",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load the trained model
try:
    with open('energy_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {background-color: #f5f1e3;} /* Light beige background */
    div[data-testid="stSidebar"] {background-color: #d6c5b3;} /* Soft light brown sidebar */
    h1, h2, h3, h4 {color: #3e2c1c;} /* Dark brown color for headers */
    .stButton>button {
        background-color: #8c6d4d; /* Warm brown button */
        color: white;
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton>button:hover {
        background-color: #a08e72; /* Lighter brown on hover */
        color: #3e2c1c; /* Dark brown text on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Title and description
st.title("🏠 Energy Consumption Prediction")
st.write("This app predicts energy consumption based on **month**, **humidity**, and **wind speed**. Use the inputs in the sidebar to get your prediction.")

# Fetch weather data function
def fetch_weather(location):
    api_key = "57b63074513c46fb942182031241712"  
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        humidity = weather_data['current']['humidity']
        wind_speed = weather_data['current']['wind_kph']
        return humidity, wind_speed
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None, None

# Sidebar inputs
st.sidebar.header("Input Parameters")
location = st.sidebar.text_input("Enter Location for Weather Data")
if st.sidebar.button("Fetch Weather Data"):
    if location:
        humidity, wind_speed = fetch_weather(location)
        if humidity is not None and wind_speed is not None:
            st.sidebar.success(f"Weather data fetched for {location}:")
            st.sidebar.write(f"- Humidity: {humidity}%")
            st.sidebar.write(f"- Wind Speed: {wind_speed} km/h")
    else:
        st.sidebar.error("Please enter a location.")

month = st.sidebar.selectbox("Select Month", range(1, 13))
humidity = st.sidebar.slider("Humidity (%)", min_value=0, max_value=100, value=50 if 'humidity' not in locals() else humidity)
wind_speed = st.sidebar.slider("Wind Speed (km/h)", min_value=0.0, max_value=50.0, value=10.0 if 'wind_speed' not in locals() else wind_speed)

# Check if model exists
if model is None:
    st.error("Model not found. Please train the model first using train_model.ipynb.")
else:
    # Make prediction
    if st.sidebar.button("Predict"):
        input_features = np.array([[month, humidity, wind_speed]])
        prediction = model.predict(input_features)
        
        # Display prediction
        st.success(f"Predicted Energy Consumption: **{prediction[0]:.2f} kWh**")

        # Prediction report
        prediction_data = pd.DataFrame({
            "Month": [month],
            "Humidity (%)": [humidity],
            "Wind Speed (km/h)": [wind_speed],
            "Predicted Energy Consumption (kWh)": [prediction[0]]
        })

        st.write("### Prediction Report")
        st.dataframe(prediction_data, use_container_width=True)

        # Download button for the report
        csv_data = prediction_data.to_csv(index=False)
        st.download_button(
            label="🔗 Download Prediction Report",
            data=csv_data,
            file_name="prediction_report.csv",
            mime="text/csv"
        )

    # Energy cost estimation
    st.subheader("Energy Cost Estimation")
    cost_per_kWh = st.number_input("Enter cost per kWh (in Rs.):", min_value=0.0, value=10.0, step=0.5)
    if 'prediction' in locals() and prediction is not None:
        energy_cost = prediction[0] * cost_per_kWh
        st.success(f"Estimated Energy Cost: **{energy_cost:.2f} Rs./-**")