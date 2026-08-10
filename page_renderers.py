# page_renderers.py
import streamlit as st
import pandas as pd
import plotly.express as px
from data_utils import get_analysis_data, render_no_data_message

# ---------- HOME ----------
def render_home(df):
    st.markdown("""
    <div class="header-section">
        <div class="header-title">📱 MOBILE <span>SALES ANALYSIS</span></div>
        <div class="header-subtitle">WELCOME TO SALES ANALYSIS</div>
        <div class="header-desc">
            Transform your mobile sales data into meaningful insights with interactive charts and reports.
            Explore sales performance, top-selling brands, revenue trends, and customer preferences—all in one place.
            Upload your sales file below to begin!
        </div>
        <div class="upload-card" style="margin-top:24px;">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <span style="font-size:18px;">📂</span>
                    <div>
                        <p style="color:rgba(255,255,255,0.85);font-size:12px;font-weight:500;margin:0;">Upload your CSV file here</p>
                        <small style="color:rgba(255,255,255,0.4);font-size:9px;">Drag &amp; drop or click to browse</small>
                    </div>
                </div>
                <div class="file-tags" style="margin-top:0;">
                    <span>CSV</span>
                    <span>XLSX</span>
                    <span>200MB max</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid-wrapper">
        <div class="feature-grid">
            <div class="feature-card">
                <span class="f-icon">📊</span>
                <h4>Sales Insights</h4>
                <p>Understand your business</p>
            </div>
            <div class="feature-card">
                <span class="f-icon">🏆</span>
                <h4>Top Brands</h4>
                <p>Find best performers</p>
            </div>
            <div class="feature-card">
                <span class="f-icon">❤️</span>
                <h4>Customer Preferences</h4>
                <p>Know what they love</p>
            </div>
            <div class="feature-card">
                <span class="f-icon">📈</span>
                <h4>Revenue Growth</h4>
                <p>Track &amp; maximize</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV", type=['csv', 'xlsx'], label_visibility="collapsed")
    if uploaded_file is not None:
        from data_utils import load_data
        df_new = load_data(uploaded_file)
        if df_new is not None:
            st.session_state.df = df_new
            st.success("✅ File uploaded successfully! View the Dashboard for insights.")
            st.balloons()
    return df

# ---------- DASHBOARD ----------
def render_dashboard(df):
    if df is None or df.empty:
        render_no_data_message()
        return
    df = get_analysis_data(df)
    st.markdown("""
    <div class="header-section" style="padding:14px 24px 18px 24px !important;">
        <div class="header-title" style="font-size:17px;">📊 <span>Dashboard</span></div>
        <div class="header-subtitle" style="font-size:11px;margin-bottom:0;">Real-time sales performance overview</div>
    </div>
    """, unsafe_allow_html=True)

    total_revenue = df['Revenue'].sum()
    top_brand = df.groupby('Brand')['Revenue'].sum().idxmax() if 'Brand' in df.columns else 'Samsung'
    top_brand_revenue = df.groupby('Brand')['Revenue'].sum().max() if 'Brand' in df.columns else 0

    if 'Month' in df.columns:
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        df['Month_Order'] = df['Month'].apply(lambda x: month_order.index(x) if x in month_order else 0)
        last_two = df.groupby('Month_Order')['Revenue'].sum().sort_index().tail(2)
        growth = ((last_two.iloc[-1] - last_two.iloc[-2]) / last_two.iloc[-2]) * 100 if len(last_two) >= 2 else 18.6
    else:
        growth = 18.6

    st.markdown(f"""
    <div class="content-body" style="padding-top:10px;">
        <div class="metrics-row">
            <div class="metric-card">
                <div class="label">Top Selling Brand</div>
                <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                    <span class="brand-badge">{top_brand.upper()}</span>
                    <span style="color:rgba(255,255,255,0.5);font-size:11px;">₹{top_brand_revenue:,.0f} revenue</span>
                </div>
            </div>
            <div class="metric-card">
                <div class="label">Total Revenue</div>
                <div>
                    <span class="value">₹{total_revenue:,.0f}</span>
                    <span class="change up">↑ {growth:.1f}% vs last month</span>
                </div>
                <div class="sub">Based on {len(df)} sales records</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if 'Region' in df.columns:
        region_data = df.groupby('Region')['Revenue'].sum().reset_index()
        all_regions = ['North', 'South', 'East', 'West', 'Central']
        for r in all_regions:
            if r not in region_data['Region'].values:
                region_data = pd.concat([region_data, pd.DataFrame({'Region': [r], 'Revenue': [0]})], ignore_index=True)
        region_data = region_data[region_data['Region'].isin(all_regions)]

        fig = px.bar(region_data, x='Region', y='Revenue', color='Region',
                     color_discrete_sequence=['#e87979','#c0392b','#a93226','#922b21','#7b241c'],
                     title='Sales by Region', text_auto='.2s')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font=dict(family='Inter', size=10, color='#ffffff'),
                          showlegend=False, height=220,
                          margin=dict(l=12,r=12,t=28,b=12),
                          xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
                          yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)', tickprefix='₹'))
        fig.update_traces(texttemplate='₹%{text}', textposition='outside', marker=dict(cornerradius=4))
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, key="region_chart")
        st.markdown('</div>', unsafe_allow_html=True)

    if 'Brand' in df.columns:
        brand_data = df.groupby('Brand')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False).head(8)
        fig2 = px.bar(brand_data, x='Brand', y='Revenue', color='Brand',
                      color_discrete_sequence=px.colors.qualitative.Set3,
                      title='Revenue by Brand', text_auto='.2s')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           font=dict(family='Inter', size=10, color='#ffffff'),
                           showlegend=False, height=200,
                           margin=dict(l=12,r=12,t=28,b=12),
                           xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
                           yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)', tickprefix='₹'))
        fig2.update_traces(texttemplate='₹%{text}', textposition='outside', marker=dict(cornerradius=4))
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, key="brand_chart")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SALES INSIGHTS ----------
def render_sales_insights(df):
    if df is None or df.empty:
        render_no_data_message()
        return
    df = get_analysis_data(df)
    st.markdown("""
    <div class="header-section" style="padding:14px 24px 18px 24px !important;">
        <div class="header-title" style="font-size:17px;">📈 <span>Sales Insights</span></div>
        <div class="header-subtitle" style="font-size:11px;margin-bottom:0;">Understand your business better</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="content-body" style="padding-top:10px;">', unsafe_allow_html=True)

    total_sales = df['Units_Sold'].sum() if 'Units_Sold' in df.columns else len(df)
    total_rev = df['Revenue'].sum()
    avg_price = df['Price'].mean() if 'Price' in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Units Sold", f"{total_sales:,}")
    c2.metric("Total Revenue", f"₹{total_rev:,.0f}")
    c3.metric("Average Price", f"₹{avg_price:,.0f}")
    c4.metric("Total Records", f"{len(df):,}")

    st.markdown("---")

    if 'Month' in df.columns:
        month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        df['Month_Order'] = df['Month'].apply(lambda x: month_order.index(x) if x in month_order else 0)
        monthly = df.groupby('Month_Order')['Revenue'].sum().reset_index()
        monthly['Month'] = monthly['Month_Order'].apply(lambda x: month_order[x] if x < len(month_order) else 'Unknown')
        monthly = monthly.sort_values('Month_Order')
        fig = px.line(monthly, x='Month', y='Revenue', markers=True, title='Monthly Revenue Trend')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font=dict(family='Inter', size=10, color='#ffffff'),
                          height=220, margin=dict(l=12,r=12,t=28,b=12),
                          xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
                          yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)', tickprefix='₹'))
        fig.update_traces(line=dict(color='#e87979', width=3), marker=dict(size=8, color='#e87979'))
        st.plotly_chart(fig, use_container_width=True, key="monthly_trend")

    if 'Region' in df.columns:
        c1, c2 = st.columns(2)
        with c1:
            region_data = df.groupby('Region')['Revenue'].sum().reset_index()
            fig = px.pie(region_data, values='Revenue', names='Region', title='Revenue by Region',
                         color_discrete_sequence=['#e87979','#c0392b','#a93226','#922b21','#7b241c'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(family='Inter', size=10, color='#ffffff'),
                              height=220, margin=dict(l=12,r=12,t=28,b=12))
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, key="region_pie")
        with c2:
            if 'Customer_Type' in df.columns:
                cust_data = df.groupby('Customer_Type')['Revenue'].sum().reset_index()
                fig = px.pie(cust_data, values='Revenue', names='Customer_Type', title='Revenue by Customer Type',
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family='Inter', size=10, color='#ffffff'),
                                  height=220, margin=dict(l=12,r=12,t=28,b=12))
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, key="customer_pie")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- TOP BRANDS ----------
def render_top_brands(df):
    if df is None or df.empty:
        render_no_data_message()
        return
    df = get_analysis_data(df)
    st.markdown("""
    <div class="header-section" style="padding:14px 24px 18px 24px !important;">
        <div class="header-title" style="font-size:17px;">🏆 <span>Top Brands</span></div>
        <div class="header-subtitle" style="font-size:11px;margin-bottom:0;">Find best performing brands</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="content-body" style="padding-top:10px;">', unsafe_allow_html=True)

    if 'Brand' in df.columns:
        brand_perf = df.groupby('Brand').agg({
            'Revenue': 'sum',
            'Units_Sold': 'sum' if 'Units_Sold' in df.columns else 'count'
        }).reset_index().sort_values('Revenue', ascending=False)

        fig = px.bar(brand_perf.head(10), x='Brand', y='Revenue', color='Brand',
                     title='Top 10 Brands by Revenue', text_auto='.2s',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font=dict(family='Inter', size=10, color='#ffffff'),
                          showlegend=False, height=260,
                          margin=dict(l=12,r=12,t=28,b=12),
                          xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
                          yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)', tickprefix='₹'))
        fig.update_traces(marker=dict(cornerradius=4))
        st.plotly_chart(fig, use_container_width=True, key="top_brands")

        st.markdown("### 📋 Brand Performance Summary")
        st.dataframe(brand_perf.style.format({'Revenue':'₹{:,.0f}','Units_Sold':'{:,.0f}'}),
                     use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- CUSTOMER ANALYSIS ----------
def render_customer_analysis(df):
    if df is None or df.empty:
        render_no_data_message()
        return
    df = get_analysis_data(df)
    st.markdown("""
    <div class="header-section" style="padding:14px 24px 18px 24px !important;">
        <div class="header-title" style="font-size:17px;">👤 <span>Customer Analysis</span></div>
        <div class="header-subtitle" style="font-size:11px;margin-bottom:0;">Know what your customers love</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="content-body" style="padding-top:10px;">', unsafe_allow_html=True)

    if 'Customer_Type' in df.columns:
        c1, c2 = st.columns(2)
        with c1:
            cust_rev = df.groupby('Customer_Type')['Revenue'].sum().reset_index()
            fig = px.bar(cust_rev, x='Customer_Type', y='Revenue', color='Customer_Type',
                         title='Revenue by Customer Type', text_auto='.2s',
                         color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(family='Inter', size=10, color='#ffffff'),
                              showlegend=False, height=220,
                              margin=dict(l=12,r=12,t=28,b=12),
                              xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
                              yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)', tickprefix='₹'))
            st.plotly_chart(fig, use_container_width=True, key="cust_rev")
        with c2:
            if 'Units_Sold' in df.columns:
                cust_units = df.groupby('Customer_Type')['Units_Sold'].sum().reset_index()
                fig = px.bar(cust_units, x='Customer_Type', y='Units_Sold', color='Customer_Type',
                             title='Units Sold by Customer Type', text_auto='.2s',
                             color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  font=dict(family='Inter', size=10, color='#ffffff'),
                                  showlegend=False, height=220,
                                  margin=dict(l=12,r=12,t=28,b=12),
                                  xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
                                  yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'))
                st.plotly_chart(fig, use_container_width=True, key="cust_units")

        if 'Brand' in df.columns:
            brand_cust = df.groupby(['Customer_Type','Brand'])['Revenue'].sum().reset_index()
            top_brands = brand_cust.loc[brand_cust.groupby('Customer_Type')['Revenue'].idxmax()]
            st.markdown("### 🏆 Preferred Brand by Customer Type")
            st.dataframe(top_brands.style.format({'Revenue':'₹{:,.0f}'}),
                         use_container_width=True, hide_index=True)
    else:
        st.info("Customer Type data not available. Please ensure your CSV has a 'Customer_Type' column.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- REVENUE ANALYSIS ----------
def render_revenue_analysis(df):
    if df is None or df.empty:
        render_no_data_message()
        return
    df = get_analysis_data(df)
    st.markdown("""
    <div class="header-section" style="padding:14px 24px 18px 24px !important;">
        <div class="header-title" style="font-size:17px;">📉 <span>Revenue Analysis</span></div>
        <div class="header-subtitle" style="font-size:11px;margin-bottom:0;">Track growth and maximize profits</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="content-body" style="padding-top:10px;">', unsafe_allow_html=True)

    total_rev = df['Revenue'].sum()
    avg_rev = df['Revenue'].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"₹{total_rev:,.0f}")
    c2.metric("Average Revenue per Sale", f"₹{avg_rev:,.0f}")
    if 'Month' in df.columns:
        month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        df['Month_Order'] = df['Month'].apply(lambda x: month_order.index(x) if x in month_order else 0)
        monthly = df.groupby('Month_Order')['Revenue'].sum().sort_index()
        if len(monthly) >= 2:
            growth = ((monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2]) * 100
            c3.metric("Growth (MoM)", f"{growth:.1f}%", delta=f"{growth:.1f}%")
        else:
            c3.metric("Growth (MoM)", "N/A")
    else:
        c3.metric("Growth (MoM)", "N/A")
    c4.metric("Total Records", f"{len(df):,}")

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        if 'Brand' in df.columns:
            brand_rev = df.groupby('Brand')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False).head(8)
            fig = px.pie(brand_rev, values='Revenue', names='Brand', title='Revenue Distribution by Brand',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(family='Inter', size=10, color='#ffffff'),
                              height=260, margin=dict(l=12,r=12,t=28,b=12))
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, key="rev_dist_brand")
    with c2:
        if 'Region' in df.columns:
            region_rev = df.groupby('Region')['Revenue'].sum().reset_index()
            fig = px.pie(region_rev, values='Revenue', names='Region', title='Revenue Distribution by Region',
                         color_discrete_sequence=['#e87979','#c0392b','#a93226','#922b21','#7b241c'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(family='Inter', size=10, color='#ffffff'),
                              height=260, margin=dict(l=12,r=12,t=28,b=12))
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, key="rev_dist_region")

    if 'Units_Sold' in df.columns and 'Price' in df.columns:
        fig = px.scatter(df, x='Units_Sold', y='Revenue', color='Brand' if 'Brand' in df.columns else None,
                         size='Price', title='Revenue vs Units Sold (bubble size = Price)',
                         labels={'Units_Sold':'Units Sold','Revenue':'Revenue (₹)'},
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font=dict(family='Inter', size=10, color='#ffffff'),
                          height=260, margin=dict(l=12,r=12,t=28,b=12),
                          xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
                          yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)', tickprefix='₹'))
        st.plotly_chart(fig, use_container_width=True, key="rev_scatter")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- REPORTS ----------
