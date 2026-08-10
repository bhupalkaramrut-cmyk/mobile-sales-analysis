# config.py
import streamlit as st
import pandas as pd
import plotly.express as px
import random

# ---------- PAGE CONFIG (must be first Streamlit command) ----------
st.set_page_config(
    page_title="Mobile Sales Analysis",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- BACKGROUND IMAGES ----------
BACKGROUND_IMAGES = {
    "Home": "https://videocdn.cdnpk.net/videos/18ea1b90-23c7-5a04-b66d-e8f07fb4816e/horizontal/thumbnails/large.jpg?semt=ais_hybrid&item_id=6355657&w=740&q=80",
    "Dashboard": "https://wallup.net/wp-content/uploads/2017/11/23/526001-computer-keyboards-748x421.jpg",
    "Sales Insights": "https://img.magnific.com/free-photo/flat-lay-work-desk-with-agenda-coffee-cup_23-2148397857.jpg?semt=ais_hybrid&w=740&q=80",
    "Top Brands": "https://img.magnific.com/free-photo/flat-lay-desktop-with-agenda-magnifying-glass_23-2148397834.jpg?semt=ais_test_b&w=740&q=80",
    "Customer Analysis": "https://static.vecteezy.com/ti/gratis-vector/p1/4999152/abstracte-donkere-achtergrond-met-een-cirkelvormig-patroon-geometrische-technologie-donker-ontwerp-illustratie-textuur-vector.jpg",
    "Revenue Analysis": "https://img.magnific.com/premium-photo/wallpaper-dark-black-leather-texture-background_35977-848.jpg",
    "Reports": "https://img.magnific.com/free-photo/nice-business-desk-black-background_24972-1179.jpg?semt=ais_hybrid&w=740&q=80",
    "Upload Data": "https://hq-wallpapers.ru/wallpapers/8/hq-wallpapers_ru_abstraction3d_38742_1920x1080.jpg",
}

# ---------- DYNAMIC CSS ----------
def get_css(page):
    """Return the full CSS string with the background image for the given page."""
    current_background = BACKGROUND_IMAGES.get(page, BACKGROUND_IMAGES["Home"])
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        .stApp {{
            background: #0d0d0d url('{current_background}') no-repeat center center fixed !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }}

        .main .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
            background: transparent !important;
        }}

        /* ===== HEADER ===== */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            backdrop-filter: none !important;
            border-bottom: none !important;
            height: 2rem !important;
            min-height: 2rem !important;
            padding: 0 !important;
            margin: 0 !important;
            box-shadow: none !important;
            position: relative !important;
            z-index: 999 !important;
        }}

        header[data-testid="stHeader"] button {{
            color: #ffffff !important;
            background: rgba(0,0,0,0.5) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            font-size: 11px !important;
            padding: 1px 5px !important;
            border-radius: 5px !important;
            transition: all 0.2s !important;
            margin: 0 3px !important;
            backdrop-filter: blur(4px) !important;
            line-height: 1.2 !important;
        }}
        header[data-testid="stHeader"] button:hover {{
            background: rgba(255,255,255,0.18) !important;
            border-color: rgba(255,255,255,0.2) !important;
        }}
        header[data-testid="stHeader"] button svg {{
            width: 12px !important;
            height: 12px !important;
        }}
        header[data-testid="stHeader"] button span {{
            font-size: 14px !important;
        }}

        /* ===== SIDEBAR - WIDER ===== */
        section[data-testid="stSidebar"] {{
            background: rgba(0, 0, 0, 0.7) !important;
            backdrop-filter: blur(6px) !important;
            -webkit-backdrop-filter: blur(6px) !important;
            min-width: 205px !important;
            width: 205px !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            height: 100vh !important;
            position: sticky !important;
            top: 0 !important;
            overflow-y: auto !important;
            border-right: 1px solid rgba(255,255,255,0.05) !important;
            box-shadow: 4px 0 20px rgba(0,0,0,0.4) !important;
        }}

        section[data-testid="stSidebar"][aria-expanded="false"] {{
            margin-left: -205px !important;
        }}

        section[data-testid="stSidebar"] .css-1d391kg {{
            background: transparent !important;
        }}

        footer {{visibility: hidden;}}

        .sidebar-logo {{
            padding: 10px 12px 6px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 6px;
        }}

        .sidebar-logo h2 {{
            color: #ffffff;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: -0.2px;
        }}

        .sidebar-logo span {{
            color: #e87979;
        }}

        .sidebar-logo small {{
            color: rgba(255,255,255,0.4);
            font-size: 9px;
            display: block;
            margin-top: 0px;
            font-weight: 400;
        }}

        .stButton button {{
            width: 100% !important;
            border-radius: 6px !important;
            padding: 4px 8px !important;
            margin: 1px 0 !important;
            font-weight: 500 !important;
            font-size: 10px !important;
            text-align: left !important;
            background: transparent !important;
            color: rgba(255,255,255,0.6) !important;
            border: none !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            gap: 5px !important;
            justify-content: flex-start !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}

        .stButton button:hover {{
            background: rgba(255,255,255,0.08) !important;
            color: #ffffff !important;
        }}

        .stButton button[data-testid="baseButton-secondary"] {{
            background: transparent !important;
            color: rgba(255,255,255,0.6) !important;
        }}

        .stButton button[data-testid="baseButton-primary"] {{
            background: rgba(200, 80, 80, 0.25) !important;
            color: #ffffff !important;
            box-shadow: inset 3px 0 0 #c0392b !important;
        }}

        .sidebar-user {{
            padding: 4px 10px;
            margin: 8px 8px 0 8px;
            border-top: 1px solid rgba(255,255,255,0.06);
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.04);
            border-radius: 6px;
        }}
        .sidebar-user .avatar {{
            font-size: 14px;
        }}
        .sidebar-user .name {{
            color: #ffffff;
            font-size: 10px;
            font-weight: 600;
        }}
        .sidebar-user .email {{
            color: rgba(255,255,255,0.35);
            font-size: 8px;
        }}

        /* ===== MAIN CONTENT ===== */
        .main-content {{
            min-height: 100vh;
            padding: 0;
            background: transparent;
            position: relative;
        }}

        .main-content::before,
        .main-content::after {{
            display: none !important;
        }}

        /* ===== HEADER SECTION - MORE BOTTOM PADDING ===== */
        .header-section {{
            background: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(4px) !important;
            -webkit-backdrop-filter: blur(4px) !important;
            padding: 24px 32px 48px 32px !important;
            border-radius: 0 0 20px 20px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 6px 30px rgba(0,0,0,0.6);
            border-bottom: 1px solid rgba(255,255,255,0.08);
            z-index: 1;
        }}

        .header-title {{
            color: #ffffff;
            font-size: 19px;
            font-weight: 800;
            letter-spacing: -0.2px;
            margin-bottom: 2px;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }}

        .header-title span {{
            color: #e87979;
        }}

        .header-subtitle {{
            color: rgba(255,255,255,0.8);
            font-size: 11px;
            font-weight: 400;
            position: relative;
            z-index: 1;
            margin-bottom: 8px;
        }}

        .header-desc {{
            color: rgba(255,255,255,0.7);
            font-size: 11px;
            max-width: 600px;
            line-height: 1.4;
            position: relative;
            z-index: 1;
        }}

        /* ===== UPLOAD CARD - MORE TOP MARGIN ===== */
        .upload-card {{
            background: rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1.5px dashed rgba(255,255,255,0.15) !important;
            border-radius: 12px;
            padding: 14px 20px !important;
            margin-top: 24px !important;
            position: relative;
            z-index: 1;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .upload-card:hover {{
            border-color: rgba(200, 80, 80, 0.4);
            background: rgba(0,0,0,0.6) !important;
        }}

        .upload-card .upload-icon {{
            font-size: 18px;
            margin-right: 10px;
        }}

        .upload-card p {{
            color: rgba(255,255,255,0.85);
            font-size: 12px;
            font-weight: 500;
            margin: 0;
        }}

        .upload-card small {{
            color: rgba(255,255,255,0.4);
            font-size: 9px;
        }}

        .file-tags {{
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
            margin-top: 6px;
        }}

        .file-tags span {{
            background: rgba(255,255,255,0.08);
            padding: 1px 10px;
            border-radius: 20px;
            color: rgba(255,255,255,0.5);
            font-size: 9px;
        }}

        /* ===== FEATURE GRID ===== */
        .feature-grid-wrapper {{
            padding: 0 24px;
            margin-top: 16px !important;
            position: relative;
            z-index: 2;
        }}

        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }}

        .feature-card {{
            background: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 12px;
            padding: 14px 16px !important;
            box-shadow: 0 3px 16px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.06);
            text-align: center;
        }}

        .feature-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 30px rgba(0,0,0,0.4);
            background: rgba(0,0,0,0.75) !important;
            border-color: rgba(200, 80, 80, 0.2);
        }}

        .feature-card .f-icon {{
            font-size: 20px;
            margin-bottom: 4px;
            display: block;
        }}

        .feature-card h4 {{
            color: #ffffff;
            font-size: 12px;
            font-weight: 700;
            margin: 0 0 2px 0;
        }}

        .feature-card p {{
            color: rgba(255,255,255,0.5);
            font-size: 10px;
            font-weight: 400;
            margin: 0;
        }}

        /* ===== CONTENT BODY (shared) ===== */
        .content-body {{
            padding: 12px 24px 24px 24px !important;
            position: relative;
            z-index: 1;
        }}

        /* ===== METRICS ===== */
        .metrics-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 12px;
        }}

        .metric-card {{
            background: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border-radius: 12px;
            padding: 10px 14px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
        }}

        .metric-card:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            background: rgba(0,0,0,0.7) !important;
        }}

        .metric-card .label {{
            color: rgba(255,255,255,0.5);
            font-size: 10px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 2px;
        }}

        .metric-card .value {{
            color: #ffffff;
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.2px;
        }}

        .metric-card .change {{
            display: inline-flex;
            align-items: center;
            font-size: 10px;
            font-weight: 600;
            padding: 1px 8px;
            border-radius: 20px;
            margin-left: 6px;
        }}

        .metric-card .change.up {{
            color: #10b981;
            background: rgba(16, 185, 129, 0.15);
        }}

        .metric-card .change.down {{
            color: #ef4444;
            background: rgba(239, 68, 68, 0.15);
        }}

        .metric-card .sub {{
            color: rgba(255,255,255,0.4);
            font-size: 10px;
            margin-top: 2px;
        }}

        .metric-card .brand-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #c0392b, #e74c3c);
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 12px;
            border-radius: 20px;
            letter-spacing: 0.3px;
            box-shadow: 0 2px 10px rgba(192, 57, 43, 0.3);
        }}

        .chart-card {{
            background: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border-radius: 12px;
            padding: 10px 14px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 12px;
            transition: all 0.3s ease;
        }}

        .chart-card:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 12px;
        }}

        .stat-card {{
            background: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(4px) !important;
            -webkit-backdrop-filter: blur(4px) !important;
            border-radius: 10px;
            padding: 8px 12px !important;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 1px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            background: rgba(0,0,0,0.7) !important;
        }}

        .stat-card .stat-label {{
            color: rgba(255,255,255,0.5);
            font-size: 9px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        .stat-card .stat-value {{
            color: #ffffff;
            font-size: 16px;
            font-weight: 700;
            margin-top: 1px;
        }}

        /* ===== RESPONSIVE ===== */
        @media (max-width: 992px) {{
            .feature-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .feature-grid-wrapper {{
                padding: 0 16px;
                margin-top: 12px !important;
            }}
            .metrics-row {{
                grid-template-columns: 1fr;
            }}
            .header-section {{
                padding: 20px 20px 36px 20px !important;
            }}
            .content-body {{
                padding: 10px 16px 18px 16px !important;
            }}
            .header-title {{
                font-size: 17px;
            }}
            .stat-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 576px) {{
            .feature-grid {{
                grid-template-columns: 1fr 1fr;
                gap: 8px;
            }}
            .feature-grid-wrapper {{
                padding: 0 10px;
                margin-top: 10px !important;
            }}
            .feature-card {{
                padding: 10px 12px !important;
            }}
            .feature-card .f-icon {{
                font-size: 18px;
            }}
            .feature-card h4 {{
                font-size: 11px;
            }}
            .metric-card .value {{
                font-size: 16px;
            }}
            .header-title {{
                font-size: 15px;
            }}
            .header-section {{
                padding: 16px 14px 32px 14px !important;
            }}
            .content-body {{
                padding: 8px 12px 14px 12px !important;
            }}
            .upload-card {{
                padding: 12px 16px !important;
                margin-top: 20px !important;
            }}
            .stat-grid {{
                grid-template-columns: 1fr 1fr;
            }}
            .stat-card .stat-value {{
                font-size: 14px;
            }}
        }}

        /* Hide default file uploader */
        .stFileUploader > div {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}
        .stFileUploader > div > div {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}
        .stFileUploader label {{
            display: none !important;
        }}
        .stFileUploader > div > div > div {{
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }}
        .stFileUploader > div > div > div > div {{
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }}
        .stFileUploader > div > div > div > div > button {{
            display: none !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            background: rgba(0,0,0,0.5) !important;
            backdrop-filter: blur(4px) !important;
            -webkit-backdrop-filter: blur(4px) !important;
            padding: 3px;
            border-radius: 8px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.06);
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 6px;
            padding: 4px 12px;
            font-weight: 500;
            font-size: 10px;
            color: rgba(255,255,255,0.5);
            border: none !important;
            background: transparent !important;
            transition: all 0.3s ease;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: #ffffff;
            background: rgba(255,255,255,0.05) !important;
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background: rgba(200, 80, 80, 0.2) !important;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            border: none !important;
        }}

        ::-webkit-scrollbar {{
            width: 5px;
            height: 5px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(255,255,255,0.3);
        }}

        .main-content::before,
        .main-content::after {{
            display: none !important;
        }}
    </style>
    """