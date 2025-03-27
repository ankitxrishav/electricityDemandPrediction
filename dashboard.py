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


forecast_data = data.copy()
forecast_data = forecast_data.sort_values(by=['date', 'hour_of_day']).reset_index(drop=True)
forecast_data['datetime'] = forecast_data['date'] + pd.to_timedelta(forecast_data['hour_of_day'], unit='h')
forecast_data = forecast_data.sort_values('datetime')

start_datetime = forecast_data['datetime'].min()
end_datetime = start_datetime + timedelta(days=forecast_days)
forecast_data = forecast_data[(forecast_data['datetime'] >= start_datetime) & (forecast_data['datetime'] <= end_datetime)]

if forecast_data.empty:
    st.warning("No data available for the selected forecast range.")
else:

    features = ['day_of_week', 'hour_of_day', 'is_weekend', 'temperature',
                'is_holiday', 'solar_generation', 'is_summer', 'is_winter', 'is_monsoon']

    X_forecast = scaler_X.transform(forecast_data[features])
    X_forecast = X_forecast.reshape((X_forecast.shape[0], 1, X_forecast.shape[1]))

    y_pred_scaled = model.predict(X_forecast)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    forecast_data['predicted_demand'] = y_pred

    
    line_fig = go.Figure()
    if view_option == 'Actual vs Predicted':
        line_fig.add_trace(go.Scatter(x=forecast_data['datetime'], y=forecast_data['electricity_demand'],
                                      mode='lines+markers', name='Actual Demand', line=dict(color='royalblue')))
    line_fig.add_trace(go.Scatter(x=forecast_data['datetime'], y=forecast_data['predicted_demand'],
                                  mode='lines+markers', name='Predicted Demand', line=dict(color='firebrick')))
    line_fig.update_layout(title='Line Graph: Electricity Demand', template='plotly_white')
    st.plotly_chart(line_fig, use_container_width=True)

    bar_fig = px.bar(forecast_data, x='datetime', y='predicted_demand',
                     title='Bar Chart: Predicted Demand')
    st.plotly_chart(bar_fig, use_container_width=True)

    area_fig = px.area(forecast_data, x='datetime', y='predicted_demand',
                       title='Area Chart: Predicted Demand')
    st.plotly_chart(area_fig, use_container_width=True)

    scatter_fig = px.scatter(forecast_data, x='temperature', y='predicted_demand', trendline='ols',
                             title='⚡ Scatter Plot: Temperature vs Predicted Demand')
    st.plotly_chart(scatter_fig, use_container_width=True)

    combo_fig = go.Figure()
    combo_fig.add_trace(go.Bar(x=forecast_data['datetime'], y=forecast_data['predicted_demand'], name='Predicted Demand'))
    combo_fig.add_trace(go.Scatter(x=forecast_data['datetime'], y=forecast_data['temperature'],
                                   yaxis='y2', name='Temperature', mode='lines'))
    combo_fig.update_layout(title='🔗 Predicted Demand vs Temperature',
                            yaxis=dict(title='Predicted Demand (MW)'),
                            yaxis2=dict(title='Temperature (°C)', overlaying='y', side='right'),
                            template='plotly_white')
    st.plotly_chart(combo_fig, use_container_width=True)

    heatmap_data = forecast_data.pivot_table(index='hour_of_day', columns='date', values='predicted_demand')
    heatmap_fig = px.imshow(heatmap_data, aspect='auto', color_continuous_scale='Viridis')
    heatmap_fig.update_layout(title="Heatmap: Predicted Demand")
    st.plotly_chart(heatmap_fig, use_container_width=True)

    boxplot_fig = px.box(forecast_data, x='is_weekend', y='predicted_demand',
                         title="Boxplot: Demand by Weekend")
    st.plotly_chart(boxplot_fig, use_container_width=True)

    st.dataframe(forecast_data[['datetime', 'predicted_demand']])
    csv = forecast_data[['datetime', 'predicted_demand']].to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Predicted CSV", data=csv, file_name='predicted_data.csv', mime='text/csv')
