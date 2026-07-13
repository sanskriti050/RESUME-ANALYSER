from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_pdf(data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>Resume Analysis Report</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>ATS Score:</b> {data['ats_score']}/100", styles["Normal"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("<b>Resume Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(data["summary"], styles["Normal"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("<b>Technical Skills</b>", styles["Heading2"]))

    for skill in data["technical_skills"]:
        elements.append(Paragraph(f"• {skill}", styles["Normal"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("<b>Strengths</b>", styles["Heading2"]))

    for item in data["strengths"]:
        elements.append(Paragraph(f"• {item}", styles["Normal"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("<b>Weaknesses</b>", styles["Heading2"]))

    for item in data["weaknesses"]:
        elements.append(Paragraph(f"• {item}", styles["Normal"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("<b>Missing Keywords</b>", styles["Heading2"]))

    for item in data["missing_keywords"]:
        elements.append(Paragraph(f"• {item}", styles["Normal"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("<b>Suggestions</b>", styles["Heading2"]))

    for item in data["suggestions"]:
        elements.append(Paragraph(f"• {item}", styles["Normal"]))

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf