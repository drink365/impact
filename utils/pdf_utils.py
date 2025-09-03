
import os, io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

FONT_CANDIDATES = ["NotoSansTC-Regular.ttf","./NotoSansTC-Regular.ttf","assets/NotoSansTC-Regular.ttf"]
LOGO_CANDIDATES = ["logo.png","./logo.png","assets/logo.png"]

def _choose(path_list):
    for p in path_list:
        if os.path.exists(p):
            return p
    return None

def _font_name():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont("NotoSansTC", p))
                return "NotoSansTC"
            except Exception:
                continue
    return "Helvetica"

def _paint_header_footer(c, font_name, footer_text):
    width, height = A4
    brand = HexColor("#0f766e")
    # header bar
    c.setFillColor(brand); c.rect(0, height-70, width, 70, fill=1, stroke=0)
    # logo
    logo = _choose(LOGO_CANDIDATES)
    if logo:
        try:
            c.drawImage(ImageReader(logo), 35, height-62, width=120, height=48, mask='auto')
        except Exception:
            pass
    # header right title
    c.setFont(font_name, 13); c.setFillColor(HexColor("#ffffff"))
    c.drawRightString(width-35, height-42, "影響力傳承平台 | 永傳家族辦公室")
    # footer
    c.setFont(font_name, 9); c.setFillColor(HexColor("#666666"))
    c.drawRightString(width-35, 22, footer_text)

def build_report(title, subtitle, summary_text, advisor_actions, tables, images,
                 footer_text="永傳家族辦公室  gracefo.com"):
    font_name = _font_name()
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # Cover
    _paint_header_footer(c, font_name, footer_text)
    c.setFillColor(HexColor("#111111")); c.setFont(font_name, 20)
    c.drawString(40, height-110, title or "")
    c.setFont(font_name, 13); c.drawString(40, height-132, subtitle or "")
    c.setFont(font_name, 11); c.setFillColor(HexColor("#444444"))
    c.drawString(40, height-154, datetime.now().strftime("%Y-%m-%d"))
    # intro text
    c.setFillColor(HexColor("#222222")); c.setFont(font_name, 11)
    t = c.beginText(40, height-185); t.textLines(summary_text or "（無）"); c.drawText(t)
    c.showPage()

    # Images pages
    if images:
        for ttitle, png in images:
            _paint_header_footer(c, font_name, footer_text)
            c.setFillColor(HexColor("#111111")); c.setFont(font_name, 13)
            c.drawString(40, height-110, ttitle or "圖表")
            try:
                img_r = ImageReader(io.BytesIO(png))
                max_w, max_h = width-80, height-200
                iw, ih = img_r.getSize()
                scale = min(max_w/iw, max_h/ih)
                w, h = iw*scale, ih*scale
                c.drawImage(img_r, 40+(max_w-w)/2, 80+(max_h-h)/2, width=w, height=h, mask='auto')
            except Exception:
                pass
            c.showPage()

    # Tables & actions
    _paint_header_footer(c, font_name, footer_text)
    y = height-110
    c.setFillColor(HexColor("#111111"))
    if tables:
        for ttitle, df in tables:
            c.setFont(font_name, 13); c.drawString(40, y, ttitle or "分數摘要"); y -= 18
            c.setFont(font_name, 10)
            if hasattr(df, "columns"):
                x = 40
                for col in df.columns:
                    c.drawString(x, y, str(col)); x += 140
                y -= 14
                if hasattr(df, "iterrows"):
                    for _, row in df.iterrows():
                        x = 40
                        for col in df.columns:
                            c.drawString(x, y, str(row[col])); x += 140
                        y -= 14
                        if y < 90:
                            c.showPage(); _paint_header_footer(c, font_name, footer_text); y = height-110
                            c.setFont(font_name, 10)
            y -= 10

    if advisor_actions:
        if y < 140: c.showPage(); _paint_header_footer(c, font_name, footer_text); y = height-110
        c.setFont(font_name, 12); c.drawString(40, y, "顧問下一步建議"); y -= 16
        c.setFont(font_name, 10)
        for line in advisor_actions.splitlines():
            c.drawString(48, y, line); y -= 13
            if y < 90:
                c.showPage(); _paint_header_footer(c, font_name, footer_text); y = height-110
                c.setFont(font_name, 10)

    c.showPage(); c.save()
    return buf.getvalue()
