
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

FONT_PATHS = [
    "NotoSansTC-Regular.ttf",
    "./NotoSansTC-Regular.ttf",
    "assets/NotoSansTC-Regular.ttf",
]

_LOGO_PATHS = ["logo.png", "./logo.png", "assets/logo.png"]
_FAVICON_PATHS = ["logo2.png", "./logo2.png", "assets/logo2.png"]

def _register_font():
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont("NotoSansTC", p))
                return "NotoSansTC"
            except Exception:
                continue
    return "Helvetica"

def _find_first(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def build_report(
    title,
    subtitle,
    summary_text,
    advisor_actions,
    tables,
    images,
    footer_text="《影響力》傳承策略平台｜永傳家族辦公室｜Email：123@gracefo.com",
):
    """Build a branded PDF and return bytes.

    Args:
        title (str): main report title
        subtitle (str): sub title
        summary_text (str): narrative summary text
        advisor_actions (str): bullet suggestions (\n separated)
        tables (list[(str, DataFrame)]): list of (title, df)
        images (list[(str, bytes)]): list of (title, png_bytes)
        footer_text (str): footer line
    Returns:
        bytes: pdf file bytes
    """
    font_name = _register_font()
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    brand_color = HexColor("#0f766e")
    logo_path = _find_first(_LOGO_PATHS)

    # Cover
    c.setFillColor(brand_color)
    c.rect(0, height-90, width, 90, fill=1, stroke=0)
    if logo_path:
        try:
            c.drawImage(ImageReader(logo_path), 40, height-80, width=120, height=60, mask='auto')
        except Exception:
            pass
    c.setFillColor(HexColor("#ffffff"))
    c.setFont(font_name, 18)
    c.drawString(180, height-55, "影響力傳承平台 | 永傳家族辦公室")
    c.setFont(font_name, 12)
    c.drawString(180, height-78, datetime.now().strftime("%Y-%m-%d"))

    c.setFillColor(HexColor("#111111"))
    c.setFont(font_name, 20)
    c.drawString(40, height-130, title or "")
    c.setFont(font_name, 14)
    c.drawString(40, height-155, subtitle or "")

    c.setFont(font_name, 12)
    c.setFillColor(HexColor("#333333"))
    text = c.beginText(40, height-190)
    text.textLines(summary_text or "（無）")
    c.drawText(text)

    # Footer
    c.setFont(font_name, 9)
    c.setFillColor(HexColor("#666666"))
    c.drawRightString(width-40, 20, footer_text)
    c.showPage()

    # Images
    if images:
        for title_i, img_bytes in images:
            c.setFillColor(brand_color)
            c.rect(0, height-70, width, 70, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_name, 14)
            c.drawString(40, height-45, title_i or "圖表")
            try:
                img_r = ImageReader(io.BytesIO(img_bytes))
                max_w, max_h = width - 80, height - 160
                iw, ih = img_r.getSize()
                scale = min(max_w/iw, max_h/ih)
                w, h = iw*scale, ih*scale
                c.drawImage(img_r, 40 + (max_w-w)/2, 80 + (max_h-h)/2, width=w, height=h, mask='auto')
            except Exception:
                pass
            c.setFont(font_name, 9)
            c.setFillColor(HexColor("#666666"))
            c.drawRightString(width-40, 20, footer_text)
            c.showPage()

    # Tables & Actions
    c.setFillColor(brand_color)
    c.rect(0, height-70, width, 70, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont(font_name, 14)
    c.drawString(40, height-45, "分數摘要與顧問建議")

    y = height - 90
    c.setFillColor(HexColor("#111111"))
    c.setFont(font_name, 12)

    if tables:
        for ttitle, df in tables:
            c.setFont(font_name, 13)
            c.drawString(40, y, ttitle or "分數摘要")
            y -= 18
            c.setFont(font_name, 10)
            # header
            if hasattr(df, "columns"):
                x = 40
                for col in df.columns:
                    c.drawString(x, y, str(col))
                    x += 140
                y -= 14
                # rows
                if hasattr(df, "iterrows"):
                    for _, row in df.iterrows():
                        x = 40
                        for col in df.columns:
                            c.drawString(x, y, str(row[col]))
                            x += 140
                        y -= 14
                        if y < 80:
                            c.setFont(font_name, 9)
                            c.setFillColor(HexColor("#666666"))
                            c.drawRightString(width-40, 20, footer_text)
                            c.showPage()
                            y = height - 90
                            c.setFillColor(brand_color)
                            c.rect(0, height-70, width, 70, fill=1, stroke=0)
                            c.setFillColor(HexColor("#ffffff"))
                            c.setFont(font_name, 14)
                            c.drawString(40, height-45, "分數摘要（續）")
                            c.setFillColor(HexColor("#111111"))
                            c.setFont(font_name, 10)
            y -= 12

    if advisor_actions:
        c.setFont(font_name, 12)
        c.setFillColor(HexColor("#111111"))
        c.drawString(40, y, "顧問下一步建議")
        y -= 16
        for line in advisor_actions.splitlines():
            c.drawString(50, y, line)
            y -= 14
            if y < 80:
                c.setFont(font_name, 9)
                c.setFillColor(HexColor("#666666"))
                c.drawRightString(width-40, 20, footer_text)
                c.showPage()
                y = height - 90

    c.setFont(font_name, 9)
    c.setFillColor(HexColor("#666666"))
    c.drawRightString(width-40, 20, footer_text)
    c.showPage()
    c.save()
    return buf.getvalue()
