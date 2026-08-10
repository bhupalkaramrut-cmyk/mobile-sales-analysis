# data_utils.py
import streamlit as st
import pandas as pd
import random

def load_data(uploaded_file):
    """Load a CSV or Excel file into a DataFrame."""
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return None
    return None

def get_analysis_data(df):
    """Ensure required columns exist; fill missing with synthetic data."""
    if df is None or df.empty:
        return None
    df = df.copy()
    if 'Brand' not in df.columns:
        for col in df.columns:
            if 'brand' in col.lower():
                df['Brand'] = df[col]
                break
        else:
            df['Brand'] = 'Unknown'
    if 'Revenue' not in df.columns:
        for col in df.columns:
            if 'revenue' in col.lower() or 'sales' in col.lower() or 'amount' in col.lower():
                df['Revenue'] = df[col]
                break
        else:
            df['Revenue'] = df.apply(lambda x: random.randint(10000, 100000), axis=1)
    if 'Region' not in df.columns:
        for col in df.columns:
            if 'region' in col.lower():
                df['Region'] = df[col]
                break
        else:
            df['Region'] = random.choice(['North', 'South', 'East', 'West', 'Central'])
    if 'Units_Sold' not in df.columns:
        for col in df.columns:
            if 'unit' in col.lower() or 'quantity' in col.lower():
                df['Units_Sold'] = df[col]
                break
        else:
            df['Units_Sold'] = random.randint(1, 100)
    if 'Month' not in df.columns:
        for col in df.columns:
            if 'month' in col.lower() or 'date' in col.lower():
                df['Month'] = df[col]
                break
        else:
            df['Month'] = random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
    if 'Price' not in df.columns:
        df['Price'] = random.randint(500, 3000)
    return df

def render_no_data_message():
    """Display a placeholder when no data is available."""
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; 
                min-height:300px; text-align:center; background:rgba(0,0,0,0.6); 
                border-radius:12px; padding:24px; border:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:40px; margin-bottom:12px;">📂</div>
        <h2 style="color:#ffffff; font-weight:600; margin-bottom:6px; font-size:18px;">No Data Uploaded</h2>
        <p style="color:rgba(255,255,255,0.5); font-size:12px; max-width:500px; line-height:1.4;">
            Please upload a CSV file using the <strong>Upload Data</strong> page or the <strong>Home</strong> page to see analysis.
        </p>
        <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap; justify-content:center;">
            <span style="background:rgba(255,255,255,0.05); padding:3px 12px; border-radius:20px; color:rgba(255,255,255,0.4); font-size:10px;">CSV</span>
            <span style="background:rgba(255,255,255,0.05); padding:3px 12px; border-radius:20px; color:rgba(255,255,255,0.4); font-size:10px;">XLSX</span>
            <span style="background:rgba(255,255,255,0.05); padding:3px 12px; border-radius:20px; color:rgba(255,255,255,0.4); font-size:10px;">200MB max</span>
        </div>
    </div>
    """, unsafe_allow_html=True)