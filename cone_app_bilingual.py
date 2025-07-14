
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

st.set_page_config(page_title="Cone Turning Calculator | محاسبه مخروط تراشی", layout="centered")

# Language selection
lang = st.sidebar.radio("Language | زبان", ["فارسی", "English"])

labels = {
    "فارسی": {
        "title": "🔧 محاسبه زاویه و ابعاد مخروط تراشی",
        "desc": "برای محاسبه، سه مقدار را وارد کنید، مقدار چهارم محاسبه و مدل سه‌بعدی مخروط نمایش داده می‌شود.",
        "big_d": "قطر بزرگ (D) بر حسب mm",
        "small_d": "قطر کوچک (d) بر حسب mm",
        "length": "طول مخروط (L) بر حسب mm",
        "angle": "زاویه ساپورت (α/2) بر حسب درجه",
        "calculate": "🔍 محاسبه",
        "angle_result": "✅ زاویه ساپورت: ",
        "angle_dms": "🧭 معادل: ",
        "length_result": "✅ طول مخروط: ",
        "big_d_result": "✅ قطر بزرگ: ",
        "small_d_result": "✅ قطر کوچک: ",
        "warning": "⚠️ لطفاً دقیقاً سه مقدار وارد کنید.",
        "error": "❌ خطا در محاسبه:",
        "model_title": "🎥 مدل سه‌بعدی مخروط تراشی"
    },
    "English": {
        "title": "🔧 Cone Turning Angle & Dimension Calculator",
        "desc": "Enter any three values to calculate the fourth and visualize a 3D cone model.",
        "big_d": "Large Diameter (D) in mm",
        "small_d": "Small Diameter (d) in mm",
        "length": "Cone Length (L) in mm",
        "angle": "Support Angle (α/2) in degrees",
        "calculate": "🔍 Calculate",
        "angle_result": "✅ Support angle: ",
        "angle_dms": "🧭 Equivalent: ",
        "length_result": "✅ Cone length: ",
        "big_d_result": "✅ Large diameter: ",
        "small_d_result": "✅ Small diameter: ",
        "warning": "⚠️ Please enter exactly three values.",
        "error": "❌ Calculation error:",
        "model_title": "🎥 3D Cone Model"
    }
}

l = labels[lang]

st.title(l["title"])
st.markdown(l["desc"])

col1, col2 = st.columns(2)

with col1:
    D = st.text_input(l["big_d"], value="80")
    d = st.text_input(l["small_d"], value="30")

with col2:
    L = st.text_input(l["length"], value="100")
    alpha_half_deg = st.text_input(l["angle"])

D = float(D) if D else None
d = float(d) if d else None
L = float(L) if L else None
alpha_half_deg = float(alpha_half_deg) if alpha_half_deg else None

if st.button(l["calculate"]):
    try:
        if alpha_half_deg is None and None not in (D, d, L):
            tan_val = (D - d) / (2 * L)
            alpha_half_rad = math.atan(tan_val)
            alpha_half_deg = math.degrees(alpha_half_rad)
            d_, m_, s_ = deg_to_dms(alpha_half_deg)
            st.success(f"{l['angle_result']}{alpha_half_deg:.2f}°")
            st.info(f"{l['angle_dms']}{d_}° {m_}' {s_:.2f}\"")

        elif L is None and None not in (D, d, alpha_half_deg):
            alpha_half_rad = math.radians(alpha_half_deg)
            L = (D - d) / (2 * math.tan(alpha_half_rad))
            st.success(f"{l['length_result']}{L:.2f} mm")

        elif D is None and None not in (d, L, alpha_half_deg):
            alpha_half_rad = math.radians(alpha_half_deg)
            D = d + 2 * L * math.tan(alpha_half_rad)
            st.success(f"{l['big_d_result']}{D:.2f} mm")

        elif d is None and None not in (D, L, alpha_half_deg):
            alpha_half_rad = math.radians(alpha_half_deg)
            d = D - 2 * L * math.tan(alpha_half_rad)
            st.success(f"{l['small_d_result']}{d:.2f} mm")

        else:
            st.warning(l["warning"])
    except Exception as e:
        st.error(f"{l['error']} {e}")

    st.subheader(l["model_title"])

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
