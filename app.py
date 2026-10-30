import streamlit as st
import requests
import pandas as pd
from html import escape

st.set_page_config(
    page_title="Liver Disease Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --teal: #087f86;
  --teal-dark: #075e66;
  --ink: #18364d;
  --muted: #647f98;
  --line: #dce8ef;
  --pale: #eef8fb;
}
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #f7fbfd 0%, #edf7fa 100%); color: var(--ink); }
.block-container { padding-top: 1.1rem; padding-bottom: 1rem; max-width: 1600px; }
[data-testid="stHeader"] { background: rgba(255,255,255,.82); }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #eaf5f8 0%, #dceff3 100%);
  border-right: 1px solid #d3e7ed;
}
[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #24445d; }
div[data-testid="stVerticalBlock"] { gap: .75rem; }
div[data-testid="stForm"] { border: 0; padding: 0; }
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
  border-radius: 9px !important;
}
.stNumberInput, .stSelectbox { margin-bottom: .15rem; }
.stButton > button, .stFormSubmitButton > button {
  border-radius: 10px; border: 0; min-height: 3rem; font-weight: 700;
  background: linear-gradient(90deg, #07858b, #08777f); color: white;
  box-shadow: 0 5px 12px rgba(8,127,134,.16); transition: transform .15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  background: linear-gradient(90deg, #066e75, #075e66); color: white; transform: translateY(-1px);
}
div[data-testid="stAlert"] { border-radius: 10px; }
hr { border-color: #e2edf2; }
.brand-header {
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
  padding: .15rem .25rem 1rem .25rem; margin-bottom: .5rem;
  border-bottom: 1px solid #e0ebf0;
}
.brand-left { display:flex; align-items:center; gap: .85rem; }
.brand-icon {
  display:flex; align-items:center; justify-content:center; width:52px; height:52px;
  background:#e0f4f3; border-radius:15px; color:#087f86; font-size:28px;
}
.brand-title { font-size:1.55rem; font-weight:800; color:#104c5a; line-height:1.2; }
.brand-subtitle { color:#6b879f; font-size:.88rem; margin-top:.22rem; }
.top-status { color:#45617a; font-size:.85rem; font-weight:600; }
.hero {
  position:relative; overflow:hidden; border:1px solid #d2e8f0; border-radius:15px;
  padding:1.55rem 1.75rem; min-height:175px; margin-bottom:1rem;
  background:
    radial-gradient(circle at 80% 15%, rgba(43,177,205,.34), transparent 30%),
    linear-gradient(105deg, #e7f8fc 0%, #d4f0f8 44%, #08719b 100%);
  box-shadow:0 4px 14px rgba(36,91,119,.06);
}
.hero:after {
  content:""; position:absolute; width:300px; height:300px; right:5%; top:-65px; border-radius:50%;
  border:1px solid rgba(255,255,255,.24); box-shadow:0 0 0 25px rgba(255,255,255,.05), 0 0 0 55px rgba(255,255,255,.04);
}
.hero-copy { position:relative; z-index:2; max-width:55%; }
.hero h2 { font-size:2rem; line-height:1.12; margin:0 0 .65rem 0; color:#12475a; font-weight:800; }
.hero p { color:#4c7290; line-height:1.55; margin:0; font-size:.98rem; max-width:410px; }
.hero-tags { display:flex; gap:1.2rem; margin-top:1.05rem; color:#28677b; font-size:.83rem; font-weight:600; flex-wrap:wrap; }
.hero-art { position:absolute; right:5%; top:12%; font-size:6.2rem; opacity:.95; filter: drop-shadow(0 5px 10px rgba(0,38,70,.15)); }
.panel {
  background:rgba(255,255,255,.94); border:1px solid #dceaf1; border-radius:14px;
  padding:1.15rem 1.2rem; box-shadow:0 4px 13px rgba(42,93,122,.055); height:100%;
}
.panel-heading { display:flex; align-items:center; gap:.7rem; margin-bottom:.25rem; }
.panel-icon {
  width:42px; height:42px; flex-shrink:0; border-radius:50%; background:#07858b;
  display:flex; align-items:center; justify-content:center; color:white; font-size:1.25rem;
}
.panel-title { font-size:1.08rem; font-weight:800; color:#183d55; }
.panel-subtitle { font-size:.78rem; color:#6c879f; margin-top:.1rem; }
.result-empty {
  padding:1.5rem 1rem; border:1px dashed #c8dfe8; border-radius:12px; text-align:center;
  background:#f7fbfd; color:#68849b; margin-top:1rem;
}
.result-box {
  padding:1.15rem; border:1px solid #a7e7d9; border-radius:12px;
  background:linear-gradient(120deg,#e8fbf5,#f4fffc); margin-top:1rem;
}
.result-box.warning { background:linear-gradient(120deg,#fff0f0,#fff9f9); border-color:#ffd2d2; }
.result-title { font-size:1.15rem; font-weight:800; color:#087b55; margin-bottom:.35rem; }
.result-title.warning { color:#bd3d45; }
.result-desc { font-size:.86rem; line-height:1.5; color:#506d82; }
.prob-label { display:flex; justify-content:space-between; font-size:.82rem; font-weight:700; margin-bottom:.5rem; }
.prob-track { height:10px; background:#e7edf2; border-radius:20px; overflow:hidden; }
.prob-fill { height:100%; border-radius:20px; background:linear-gradient(90deg,#16a36d,#54c69a); }
.summary {
  border:1px solid #e1ebf1; border-radius:11px; overflow:hidden; margin-top:1rem;
}
.summary-head { background:#f7fafc; padding:.8rem .95rem; font-size:.86rem; font-weight:700; }
.summary-row { display:flex; justify-content:space-between; padding:.55rem .95rem; border-top:1px solid #edf2f5; font-size:.8rem; gap:1rem; }
.summary-row span:first-child { color:#6a849b; }
.summary-row span:last-child { color:#244c68; font-weight:600; text-align:right; }
.note {
  background:#fff7f7; border:1px solid #ffdddd; border-radius:11px; padding:.9rem;
  color:#7b6268; font-size:.78rem; line-height:1.55; margin-top:1rem;
}
.note strong { color:#bd3d45; }
.trust-note { background:#f2f9fb; border:1px solid #d9ebf1; border-radius:9px; padding:.7rem .8rem; color:#5d7b92; font-size:.76rem; margin-top:.8rem; }
.footer { text-align:center; color:#7890a4; font-size:.75rem; padding:1rem .2rem .2rem; }
.side-tagline { color:#5d8998; font-size:.82rem; line-height:1.7; font-style:italic; margin-top:2rem; }
@media (max-width: 900px) {
  .hero-copy { max-width:75%; }
  .hero-art { right:1%; font-size:4rem; }
  .hero h2 { font-size:1.55rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:.25rem 0 1.2rem;">
      <div style="font-size:2rem;">🩺</div>
      <div><div style="font-weight:800;color:#105363;font-size:1.1rem;">LiverCare AI</div>
      <div style="font-size:.73rem;color:#6d899e;">Prediction Dashboard</div></div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["⌂  Home", "♧  Predict", "ⓘ  About", "▤  Dataset Info", "⚙  Model Details", "✉  Contact"],
        label_visibility="collapsed",
    )
    st.markdown("""
    <div class="side-tagline">Better Data.<br>Better Decisions.<br>Healthier Tomorrow.</div>
    <div style="font-size:3.5rem;opacity:.22;margin-top:1rem;">◒</div>
    """, unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="brand-header">
  <div class="brand-left">
    <div class="brand-icon">◒</div>
    <div>
      <div class="brand-title">Liver Disease Prediction</div>
      <div class="brand-subtitle">Machine Learning Based Prediction System</div>
    </div>
  </div>
  <div class="top-status">◉ &nbsp; Health Analytics &nbsp;⌄</div>
</div>
""", unsafe_allow_html=True)

if page.startswith("ⓘ") or page.startswith("▤") or page.startswith("⚙") or page.startswith("✉"):
    if page.startswith("ⓘ"):
        st.title("About this project")
        st.write("This academic project demonstrates how a trained machine-learning pipeline can analyze selected patient measurements and return a model prediction.")
        st.info("This tool is for educational demonstration only and is not a medical diagnosis.")
    elif page.startswith("▤"):
        st.title("Dataset Information")
        st.write("The project is designed for the Indian Liver Patient Dataset (ILPD). Confirm the dataset source, row count, feature definitions, and class mapping from your notebook before presenting these details.")
        st.markdown("**Expected input features:** Age, Gender, Total Bilirubin, Direct Bilirubin, Alkaline Phosphotase, Alamine Aminotransferase, Aspartate Aminotransferase, Total Proteins, Albumin, Albumin and Globulin Ratio.")
    elif page.startswith("⚙"):
        st.title("Model Details")
        st.write("The interface is prepared to send the patient measurements to a FastAPI backend. Model name, evaluation scores, and training details should be filled using your actual notebook results.")
        st.warning("Do not claim accuracy or clinical reliability without verified evaluation results.")
    else:
        st.title("Contact")
        st.write("Student ML mini-project — Liver Disease Prediction")
        st.caption("Add your preferred project contact details here.")
    st.stop()

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <div class="hero-copy">
    <h2>Early Detection<br>Saves Lives</h2>
    <p>Our machine learning model analyzes selected health parameters to estimate the model's liver-disease class prediction.</p>
    <div class="hero-tags"><span>ϟ &nbsp; Fast</span><span>⬡ &nbsp; Data-driven</span><span>✦ &nbsp; Informative</span></div>
  </div>
  <div class="hero-art">🫀</div>
</div>
""", unsafe_allow_html=True)

if page.startswith("♧"):
    st.markdown("### Patient Assessment")
    st.caption("Enter the available measurements, then submit them for a model prediction.")
else:
    st.markdown("")

# ---------- Main layout ----------
left, right = st.columns([1.16, 0.94], gap="medium")

with left:
    st.markdown("""
    <div class="panel">
      <div class="panel-heading"><div class="panel-icon">♙</div>
      <div><div class="panel-title">Patient Details</div>
      <div class="panel-subtitle">Enter the patient's information and lab test results</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("patient_form"):
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=35, step=1)
            total_bilirubin = st.number_input("Total Bilirubin (mg/dL)", min_value=0.0, value=0.8, step=0.1, format="%.2f")
            alkaline_phosphotase = st.number_input("Alkaline Phosphotase (U/L)", min_value=0.0, value=200.0, step=1.0, format="%.1f")
            ast = st.number_input("Aspartate Aminotransferase (AST) (U/L)", min_value=0.0, value=25.0, step=1.0, format="%.1f")
            albumin = st.number_input("Albumin (g/dL)", min_value=0.0, value=3.5, step=0.1, format="%.2f")
        with c2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            direct_bilirubin = st.number_input("Direct Bilirubin (mg/dL)", min_value=0.0, value=0.2, step=0.1, format="%.2f")
            alt = st.number_input("Alamine Aminotransferase (ALT) (U/L)", min_value=0.0, value=25.0, step=1.0, format="%.1f")
            total_proteins = st.number_input("Total Proteins (g/dL)", min_value=0.0, value=7.0, step=0.1, format="%.2f")
            ag_ratio = st.number_input("Albumin and Globulin Ratio", min_value=0.0, value=1.0, step=0.1, format="%.2f")

        submitted = st.form_submit_button("🧠  Predict Liver Disease", use_container_width=True)

    st.markdown("""
    <div class="trust-note">ⓘ &nbsp; Patient values are sent to the configured prediction service only when you submit the form.</div>
    """, unsafe_allow_html=True)

    patient = {
        "Age": age,
        "Gender": gender,
        "Total_Bilirubin": total_bilirubin,
        "Direct_Bilirubin": direct_bilirubin,
        "Alkaline_Phosphotase": alkaline_phosphotase,
        "Alamine_Aminotransferase": alt,
        "Aspartate_Aminotransferase": ast,
        "Total_Protiens": total_proteins,
        "Albumin": albumin,
        "Albumin_and_Globulin_Ratio": ag_ratio,
    }

with right:
    st.markdown("""
    <div class="panel">
      <div class="panel-heading"><div class="panel-icon">⌁</div>
      <div><div class="panel-title">Prediction Result</div>
      <div class="panel-subtitle">The model result will appear here after submission</div></div></div>
    """, unsafe_allow_html=True)

    result = st.session_state.get("prediction_result")
    if submitted:
        try:
            # Frontend -> FastAPI backend. Backend will be added in the next step.
            response = requests.post("http://127.0.0.1:8000/predict", json=patient, timeout=8)
            response.raise_for_status()
            result = response.json()
            st.session_state["prediction_result"] = result
        except requests.exceptions.ConnectionError:
            st.session_state.pop("prediction_result", None)
            st.warning("The frontend is ready, but the backend is not running yet. We'll connect it in the next step.")
            result = None
        except requests.exceptions.Timeout:
            st.error("The prediction service took too long to respond. Please try again.")
            result = None
        except requests.exceptions.RequestException as exc:
            st.error(f"The prediction request failed: {exc}")
            result = None

    if result:
        prediction = result.get("prediction", result.get("class", None))
        probability = result.get("probability", result.get("liver_probability", None))
        # Contract: prediction 1 = liver-patient class; 0 = non-liver-patient class.
        is_liver = str(prediction).strip().lower() in {"1", "liver", "liver disease", "positive", "true"}
        label = "Liver Disease Class" if is_liver else "Non-Liver Disease Class"
        title_class = "warning" if is_liver else ""
        desc = ("The model predicted the liver-disease class for the submitted measurements."
                if is_liver else "The model predicted the non-liver-disease class for the submitted measurements.")
        st.markdown(f"""
        <div class="result-box {'warning' if is_liver else ''}">
          <div class="result-title {'warning' if is_liver else ''}">{'⚠️' if is_liver else '✓'} &nbsp; {escape(label)}</div>
          <div class="result-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if probability is not None:
            try:
                prob = float(probability)
                # Accept either 0-1 or 0-100 probability values.
                if prob <= 1:
                    prob *= 100
                prob = max(0.0, min(100.0, prob))
                st.markdown(f"""
                <div style="margin-top:1rem;border:1px solid #e0ebf1;border-radius:11px;padding:1rem;background:#fbfdfe;">
                  <div class="prob-label"><span>Model-estimated liver-class probability</span><span>{prob:.1f}%</span></div>
                  <div class="prob-track"><div class="prob-fill" style="width:{prob:.1f}%"></div></div>
                  <div style="font-size:.72rem;color:#7890a4;margin-top:.45rem;">This is a model estimate, not a clinical risk score.</div>
                </div>
                """, unsafe_allow_html=True)
            except (ValueError, TypeError):
                pass
    else:
        st.markdown("""
        <div class="result-empty">
          <div style="font-size:2rem;margin-bottom:.5rem;">🩺</div>
          <div style="font-weight:700;color:#355a72;margin-bottom:.35rem;">Ready for assessment</div>
          <div style="font-size:.82rem;line-height:1.5;">Complete the patient form and click <b>Predict Liver Disease</b>. The actual model output will appear here.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="summary"><div class="summary-head">▤ &nbsp; Input Summary</div>', unsafe_allow_html=True)
    summary_rows = [
        ("Age", f"{age} years"), ("Gender", gender),
        ("Total Bilirubin", f"{total_bilirubin:g}"), ("Direct Bilirubin", f"{direct_bilirubin:g}"),
        ("Alkaline Phosphotase", f"{alkaline_phosphotase:g}"), ("ALT", f"{alt:g}"),
        ("AST", f"{ast:g}"), ("Total Proteins", f"{total_proteins:g}"),
        ("Albumin", f"{albumin:g}"), ("A/G Ratio", f"{ag_ratio:g}")
    ]
    for label, value in summary_rows:
        st.markdown(f'<div class="summary-row"><span>{escape(label)}</span><span>{escape(value)}</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="note"><strong>⚠ &nbsp; Important Note</strong><br>
    This prediction is for educational purposes only and is not a substitute for professional medical advice.
    Please consult a qualified healthcare professional for diagnosis and treatment.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">Liver Disease Prediction &nbsp;•&nbsp; Academic ML Project &nbsp;•&nbsp; Streamlit Frontend + FastAPI Backend</div>
""", unsafe_allow_html=True)
