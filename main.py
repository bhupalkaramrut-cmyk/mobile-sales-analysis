# main.py
import streamlit as st
from config import get_css
from sidebar import render_sidebar
from data_utils import load_data, get_analysis_data, render_no_data_message
from page_renderers import (
    render_home,
    render_dashboard,
    render_sales_insights,
    render_top_brands,
    render_customer_analysis,
    render_revenue_analysis,
    render_reports,
    render_upload_data,
)

# ---------- INIT SESSION STATE ----------
if 'df' not in st.session_state:
    st.session_state.df = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# ---------- APPLY DYNAMIC CSS ----------
current_page = st.session_state.page
st.markdown(get_css(current_page), unsafe_allow_html=True)

# ---------- SIDEBAR & PAGE ROUTING ----------
page = render_sidebar()          # also updates st.session_state.page if a button is pressed
df = st.session_state.df

page_map = {
    "Home": render_home,
    "Dashboard": render_dashboard,
    "Sales Insights": render_sales_insights,
    "Top Brands": render_top_brands,
    "Customer Analysis": render_customer_analysis,
    "Revenue Analysis": render_revenue_analysis,
    "Reports": render_reports,
    "Upload Data": render_upload_data,
}

# Call the render function for the current page
page_map.get(page, render_home)(df)