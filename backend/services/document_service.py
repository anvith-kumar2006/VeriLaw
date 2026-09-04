"""
services/document_service.py – PDF and HTML complaint document generation.

Uses ReportLab for PDF generation with a plain-text fallback.
HTML generation is always available (no extra dependencies).
"""

import os
import uuid
import logging
from datetime import datetime

logger = logging.getLogger("verilaw")


def generate_pdf(file_path: str, user, complaint, category, department, evidence_list) -> None:
    """
    Write a PDF complaint document to file_path using ReportLab.
    Falls back to a plain-text file if ReportLab is not installed.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        )

        doc = SimpleDocTemplate(
            file_path, pagesize=A4,
            leftMargin=50, rightMargin=50, topMargin=60, bottomMargin=60,
        )
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("⚖ JUDICIARY FLOW", styles["Title"]))
        story.append(Paragraph("Complaint Document", styles["Heading1"]))
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            f"Generated: {datetime.utcnow().strftime('%d %B %Y %H:%M UTC')}",
            styles["Normal"],
        ))
        story.append(Spacer(1, 14))

        def section(title, rows):
            story.append(Paragraph(title, styles["Heading2"]))
            t = Table(rows, colWidths=[160, 330])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1a3a5c")),
                ("TEXTCOLOR",  (0, 0), (0, -1), colors.white),
                ("GRID",       (0, 0), (-1, -1), 0.4, colors.grey),
                ("ROWBACKGROUNDS", (1, 0), (-1, -1),
                 [colors.HexColor("#f4f8ff"), colors.white]),
                ("PADDING",    (0, 0), (-1, -1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

        section("Complainant", [
            ["Name",   user.full_name],
            ["Email",  user.email],
            ["Mobile", user.mobile],
        ])
        section("Authority", [
            ["Department", department.department_name if department else "N/A"],
            ["Helpline",   department.helpline if department and department.helpline else "N/A"],
            ["Website",    department.website  if department and department.website  else "N/A"],
        ])
        section("Complaint Details", [
            ["Title",         complaint.title],
            ["Category",      category.category_name if category else "N/A"],
            ["State",         complaint.state],
            ["District",      complaint.district],
            ["Incident Date", str(complaint.incident_date or "N/A")],
            ["Status",        complaint.status],
            ["AI Confidence", f"{complaint.ai_confidence}%"],
        ])

        story.append(Paragraph("Description", styles["Heading2"]))
        story.append(Paragraph(complaint.description, styles["Normal"]))
        story.append(Spacer(1, 12))

        if evidence_list:
            story.append(Paragraph("Evidence", styles["Heading2"]))
            ev_data = [["File Name", "Type", "Size"]] + [
                [e.original_name, e.file_type,
                 f"{round((e.file_size or 0) / 1024, 1)} KB"]
                for e in evidence_list
            ]
            et = Table(ev_data, colWidths=[250, 60, 180])
            et.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
                ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                ("GRID",       (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING",    (0, 0), (-1, -1), 6),
            ]))
            story.append(et)
            story.append(Spacer(1, 12))

        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "Complainant Signature: _______________________   Date: _______________",
            styles["Normal"],
        ))
        doc.build(story)

    except ImportError:
        # Fallback: plain text
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(f"COMPLAINT: {complaint.title}\n")
            fh.write(f"Category:  {category.category_name if category else 'N/A'}\n")
            fh.write(f"Status:    {complaint.status}\n\n")
            fh.write(complaint.description)


def generate_html(file_path: str, user, complaint, category, department, evidence_list) -> None:
    """Write an HTML complaint document to file_path."""
    ev_rows = "".join(
        f"<tr><td>{e.original_name}</td><td>{e.file_type}</td>"
        f"<td>{round((e.file_size or 0) / 1024, 1)} KB</td></tr>"
        for e in evidence_list
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Complaint – {complaint.title}</title>
  <style>
    body {{font-family:Arial,sans-serif;margin:40px;color:#222;}}
    h1   {{color:#1a3a5c;border-bottom:2px solid #1a3a5c;padding-bottom:8px;}}
    h2   {{color:#2c5f8a;margin-top:28px;}}
    table{{width:100%;border-collapse:collapse;margin-top:10px;}}
    th,td{{padding:10px 14px;border:1px solid #ccc;text-align:left;}}
    th   {{background:#1a3a5c;color:#fff;}}
    tr:nth-child(even){{background:#f4f8ff;}}
    .footer{{margin-top:60px;border-top:1px solid #ccc;padding-top:20px;}}
  </style>
</head>
<body>
  <h1>⚖ Judiciary Flow – Complaint Document</h1>
  <p><strong>Generated:</strong> {datetime.utcnow().strftime("%d %B %Y %H:%M UTC")}</p>

  <h2>Complainant</h2>
  <table>
    <tr><th>Name</th><td>{user.full_name}</td></tr>
    <tr><th>Email</th><td>{user.email}</td></tr>
    <tr><th>Mobile</th><td>{user.mobile}</td></tr>
  </table>

  <h2>Authority</h2>
  <table>
    <tr><th>Department</th><td>{department.department_name if department else "N/A"}</td></tr>
    <tr><th>Helpline</th><td>{department.helpline if department and department.helpline else "N/A"}</td></tr>
    <tr><th>Website</th><td>{department.website if department and department.website else "N/A"}</td></tr>
  </table>

  <h2>Complaint Details</h2>
  <table>
    <tr><th>Title</th><td>{complaint.title}</td></tr>
    <tr><th>Category</th><td>{category.category_name if category else "N/A"}</td></tr>
    <tr><th>State</th><td>{complaint.state}</td></tr>
    <tr><th>District</th><td>{complaint.district}</td></tr>
    <tr><th>Incident Date</th><td>{complaint.incident_date or "N/A"}</td></tr>
    <tr><th>Status</th><td>{complaint.status}</td></tr>
    <tr><th>AI Confidence</th><td>{complaint.ai_confidence}%</td></tr>
  </table>

  <h2>Description</h2>
  <p style="line-height:1.7">{complaint.description}</p>

  <h2>Evidence</h2>
  <table>
    <tr><th>File Name</th><th>Type</th><th>Size</th></tr>
    {ev_rows or "<tr><td colspan='3'>No evidence uploaded.</td></tr>"}
  </table>

  <div class="footer">
    <p>Complainant Signature: _________________________&nbsp;&nbsp; Date: _____________</p>
  </div>
</body>
</html>"""
    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write(html)
