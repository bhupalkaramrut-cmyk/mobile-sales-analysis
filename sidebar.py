# sidebar.py
import streamlit as st

def render_sidebar():
    """Render the sidebar with navigation and user info."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>📱 <span>Mobile</span>Sales</h2>
            <small>Analytics Dashboard</small>
        </div>
        """, unsafe_allow_html=True)

        nav_items = [
            ("🏠", "Home"),
            ("📊", "Dashboard"),
            ("📈", "Sales Insights"),
            ("🏆", "Top Brands"),
            ("👤", "Customer Analysis"),
            ("📉", "Revenue Analysis"),
            ("📄", "Reports"),
            ("📤", "Upload Data"),
        ]

        for icon, label in nav_items:
            is_active = st.session_state.page == label
            if st.button(
                f"{icon} {label}",
                key=f"nav_{label.replace(' ', '_')}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.page = label
                st.rerun()

        st.markdown("""
        <div class="sidebar-user">
            <span class="avatar">👤</span>
            <div>
                <div class="name">Admin User</div>
                <div class="email">amrut@gmail.com</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.page