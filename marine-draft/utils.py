from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
import io
import os
sys.path.append(os.path.dirname(__file__))

def load_ship_image():
    try:
    # Gunakan path absolut agar tidak tergantung lokasi eksekusi
    dir_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(dir_path, "static", "ship_diagram.png")
    
    if os.path.exists(img_path):
        c.drawImage(img_path, 50, 400, width=500, height=150)
    else:
        c.drawString(50, 400, "[Ship diagram not found]")
except Exception as e:
    c.drawString(50, 400, f"[Error loading image: {str(e)}]")

def generate_pdf_report(ship_name, imo_number, surveyor, draft_points, density, summary, date):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 12)

    c.drawString(50, 800, f"Ship Name: {ship_name}")
    c.drawString(50, 785, f"IMO Number: {imo_number}")
    c.drawString(50, 770, f"Surveyor: {surveyor}")
    c.drawString(50, 755, f"Date: {date}")
    c.drawString(50, 740, f"Water Density: {density if density else 'Not Provided'}")

    c.drawString(50, 710, "Draft Points:")
    for i, d in enumerate(draft_points):
        c.drawString(60, 695 - i*15, f"Point {i+1}: {d} m")

    c.drawString(50, 600, f"Mean Draft: {summary['mean_draft']} m")

    # Insert image if found
    try:
        img_path = os.path.join("static", "ship_diagram.png")
        c.drawImage(img_path, 50, 400, width=500, height=150)
    except:
        c.drawString(50, 400, "[Ship diagram not found]")

    c.save()
    buffer.seek(0)
    return buffer
