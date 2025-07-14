
import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np

def deg_to_dms(angle_deg):
    d = int(angle_deg)
    m_float = (angle_deg - d) * 60
    m = int(m_float)
    s = (m_float - m) * 60
    return d, m, s

st.set_page_config(page_title="محاسبه مخروط تراشی", layout="centered")
st.title("🔧 محاسبه زاویه و ابعاد مخروط تراشی")
st.markdown("برای محاسبه، سه مقدار را وارد کنید، مقدار چهارم محاسبه و مدل سه‌بعدی مخروط نمایش داده می‌شود.")

col1, col2 = st.columns(2)

with col1:
    D = st.text_input("قطر بزرگ (D) بر حسب mm", value="80")
    d = st.text_input("قطر کوچک (d) بر حسب mm", value="30")

with col2:
    L = st.text_input("طول مخروط (L) بر حسب mm", value="100")
    alpha_half_deg = st.text_input("زاویه ساپورت (α/2) بر حسب درجه")

D = float(D) if D else None
d = float(d) if d else None
L = float(L) if L else None
alpha_half_deg = float(alpha_half_deg) if alpha_half_deg else None

if st.button("🔍 محاسبه"):
    try:
        if alpha_half_deg is None and None not in (D, d, L):
            tan_val = (D - d) / (2 * L)
            alpha_half_rad = math.atan(tan_val)
            alpha_half_deg = math.degrees(alpha_half_rad)
            d_, m_, s_ = deg_to_dms(alpha_half_deg)
            st.success(f"✅ زاویه ساپورت: {alpha_half_deg:.2f} درجه")
            st.info(f"🧭 معادل: {d_}° {m_}' {s_:.2f}"")

        elif L is None and None not in (D, d, alpha_half_deg):
            alpha_half_rad = math.radians(alpha_half_deg)
            L = (D - d) / (2 * math.tan(alpha_half_rad))
            st.success(f"✅ طول مخروط: {L:.2f} mm")

        elif D is None and None not in (d, L, alpha_half_deg):
            alpha_half_rad = math.radians(alpha_half_deg)
            D = d + 2 * L * math.tan(alpha_half_rad)
            st.success(f"✅ قطر بزرگ: {D:.2f} mm")

        elif d is None and None not in (D, L, alpha_half_deg):
            alpha_half_rad = math.radians(alpha_half_deg)
            d = D - 2 * L * math.tan(alpha_half_rad)
            st.success(f"✅ قطر کوچک: {d:.2f} mm")

        else:
            st.warning("⚠️ لطفاً دقیقاً سه مقدار وارد کنید.")
    except Exception as e:
        st.error(f"❌ خطا در محاسبه: {e}")

    # مدل سه‌بعدی مخروط قابل چرخش
    st.subheader("🎥 مدل سه‌بعدی مخروط تراشی")

    R1 = D / 2
    R2 = d / 2
    height = L

    theta = np.linspace(0, 2 * np.pi, 50)
    z = np.linspace(0, height, 2)
    theta_grid, z_grid = np.meshgrid(theta, z)
    r_grid = R1 + (R2 - R1) * (z_grid / height)
    x_grid = r_grid * np.cos(theta_grid)
    y_grid = r_grid * np.sin(theta_grid)

    fig = go.Figure(data=[go.Surface(x=x_grid, y=y_grid, z=z_grid, colorscale='YlGnBu')])
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
