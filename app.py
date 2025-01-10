import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(layout="wide", page_title="Danaher Strategic Capacity Dashboard")

# Generate synthetic data
def generate_time_series_data():
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    
    # Base metrics with realistic manufacturing trends
    dppm = 2000 + np.random.normal(0, 200, len(dates))  # Defects Per Million Parts
    dppm = dppm * np.exp(-0.002 * np.arange(len(dates)))  # Declining trend
    
    fpy = 0.85 + 0.15 * (1 - np.exp(-0.003 * np.arange(len(dates))))  # First Pass Yield
    otd = 0.88 + 0.12 * (1 - np.exp(-0.002 * np.arange(len(dates))))  # On-Time Delivery
    
    # Process capability
    cpk = 1.0 + 0.5 * (1 - np.exp(-0.002 * np.arange(len(dates))))  # Process Capability Index
    
    # Equipment reliability
    reliability = 0.90 + 0.1 * (1 - np.exp(-0.003 * np.arange(len(dates))))
    
    df = pd.DataFrame({
        'Date': dates,
        'DPPM': dppm,
        'First_Pass_Yield': fpy * 100,
        'OTD': otd * 100,
        'Process_Cpk': cpk,
        'Equipment_Reliability': reliability * 100
    })
    
    return df

# Generate supplier capability data
def generate_supplier_data():
    suppliers = ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D', 'Supplier E']
    metrics = ['Quality', 'Delivery', 'Technical', 'Cost', 'Innovation']
    
    data = np.random.uniform(0.6, 0.95, size=(len(suppliers), len(metrics)))
    return pd.DataFrame(data * 100, columns=metrics, index=suppliers)

# Main dashboard
st.title("Strategic Capacity Optimization Dashboard")

# Generate data
df = generate_time_series_data()
supplier_df = generate_supplier_data()

# KPI Cards row
col1, col2, col3, col4 = st.columns(4)

latest_metrics = df.iloc[-1]

with col1:
    st.metric("First Pass Yield", f"{latest_metrics['First_Pass_Yield']:.1f}%", 
              f"{latest_metrics['First_Pass_Yield'] - df.iloc[-30]['First_Pass_Yield']:.1f}%")

with col2:
    st.metric("On-Time Delivery", f"{latest_metrics['OTD']:.1f}%",
              f"{latest_metrics['OTD'] - df.iloc[-30]['OTD']:.1f}%")

with col3:
    st.metric("Process Cpk", f"{latest_metrics['Process_Cpk']:.2f}",
              f"{latest_metrics['Process_Cpk'] - df.iloc[-30]['Process_Cpk']:.2f}")

with col4:
    st.metric("Equipment Reliability", f"{latest_metrics['Equipment_Reliability']:.1f}%",
              f"{latest_metrics['Equipment_Reliability'] - df.iloc[-30]['Equipment_Reliability']:.1f}%")

# Time series plots
st.subheader("Performance Trends")
metrics_to_plot = st.multiselect(
    "Select metrics to display",
    ['First_Pass_Yield', 'OTD', 'Process_Cpk', 'Equipment_Reliability'],
    default=['First_Pass_Yield', 'OTD']
)

if metrics_to_plot:
    fig = go.Figure()
    for metric in metrics_to_plot:
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[metric],
            name=metric.replace('_', ' '),
            mode='lines'
        ))
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Supplier capability heatmap
st.subheader("Supplier Capability Matrix")
fig = px.imshow(
    supplier_df,
    color_continuous_scale="RdYlGn",
    aspect="auto"
)
fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# DPPM Analysis
st.subheader("Defects Per Million Parts (DPPM) Trend")
fig = px.line(df, x='Date', y='DPPM')
fig.add_hline(y=1500, line_dash="dash", line_color="red", annotation_text="Target")
fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# Efficiency Gains Calculator
st.subheader("Efficiency Gains Analysis")
baseline_efficiency = st.slider("Baseline Efficiency (%)", 0, 100, 60)
current_efficiency = baseline_efficiency * 1.4  # 40% improvement

col1, col2 = st.columns(2)
with col1:
    st.metric("Baseline Efficiency", f"{baseline_efficiency}%")
with col2:
    st.metric("Current Efficiency", f"{current_efficiency:.1f}%", 
              f"+{(current_efficiency - baseline_efficiency):.1f}%")

# Cost Savings Breakdown
savings_data = {
    'Category': ['Process Optimization', 'Equipment Reliability', 'Quality Improvement', 'Supply Chain'],
    'Savings': [400000, 300000, 200000, 100000]
}
savings_df = pd.DataFrame(savings_data)

st.subheader("Cost Savings Breakdown ($1M Total)")
fig = px.bar(savings_df, x='Category', y='Savings', text='Savings')
# Update the text format after creating the figure
fig.update_traces(texttemplate='$%{text:,.0f}', textposition='auto')
fig.update_layout(
    height=400, 
    margin=dict(l=0, r=0, t=30, b=0),
    yaxis_title="Savings ($)",
    xaxis_title=""
)
st.plotly_chart(fig, use_container_width=True)