def render_reports(df):
    if df is None or df.empty:
        render_no_data_message()
        return
    df = get_analysis_data(df)
    st.markdown("""
    <div class="header-section" style="padding:14px 24px 18px 24px !important;">
        <div class="header-title" style="font-size:17px;">📄 <span>Reports</span></div>
        <div class="header-subtitle" style="font-size:11px;margin-bottom:0;">Detailed sales reports and summaries</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="content-body" style="padding-top:10px;">', unsafe_allow_html=True)

    total_rev = df['Revenue'].sum()
    total_units = df['Units_Sold'].sum() if 'Units_Sold' in df.columns else len(df)
    avg_price = df['Price'].mean() if 'Price' in df.columns else 0

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-label">Total Revenue</div><div class="stat-value">₹{total_rev:,.0f}</div></div>
        <div class="stat-card"><div class="stat-label">Total Units Sold</div><div class="stat-value">{total_units:,.0f}</div></div>
        <div class="stat-card"><div class="stat-label">Average Price</div><div class="stat-value">₹{avg_price:,.0f}</div></div>
        <div class="stat-card"><div class="stat-label">Total Transactions</div><div class="stat-value">{len(df):,}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Full Data View")
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Report (CSV)", data=csv,
                       file_name="sales_report.csv", mime="text/csv",
                       use_container_width=True, type="primary")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- UPLOAD DATA ----------
def render_upload_data(df):
    st.markdown("""
    <div class="header-section" style="padding:14px 24px 18px 24px !important;">
        <div class="header-title" style="font-size:17px;">📤 <span>Upload Data</span></div>
        <div class="header-subtitle" style="font-size:11px;margin-bottom:0;">Upload your sales data CSV file</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="content-body" style="padding-top:10px;">', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(0,0,0,0.6);backdrop-filter:blur(8px);border-radius:12px;padding:20px;border:2px dashed rgba(255,255,255,0.08);text-align:center;margin-bottom:16px;transition:all 0.3s ease;">
        <div style="font-size:36px;margin-bottom:10px;">📂</div>
        <h3 style="color:#ffffff;font-weight:600;margin-bottom:4px;font-size:16px;">Upload Your CSV File</h3>
        <p style="color:rgba(255,255,255,0.5);font-size:12px;margin-bottom:12px;">Drag and drop your file here or click to browse</p>
        <div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap;">
            <span style="background:rgba(255,255,255,0.05);padding:2px 12px;border-radius:20px;color:rgba(255,255,255,0.4);font-size:10px;">CSV</span>
            <span style="background:rgba(255,255,255,0.05);padding:2px 12px;border-radius:20px;color:rgba(255,255,255,0.4);font-size:10px;">Max 200MB</span>
            <span style="background:rgba(255,255,255,0.05);padding:2px 12px;border-radius:20px;color:rgba(255,255,255,0.4);font-size:10px;">UTF-8</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'], label_visibility="collapsed")
    if uploaded_file is not None:
        from data_utils import load_data
        new_df = load_data(uploaded_file)
        if new_df is not None:
            st.session_state.df = new_df
            st.success(f"✅ File '{uploaded_file.name}' uploaded! {len(new_df)} records loaded.")
            st.dataframe(new_df.head(10), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:rgba(0,0,0,0.5);backdrop-filter:blur(6px);border-radius:12px;padding:16px 20px;margin-top:8px;">
        <h4 style="color:#ffffff;font-weight:600;margin-bottom:6px;font-size:14px;">📄 Sample CSV Format</h4>
        <p style="color:rgba(255,255,255,0.6);font-size:11px;margin-bottom:10px;">Your CSV should include these columns (names can vary but are recommended):</p>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 2])
    with cols[0]:
        st.markdown("**Column**")
        st.write("Brand")
        st.write("Revenue")
        st.write("Region")
        st.write("Units_Sold")
        st.write("Month")
        st.write("Price *(optional)*")
    with cols[1]:
        st.markdown("**Description**")
        st.write("Mobile brand name (e.g., Apple, Samsung)")
        st.write("Sales revenue amount (numeric)")
        st.write("Sales region (e.g., North, South)")
        st.write("Number of units sold (integer)")
        st.write("Month of sale (e.g., Jan, Feb)")
        st.write("Price per unit (optional)")

    sample_df = pd.DataFrame({
        "Brand": ["Apple", "Samsung", "Xiaomi"],
        "Revenue": [45000, 38000, 28000],
        "Region": ["North", "South", "East"],
        "Units_Sold": [45, 38, 28],
        "Month": ["Jan", "Feb", "Mar"],
        "Price": [1000, 1000, 1000]
    })
    csv_sample = sample_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Sample CSV",
        data=csv_sample,
        file_name="sample_sales_data.csv",
        mime="text/csv",
        use_container_width=False,
        type="primary"
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)