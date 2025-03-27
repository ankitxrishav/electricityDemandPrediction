# Electricity Demand Forecast Dashboard 

This project is an interactive **Streamlit Dashboard** designed to forecast electricity demand using an LSTM-based model.

##  Features
- **Interactive multi-graph dashboard**
- Forecast for **1 to 30 days** into the future
- Visualizations include:
  - Line Graph (Actual vs Predicted or Predicted Only)
  - Bar Chart
  - Area Chart
  - Scatter Plot with Trend Line
  - Combination Chart (Bar + Line)
  - Heatmap (Hour vs Date)
  - Boxplot (Weekend vs Demand)
- CSV Download feature
- Date-shifted simulated data (real-time effect)

## Model Details
- The LSTM model is pre-trained and loaded as `.h5`
- MinMaxScaler is used for feature scaling

##  Files
- `lstm_electricity_model.h5`: Pre-trained LSTM model
- `scaler_X.pkl`, `scaler_y.pkl`: Scalers for input features & target
- `new_data_simulated.csv`: Hourly data used for real-time predictions
- `dashbo.py`: Streamlit app code (this file)

##  How to Run
1. Install dependencies:
    ```bash
    pip install streamlit pandas tensorflow scikit-learn plotly joblib
    ```

2. Run the Streamlit app:
    ```bash
    streamlit run dashboard.py
    ```

##  Usage
- Select forecast horizon using the sidebar slider
- Choose to view **Actual vs Predicted** or **Predicted Only**
- Explore various charts
- Download forecasted results as CSV

##  Notes

- Data has been programmatically shifted to simulate future (2025+)
- Supports **interactive zoom & range selector** for time series graphs

---
## working screenshot actual vs predicted 



<img width="1553" alt="Screenshot 2025-03-22 at 6 18 24 AM" src="https://github.com/user-attachments/assets/3607f2c3-77e7-40f7-8f22-cdc75e3b2cfd" />


<img width="1551" alt="Screenshot 2025-03-22 at 6 18 50 AM" src="https://github.com/user-attachments/assets/37e19c26-916a-4b8b-8088-c571cc28fc66" />

<img width="1680" alt="Screenshot 2025-03-22 at 6 19 03 AM" src="https://github.com/user-attachments/assets/90be8b44-fb63-4563-b2b2-3bb068c080e0" />


<img width="1641" alt="Screenshot 2025-03-27 at 9 49 05 AM" src="https://github.com/user-attachments/assets/98c45941-22d5-4920-836d-edaf74dcf6f9" />

## working screenshot of predicted with graph change

<img width="1635" alt="Screenshot 2025-03-27 at 9 49 29 AM" src="https://github.com/user-attachments/assets/7fc367ab-d66c-474e-9f66-5dcbf04cfcb8" />

<img width="1632" alt="Screenshot 2025-03-27 at 9 49 40 AM" src="https://github.com/user-attachments/assets/afce5be1-c33c-49b6-b02a-fc8d2c296191" />


