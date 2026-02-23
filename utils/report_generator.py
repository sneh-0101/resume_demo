from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import io

def generate_report(resume_name, match_score, matched_skills, missing_skills, suggestions):
    """
    Generates a PDF report for the resume analysis.
    Returns a bytes object of the PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=1))
    styles.add(ParagraphStyle(name='Header', fontSize=18, spaceAfter=20, alignment=1, textColor=colors.HexColor("#2E86C1")))
    styles.add(ParagraphStyle(name='SubSection', fontSize=14, spaceBefore=15, spaceAfter=10, textColor=colors.HexColor("#2874A6")))
    
    # Content Container
    elements = []
    
    # Title
    elements.append(Paragraph("AI Resume Analysis Report", styles['Header']))
    elements.append(Paragraph(f"Candidate: {resume_name}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Score Section
    score_color = colors.green if match_score >= 70 else colors.orange if match_score >= 40 else colors.red
    elements.append(Paragraph(f"Match Score: <font color='{score_color}'><b>{match_score}%</b></font>", styles['SubSection']))
    elements.append(Spacer(1, 12))
    
    # Skills Table
    elements.append(Paragraph("Skill Analysis:", styles['SubSection']))
    
    data = [['Matched Skills', 'Missing Skills']]
    
    # Transpose lists to fit table
    max_len = max(len(matched_skills), len(missing_skills))
    for i in range(max_len):
        m = matched_skills[i] if i < len(matched_skills) else ""
        miss = missing_skills[i] if i < len(missing_skills) else ""
        data.append([m, miss])
        
    if not data[1:]: # handle empty lists
        data.append(["None", "None"])

    # Table Style
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Suggestions
    elements.append(Paragraph("Improvement Suggestions:", styles['SubSection']))
    for suggestion in suggestions:
        elements.append(Paragraph(f"• {suggestion}", styles['Normal']))
        elements.append(Spacer(1, 6))
        
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
