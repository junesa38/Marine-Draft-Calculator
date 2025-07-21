from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
import io
import os
import sys

sys.path.append(os.path.dirname(__file__))

def load_ship_image():
    try:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(dir_path, "static", "ship_diagram.png")
        if os.path.exists(img_path):
            return Image.open(img_path)
        else:
            raise FileNotFoundError("ship_diagram.png not found.")
    except Exception as e:
        raise RuntimeError(f"Error loading image: {str(e)}")

def generate_pdf_report(ship_name, imo_number, surveyor, draft_points, density, summary, date, chart_image=None):
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

    try:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(dir_path, "static", "ship_diagram.png")
        if os.path.exists(img_path):
            c.drawImage(img_path, 50, 400, width=500, height=150)
        else:
            c.drawString(50, 400, "[Ship diagram not found]")
    except Exception as e:
        c.drawString(50, 400, f"[Error loading image: {str(e)}]")

    if chart_image:
        try:
            c.drawImage(chart_image, 50, 280, width=500, height=100)
        except Exception as e:
            c.drawString(50, 280, f"[Failed to render chart: {str(e)}]")
    else:
        c.drawString(50, 280, "[No chart provided]")

    c.save()
    buffer.seek(0)
    return buffer
