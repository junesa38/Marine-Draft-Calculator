import streamlit as st
from calculation import calculate_draft_summary
from utils import generate_pdf_report, load_ship_image
from datetime import datetime
from PIL import Image, ImageDraw
from io import BytesIO

st.set_page_config(page_title="Marine Draft Calculator", layout="wide")
st.title("Marine Draft Calculator")

st.markdown("### Vessel Information")
col1, col2, col3 = st.columns(3)
with col1:
    ship_name = st.text_input("Ship Name")
with col2:
    imo_number = st.text_input("IMO Number")
with col3:
    surveyor = st.text_input("Surveyor Name")

st.markdown("### Draft Measurements")
num_points = st.selectbox("Number of Draft Points", [4, 6])

draft_points = []
for i in range(num_points):
    draft = st.text_input(f"Draft Point {i+1} (m)", value="", key=f"draft_{i}_{num_points}")
    draft_points.append(draft)

st.markdown("### Environmental Data (Optional)")
density = st.text_input("Water Density (e.g. 1.025)", value="")

# Show ship diagram
image = load_ship_image()
if image:
    st.image(image, caption="Ship Draft Reference", use_container_width=True)
else:
    st.warning("Ship diagram not found or failed to load.")

# Trim Visualization Function
def draw_trim_visual(fwd, aft):
    width = 600
    height = 200
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    center_y = height // 2
    length = width - 100

    delta = (aft - fwd) * 10
    bow_y = center_y - delta
    stern_y = center_y + delta

    draw.line([(50, bow_y), (50 + length, stern_y)], fill="blue", width=4)
    draw.text((50, bow_y - 20), "Bow", fill="black")
    draw.text((50 + length - 30, stern_y + 5), "Stern", fill="black")

    return img

def get_trim_image_buffer(fwd, aft):
    img = draw_trim_visual(fwd, aft)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

if st.button("Generate PDF Report"):
    try:
        draft_values = [float(x) for x in draft_points if x.strip() != ""]
        density_val = float(density) if density.strip() != "" else None
        summary = calculate_draft_summary(draft_values, density_val)

        trim_img_buf = None
        if len(draft_values) >= 2:
            fwd = draft_values[0]
            aft = draft_values[-1]
            trim_img_buf = get_trim_image_buffer(fwd, aft)

        pdf_bytes = generate_pdf_report(
            ship_name=ship_name,
            imo_number=imo_number,
            surveyor=surveyor,
            draft_points=draft_values,
            density=density_val,
            summary=summary,
            date=datetime.today().strftime("%Y-%m-%d"),
            chart_image=trim_img_buf
        )

        st.download_button("Download PDF Report", data=pdf_bytes,
                           file_name=f"{ship_name}_draft_report.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"Error generating report: {e}")
