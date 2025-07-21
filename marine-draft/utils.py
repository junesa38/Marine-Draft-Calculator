from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO

def load_ship_image():
    return "static/ship_diagram.png"

def generate_pdf_report(
    ship_name,
    imo_number,
    surveyor,
    draft_points,
    density,
    summary,
    date,
    logo_path=None,
    signature_path=None
):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Marine Draft Survey Report")

    # Ship Information
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Ship Name: {ship_name}")
    c.drawString(50, height - 100, f"IMO Number: {imo_number}")
    c.drawString(50, height - 120, f"Surveyor: {surveyor}")
    c.drawString(50, height - 140, f"Survey Date: {date}")
    c.drawString(50, height - 160, f"Water Density: {density if density else 'Not Provided'}")

    # Ship logo (optional)
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo_io = BytesIO()
            logo.save(logo_io, format="PNG")
            logo_io.seek(0)
            c.drawImage(logo_io, width - 120, height - 100, width=60, height=40)
        except:
            c.drawString(width - 120, height - 100, "[Logo error]")

    # Draft points
    c.drawString(50, height - 190, "Draft Readings:")
    labels = ['FP', 'AP', 'Port', 'Stbd'] + (['FP-Port', 'AP-Stbd'] if len(draft_points) == 6 else [])
    for i, val in enumerate(draft_points):
        c.drawString(70, height - 210 - (i * 15), f"{labels[i]}: {val} m")

    # Calculation Summary
    c.drawString(50, height - 220 - (len(draft_points) * 15), "Calculation Summary:")
    c.drawString(70, height - 240 - (len(draft_points) * 15), f"Trim: {summary.get('trim', '-')} m")
    c.drawString(70, height - 255 - (len(draft_points) * 15), f"Mean Draft: {summary.get('mean_draft', '-')} m")
    if 'mean_draft_corrected' in summary and summary['mean_draft_corrected'] is not None:
        c.drawString(70, height - 270 - (len(draft_points) * 15), f"Corrected Mean Draft: {summary['mean_draft_corrected']} m")

    # Reference Image
    try:
        c.drawImage("static/ship_diagram.png", 50, 100, width=500, height=100)
    except:
        c.drawString(50, 100, "[Diagram image not found]")

    # Signature (optional)
    if signature_path:
        try:
            sign = Image.open(signature_path)
            sign_io = BytesIO()
            sign.save(sign_io, format="PNG")
            sign_io.seek(0)
            c.drawImage(sign_io, 70, 60, width=150, height=40)
            c.drawString(70, 50, f"Signature: {surveyor}")
        except:
            c.drawString(70, 50, "[Signature error]")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
