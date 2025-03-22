# import streamlit as st
# import pandas as pd
# import joblib
# import tensorflow as tf
# import matplotlib.pyplot as plt
# import plotly.express as px
# from datetime import datetime, timedelta

# # Streamlit dashboard title
# st.title("⚡ Electricity Demand Forecast Dashboard")

# # Load trained model (.h5)
# model = tf.keras.models.load_model('lstm_electricity_model.h5', compile=False)
# st.success("✅ LSTM model loaded successfully!")

# # Load scaler
# scaler_X = joblib.load('scaler_X.pkl')
# scaler_y = joblib.load('scaler_y.pkl')

# # Sidebar slider to select forecast horizon (1 to 30 days)
# forecast_days = st.sidebar.slider("Select Forecast Horizon (in Days)", min_value=1, max_value=30, value=7)

# # Sidebar toggle for plot selection
# plot_type = st.sidebar.radio("Choose Plot Type", ('Actual vs Predicted', 'Forecast Only'))

# # Load dataset
# data = pd.read_csv('new_data_simulated.csv')
# data['date'] = pd.to_datetime(data['date'])

# # Shift dataset dates to start from today
# today = datetime.today()
# days_to_shift = (today - data['date'].min()).days
# data['date'] = data['date'] + pd.Timedelta(days=days_to_shift)

# # Forecast window (next N days from today)
# start_date = data['date'].min()
# end_date = start_date + timedelta(days=forecast_days - 1)
# forecast_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# if forecast_data.empty:
#     st.warning("No data available for the selected forecast range.")
# else:
#     # Define features used for LSTM model
#     features = ['day_of_week', 'hour_of_day', 'is_weekend', 'temperature',
#                 'is_holiday', 'solar_generation', 'is_summer', 'is_winter', 'is_monsoon']

#     # Scale features
#     X_forecast = scaler_X.transform(forecast_data[features])
#     X_forecast = X_forecast.reshape((X_forecast.shape[0], 1, X_forecast.shape[1]))

#     # Predict electricity demand
#     y_pred_scaled = model.predict(X_forecast)
#     y_pred = scaler_y.inverse_transform(y_pred_scaled)

#     # Append predictions to dataframe
#     forecast_data['predicted_demand'] = y_pred

#     # Animated Plotly Graph based on selection
#     if plot_type == 'Actual vs Predicted':
#         fig = px.line(forecast_data, x='date', y=['electricity_demand', 'predicted_demand'],
#                       labels={'value': 'Electricity Demand', 'variable': 'Legend'},
#                       title=f'📈 Forecast for {forecast_days} Day(s) from {start_date.date()}')
#     else:
#         fig = px.line(forecast_data, x='date', y=['predicted_demand'],
#                       labels={'predicted_demand': 'Predicted Demand'},
#                       title=f'📈 Forecast Only for {forecast_days} Day(s) from {start_date.date()}')

#     st.plotly_chart(fig, use_container_width=True)

#     # Show dataframe
#     st.dataframe(forecast_data[['date', 'hour_of_day', 'electricity_demand', 'predicted_demand']])

#     # Download predictions as CSV
#     csv = forecast_data.to_csv(index=False).encode('utf-8')
#     st.download_button("⬇️ Download Forecast CSV", data=csv, file_name='forecasted_data.csv', mime='text/csv')

# import streamlit as st
# import pandas as pd
# import joblib
# import tensorflow as tf
# import plotly.graph_objects as go
# import plotly.express as px
# from datetime import datetime, timedelta

# # Streamlit dashboard title
# st.title("⚡ Electricity Demand Forecast Dashboard")

# # Load trained model (.h5)
# model = tf.keras.models.load_model('lstm_electricity_model.h5', compile=False)
# st.success("✅ LSTM model loaded successfully!")

# # Load scaler
# scaler_X = joblib.load('scaler_X.pkl')
# scaler_y = joblib.load('scaler_y.pkl')

