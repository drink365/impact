
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime, os

# Register custom font
font_path = os.path.join(os.path.dirname(__file__), "..", "NotoSansTC-Regular.ttf")
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("NotoSansTC", font_path))
    base_font = "NotoSansTC"
else:
    base_font = "Helvetica"

def build_pdf_report(output_path, title, summary_text, advisor_text, score_df, chart_paths, logo_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Custom", fontName=base_font, fontSize=12, leading=18))

    story = []
    # Cover with logo
    if logo_path and os.path.exists(logo_path):
        story.append(Image(logo_path, width=2*inch, height=2*inch))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(title, styles["Title"]))
    story.append(Paragraph("生成時間：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), styles["Custom"]))
    story.append(Spacer(1, 0.5*inch))

    story.append(Paragraph("AI 分析摘要", styles["Heading2"]))
    story.append(Paragraph(summary_text.replace("\n", "<br/>"), styles["Custom"]))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("顧問下一步建議", styles["Heading2"]))
    story.append(Paragraph(advisor_text.replace("\n", "<br/>"), styles["Custom"]))
    story.append(Spacer(1, 0.5*inch))

    # Charts
    for path in chart_paths:
        if path and os.path.exists(path):
            story.append(Image(path, width=5*inch, height=3*inch))
            story.append(Spacer(1, 0.2*inch))

    # Score table if provided
    if score_df is not None:
        data = [score_df.columns.tolist()] + score_df.values.tolist()
        table = Table(data)
        table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
                                   ("GRID", (0,0), (-1,-1), 0.5, colors.grey)]))
        story.append(table)

    doc.build(story)
    return output_path
