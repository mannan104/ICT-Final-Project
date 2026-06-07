import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="ICT for Structural Safety",
    page_icon="🏗️",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown("""
<style>

.stApp{
background: linear-gradient(
135deg,
#0f2027,
#203a43,
#2c5364
);
}

[data-testid="stSidebar"]{
background: linear-gradient(
180deg,
#141e30,
#243b55
);
}

div[data-testid="metric-container"]{
background: rgba(255,255,255,0.08);
border-radius:15px;
padding:15px;
border:1px solid rgba(255,255,255,0.15);
box-shadow:0px 0px 15px rgba(0,255,255,0.15);
}

h1,h2,h3,h4{
color:white;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown("""
<div style="
background:linear-gradient(90deg,#00c6ff,#0072ff);
padding:25px;
border-radius:20px;
text-align:center;
margin-bottom:20px;
box-shadow:0px 0px 20px rgba(0,114,255,0.5);
">

<h1 style="color:white;">
🏗 ICT FOR STRUCTURAL SAFETY
</h1>

<h3 style="color:white;">
LIVE BEAM DEFLECTION VISUALIZER
</h3>

<p style="color:white;font-size:18px;">
Real-Time Structural Monitoring & Analysis Dashboard
</p>

</div>
""", unsafe_allow_html=True)

# ======================================================
# TEAM SECTION
# ======================================================
st.markdown("""
<div style="
background:linear-gradient(135deg,#11998e,#38ef7d);
padding:20px;
border-radius:20px;
margin-bottom:20px;
color:white;
">

<h2>👨‍💻 Project Team</h2>

<table style="width:100%; font-size:18px;">
<tr>
<th align="left">Name</th>
<th align="left">Registration No.</th>
</tr>

<tr>
<td>Abdul Mannan</td>
<td>25-ME-55</td>
</tr>

<tr>
<td>Muhammad Bin Akarma</td>
<td>25-ME-59</td>
</tr>

<tr>
<td>Muneeb Azhar</td>
<td>25-ME-03</td>
</tr>

<tr>
<td>Ahmed Ali</td>
<td>25-ME-115</td>
</tr>

<tr>
<td>Hammad Fida</td>
<td>25-ME-27</td>
</tr>

</table>

</div>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("⚙ Beam Parameters")

materials = {
    "Steel": 200e9,
    "Aluminum": 69e9,
    "Concrete": 30e9,
    "Wood": 12e9
}

material = st.sidebar.selectbox(
    "Material",
    list(materials.keys())
)

E = materials[material]

L = st.sidebar.slider(
    "Beam Length (m)",
    1.0,
    20.0,
    10.0
)

P = st.sidebar.slider(
    "Point Load (N)",
    100,
    10000,
    3000
)

I = st.sidebar.slider(
    "Moment of Inertia (m⁴)",
    0.000001,
    0.01,
    0.0005
)

# ======================================================
# CALCULATIONS
# ======================================================
delta_max = (P * L**3) / (48 * E * I)

allowable = L / 360

# ======================================================
# DASHBOARD
# ======================================================
st.subheader("📊 Engineering Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("📏 Length", f"{L:.2f} m")
c2.metric("⚖ Load", f"{P:.0f} N")
c3.metric("🏗 Material", material)
c4.metric("📉 Deflection", f"{delta_max:.6f} m")

# ======================================================
# SAFETY STATUS
# ======================================================
st.subheader("🛡 Structural Safety Assessment")

if delta_max <= allowable:

    st.markdown("""
    <div style="
    background:#00c853;
    color:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:24px;
    ">
    ✅ STRUCTURE SAFE
    </div>
    """, unsafe_allow_html=True)

    safety_status = "SAFE"

else:

    st.markdown("""
    <div style="
    background:#d50000;
    color:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:24px;
    ">
    ❌ STRUCTURE UNSAFE
    </div>
    """, unsafe_allow_html=True)

    safety_status = "UNSAFE"

# ======================================================
# GAUGE CHART
# ======================================================
st.subheader("🎯 Deflection Gauge")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=delta_max * 1000,
    title={"text":"Deflection (mm)"},
    gauge={
        "axis":{"range":[0,max(allowable*1000,1)]}
    }
))

st.plotly_chart(gauge, use_container_width=True)

# ======================================================
# BEAM DIAGRAM
# ======================================================
st.subheader("🏗 Beam Model")

fig1, ax1 = plt.subplots(figsize=(10,2))

ax1.plot([0,L],[0,0], linewidth=8)

ax1.scatter([0,L],[0,0], s=250)

ax1.arrow(
    L/2,
    0.5,
    0,
    -0.4,
    head_width=0.4,
    head_length=0.1
)

ax1.text(
    L/2,
    0.65,
    f"{P} N",
    ha="center",
    fontsize=12
)

ax1.set_title("Simply Supported Beam with Central Load")
ax1.axis("off")

st.pyplot(fig1)

# ======================================================
# DEFLECTION GRAPH
# ======================================================
st.subheader("📈 Live Deflection Visualization")

x = np.linspace(0,L,500)

y = -delta_max*np.sin(np.pi*x/L)

fig2, ax2 = plt.subplots(figsize=(10,4))

ax2.plot(
    x,
    y,
    linewidth=4
)

ax2.fill_between(
    x,
    y,
    0,
    alpha=0.3
)

ax2.grid(True)

ax2.set_xlabel("Beam Length (m)")
ax2.set_ylabel("Deflection (m)")
ax2.set_title("Beam Deflection Curve")

st.pyplot(fig2)

# ======================================================
# RESULTS TABLE
# ======================================================
st.subheader("📋 Analysis Results")

df = pd.DataFrame({
    "Parameter":[
        "Material",
        "Length (m)",
        "Load (N)",
        "Moment of Inertia (m⁴)",
        "Maximum Deflection (m)",
        "Allowable Deflection (m)",
        "Safety Status"
    ],
    "Value":[
        material,
        L,
        P,
        I,
        delta_max,
        allowable,
        safety_status
    ]
})

st.dataframe(df, use_container_width=True)

# ======================================================
# DOWNLOAD REPORT
# ======================================================
csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Report",
    csv,
    file_name="beam_deflection_report.csv",
    mime="text/csv"
)

# ======================================================
# FORMULA SECTION
# ======================================================
st.subheader("📚 Engineering Formula")

:contentReference[oaicite:0]{index=0}

st.markdown("""
Where:

- **P** = Applied Load (N)
- **L** = Beam Length (m)
- **E** = Young's Modulus (Pa)
- **I** = Moment of Inertia (m⁴)
- **δ** = Maximum Deflection (m)

This application demonstrates how ICT tools can be used to improve structural safety by visualizing beam behavior under loading conditions.
""")

# ======================================================
# PROJECT FEATURES
# ======================================================
st.subheader("🚀 Smart Features")

st.markdown("""
✅ Real-Time Beam Deflection Analysis

✅ Material Property Database

✅ Structural Safety Monitoring

✅ Interactive Load Visualization

✅ Engineering Calculations

✅ Downloadable Analysis Report

✅ Modern Dashboard Interface

✅ ICT-Based Structural Assessment

✅ Live Deflection Curve

✅ Safety Limit Verification
""")

# ======================================================
# ABOUT PROJECT
# ======================================================
with st.expander("📖 About This Project"):
    st.write("""
This project applies Information and Communication Technology (ICT)
to Structural Safety by providing a real-time beam deflection
visualization system.

Users can change beam length, load, and material properties to
observe how structural behavior changes instantly.
""")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")

st.markdown("""
<div style="text-align:center;color:white;">

<h3>ICT for Structural Safety: Live Beam Deflection Visualizer</h3>

<p>
Abdul Mannan • Muhammad Bin Akarma • Muneeb Azhar • Ahmed Ali • Hammad Fida
</p>

<p>Department of Mechanical Engineering</p>

</div>
""", unsafe_allow_html=True)