# # Sidebar slider to select forecast horizon (1 to 30 days)
# forecast_days = st.sidebar.slider("Select Forecast Horizon (in Days)", min_value=1, max_value=30, value=7)

# # Load dataset
# data = pd.read_csv('new_data_simulated.csv')
# data['date'] = pd.to_datetime(data['date'])

# # Shift dataset dates to start from today
# today = datetime.today()
# days_to_shift = (today - data['date'].min()).days
# data['date'] = data['date'] + pd.Timedelta(days=days_to_shift)

# # Forecast window (next N days from today)
# start_date = data['date'].min()
# end_date = start_date + timedelta(days=forecast_days - 1)
# forecast_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# if forecast_data.empty:
#     st.warning("No data available for the selected forecast range.")
# else:
#     # Define features used for LSTM model
#     features = ['day_of_week', 'hour_of_day', 'is_weekend', 'temperature',
#                 'is_holiday', 'solar_generation', 'is_summer', 'is_winter', 'is_monsoon']

#     # Scale features
#     X_forecast = scaler_X.transform(forecast_data[features])
#     X_forecast = X_forecast.reshape((X_forecast.shape[0], 1, X_forecast.shape[1]))

#     # Predict electricity demand
#     y_pred_scaled = model.predict(X_forecast)
#     y_pred = scaler_y.inverse_transform(y_pred_scaled)

#     # Append predictions to dataframe
#     forecast_data['predicted_demand'] = y_pred

#     # ===== Chart 1: Combination Chart (Bar + Line) =====
#     combo_fig = go.Figure()
#     combo_fig.add_trace(go.Bar(
#         x=forecast_data['date'],
#         y=forecast_data['predicted_demand'],
#         name='Predicted Demand',
#         marker_color='indianred'
#     ))
#     combo_fig.add_trace(go.Scatter(
#         x=forecast_data['date'],
#         y=forecast_data['temperature'],
#         name='Temperature',
#         yaxis='y2',
#         mode='lines',
#         line=dict(color='blue')
#     ))
#     combo_fig.update_layout(
#         title='📊 Predicted Demand vs Temperature',
#         yaxis=dict(title='Predicted Demand (MW)'),
#         yaxis2=dict(title='Temperature (°C)', overlaying='y', side='right'),
#         template='plotly_white'
#     )
#     st.plotly_chart(combo_fig, use_container_width=True)

#     # ===== Chart 2: Heatmap (Hourly vs Predicted Demand) =====
#     heatmap_data = forecast_data.pivot_table(index='hour_of_day', columns='date', values='predicted_demand')
#     heatmap_fig = px.imshow(heatmap_data, aspect='auto', color_continuous_scale='Viridis',
#                             labels=dict(color="Predicted Demand (MW)"))
#     heatmap_fig.update_layout(title="🔥 Predicted Demand Heatmap (Hour vs Date)")
#     st.plotly_chart(heatmap_fig, use_container_width=True)

#     # ===== Chart 3: Boxplot of Predicted Demand =====
#     boxplot_fig = px.box(forecast_data, x='is_weekend', y='predicted_demand',
#                          labels={'is_weekend': 'Weekend (1=Yes, 0=No)', 'predicted_demand': 'Predicted Demand'},
#                          title="📦 Predicted Demand Distribution by Weekend")
#     st.plotly_chart(boxplot_fig, use_container_width=True)

#     # Show dataframe with only date & predicted_demand
#     st.dataframe(forecast_data[['date', 'predicted_demand']])

#     # Download predictions as CSV (only predicted_demand)
#     csv = forecast_data[['date', 'predicted_demand']].to_csv(index=False).encode('utf-8')
#     st.download_button("⬇️ Download Predicted CSV", data=csv, file_name='predicted_data.csv', mime='text/csv')


import streamlit as st
import pandas as pd
import joblib
import tensorflow as tf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.title("Electricity Demand Forecast Dashboard by team BXCD")

model = tf.keras.models.load_model('lstm_electricity_model.h5', compile=False)
st.success("model loaded successfully!")

