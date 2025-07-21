import streamlit as st
from datetime import date
from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

from utils import generate_pdf_report

st.set_page_config(page_title="Marine Draft Calculator", layout="centered")

st.title("Marine Draft Calculator")

with st.form("draft_form"):
    st.markdown("## 📋 Ship Data")
    nama_kapal = st.text_input("Ship Name")
    imo = st.text_input("IMO Number")
    surveyor = st.text_input("Surveyor Name")
    tanggal = st.date_input("Survey Date", value=date.today())

    logo = st.file_uploader("Upload Ship Logo (optional)", type=["png", "jpg"])
    tanda_tangan = st.file_uploader("Upload Surveyor Signature (optional)", type=["png", "jpg"])

    st.markdown("## ⚙️ Settings")
    mode6 = st.checkbox("Use 6 Draft Points?")
    use_density = st.checkbox("Apply Density Correction?")
    density = None
    if use_density:
        density = st.number_input("Enter Water Density (default 1.025)", step=0.001, format="%.3f")
    st.markdown("## 📏 Draft Input (meters)")

    
    if mode6:
        fp = st.number_input("Forward (FP)", step=0.01, format="%.2f")
        ap = st.number_input("Aft (AP)", step=0.01, format="%.2f")
        port = st.number_input("Port Midship", step=0.01, format="%.2f")
        stbd = st.number_input("Starboard Midship", step=0.01, format="%.2f")
        fp_port = st.number_input("FP Port", step=0.01, format="%.2f")
        ap_stbd = st.number_input("AP Starboard", step=0.01, format="%.2f")
    else:
        fp = st.number_input("Forward (FP)", step=0.01, format="%.2f")
        ap = st.number_input("Aft (AP)", step=0.01, format="%.2f")
        port = st.number_input("Port Midship", step=0.01, format="%.2f")
        stbd = st.number_input("Starboard Midship", step=0.01, format="%.2f")
        fp_port, ap_stbd = None, None


    submit = st.form_submit_button("📊 Calculate & Generate PDF")

if submit:
    # Validation
    if not all([fp, ap, port, stbd]):
        st.error("All main draft points must be filled.")
        st.stop()
    if mode6 and not all([fp_port, ap_stbd]):
        st.error("All draft points must be filled for 6-point mode.")
        st.stop()

    # Calculation
    draft_points = [fp, ap, port, stbd]
    if mode6:
        draft_points.extend([fp_port, ap_stbd])

    mean_draft = round(sum(draft_points) / len(draft_points), 3)
    trim = round(ap - fp, 3)

    if use_density and density:
        mean_draft_corr = round(mean_draft * (1.025 / density), 3)
        st.info(f"Mean Draft corrected by density: **{mean_draft_corr} m**")
    else:
        mean_draft_corr = mean_draft

    st.success("✅ Calculation Complete")
    st.markdown(f"- **Trim:** `{trim} m`")
    st.markdown(f"- **Mean Draft:** `{mean_draft_corr} m`")

    # Visual Trim
    img = Image.new("RGB", (600, 200), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 100, 550, 150], fill="lightblue", outline="black")
    draw.line([50, 100 + trim * 5, 550, 100 - trim * 5], fill="red", width=3)
    draw.text((260, 160), f"Trim: {trim} m", fill="black")
    st.image(img, caption="Trim Visualization", use_container_width=True)

    # Draft Chart
    st.markdown("### 📈 Draft Chart")
    fig, ax = plt.subplots()
    labels = ['FP', 'AP', 'Port', 'Stbd'] + (['FP-Port', 'AP-Stbd'] if mode6 else [])
    ax.bar(labels, draft_points, color="steelblue")
    ax.set_ylabel("Draft (m)")
    st.pyplot(fig)

    # Create summary and PDF
    summary = {
        "trim": trim,
        "mean_draft": mean_draft,
        "mean_draft_corrected": mean_draft_corr if use_density else None
    }

    pdf_bytes = generate_pdf_report(
        ship_name=nama_kapal,
        imo_number=imo,
        surveyor=surveyor,
        draft_points=draft_points,
        density=density,
        summary=summary,
        date=tanggal.strftime("%Y-%m-%d"),
        logo_path=logo,
        signature_path=tanda_tangan
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name=f"{nama_kapal}_DraftReport.pdf",
        mime="application/pdf"
    )