scaler_X = joblib.load('scaler_X.pkl')
scaler_y = joblib.load('scaler_y.pkl')

forecast_days = st.sidebar.slider("Select Forecast Horizon (in Days)", min_value=1, max_value=30, value=7)
view_option = st.sidebar.radio("Choose View Mode", ('Actual vs Predicted', 'Predicted Only'))
data = pd.read_csv('new_data_simulated.csv')
data['date'] = pd.to_datetime(data['date'])

today = datetime.today()
days_to_shift = (today - data['date'].min()).days
data['date'] = data['date'] + pd.Timedelta(days=days_to_shift)


start_date = data['date'].min()
end_date = start_date + timedelta(days=forecast_days - 1)
forecast_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

if forecast_data.empty:
    st.warning("No data available for the selected forecast range.")
else:
    # here is the which consider the all factor to predict the demand
    features = ['day_of_week', 'hour_of_day', 'is_weekend', 'temperature',
                'is_holiday', 'solar_generation', 'is_summer', 'is_winter', 'is_monsoon']


    X_forecast = scaler_X.transform(forecast_data[features])
    X_forecast = X_forecast.reshape((X_forecast.shape[0], 1, X_forecast.shape[1]))

    
    y_pred_scaled = model.predict(X_forecast)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    forecast_data['predicted_demand'] = y_pred

    
    line_fig = go.Figure()
    if view_option == 'Actual vs Predicted':
        line_fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['electricity_demand'],
                                      mode='lines+markers', name='Actual Demand', line=dict(color='royalblue')))
    line_fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['predicted_demand'],
                                  mode='lines+markers', name='Predicted Demand', line=dict(color='firebrick')))
    line_fig.update_layout(title='📈 Line Graph: Electricity Demand', template='plotly_white')
    st.plotly_chart(line_fig, use_container_width=True)

    
    bar_fig = px.bar(forecast_data, x='date', y='predicted_demand',
                     title='📊 Bar Chart: Predicted Demand')
    st.plotly_chart(bar_fig, use_container_width=True)

    
    area_fig = px.area(forecast_data, x='date', y='predicted_demand',
                       title='🌊 Area Chart: Predicted Demand')
    st.plotly_chart(area_fig, use_container_width=True)

    
    scatter_fig = px.scatter(forecast_data, x='temperature', y='predicted_demand', trendline='ols',
                             title='⚡ Scatter Plot: Temperature vs Predicted Demand')
    st.plotly_chart(scatter_fig, use_container_width=True)

    
    combo_fig = go.Figure()
    combo_fig.add_trace(go.Bar(x=forecast_data['date'], y=forecast_data['predicted_demand'], name='Predicted Demand'))
    combo_fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['temperature'],
                                   yaxis='y2', name='Temperature', mode='lines'))
    combo_fig.update_layout(title='🔗 Predicted Demand vs Temperature',
                            yaxis=dict(title='Predicted Demand (MW)'),
                            yaxis2=dict(title='Temperature (°C)', overlaying='y', side='right'),
                            template='plotly_white')
    st.plotly_chart(combo_fig, use_container_width=True)

    
    heatmap_data = forecast_data.pivot_table(index='hour_of_day', columns='date', values='predicted_demand')
    heatmap_fig = px.imshow(heatmap_data, aspect='auto', color_continuous_scale='Viridis')
    heatmap_fig.update_layout(title="🔥 Heatmap: Predicted Demand")
    st.plotly_chart(heatmap_fig, use_container_width=True)

    
    boxplot_fig = px.box(forecast_data, x='is_weekend', y='predicted_demand',
                         title="📦 Boxplot: Demand by Weekend")
    st.plotly_chart(boxplot_fig, use_container_width=True)
    st.dataframe(forecast_data[['date', 'predicted_demand']])
    csv = forecast_data[['date', 'predicted_demand']].to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Predicted CSV", data=csv, file_name='predicted_data.csv', mime='text/csv')