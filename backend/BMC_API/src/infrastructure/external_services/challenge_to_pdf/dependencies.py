import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from BMC_API.src.core.config.settings import settings


def add_horizontal_lines(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColorRGB(0.7, 0.7, 0.7)  # Set line color
    canvas.setLineWidth(0.5)  # Set line width

    if doc.page > 1:  # Add top line on pages after the first page
        canvas.line(
            0,
            doc.height + doc.topMargin + 10,
            doc.width + 2 * doc.leftMargin,
            doc.height + doc.topMargin + 10,
        )

    # Add bottom line on all pages
    canvas.line(
        0,
        doc.bottomMargin,
        doc.width + 2 * doc.leftMargin,
        doc.bottomMargin,
    )
    canvas.restoreState()


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, header_text="", **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.header_text = header_text

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for i, page in enumerate(self.pages):
            self.__dict__.update(page)
            if i > 0:
                self.drawHeader()
            if i == page_count - 1:
                self.addTimestamp()
            self.drawPageNumber(page_count)
            self.drawLink(i)

            super().showPage()

        super().save()

    def drawPageNumber(self, page_count):
        page_number_text = "Page %d of %d" % (self._pageNumber, page_count)
        self.setFont("OpenSans-Light", 10)
        text_width = self.stringWidth(page_number_text, "OpenSans-Light", 10)
        canvas_width, canvas_height = self._pagesize
        x = (canvas_width - text_width) / 2  # Horizontal center
        y = 20  # Bottom margin of 1 inch (adjust as needed)
        self.drawString(x, y, page_number_text)

    def drawLink(self, i):
        link_text = "Biomedical Image Analysis ChallengeS (BIAS) Initiative"
        link_url = "https://www.dkfz.de/en/cami/research/topics/biasInitiative.html?m=1581426918"
        self.setFont("OpenSans-Light", 8)
        link_width = self.stringWidth(link_text, "OpenSans-Light", 8)
        canvas_width, canvas_height = self._pagesize
        x = canvas_width - link_width - 10  # Right side of the page with 1 inch margin
        y = 20  # Same y-axis position as page number
        rect = (
            x,
            y - 2,
            x + link_width,
            y + 12,
        )  # Adjust the link height as needed
        self.drawRect(*rect, fill=0, stroke=0)
        self.setFillColorRGB(0, 0.278, 0.725)  # Set text color to #0047b9
        self.setFont("OpenSans-Light", 8)

        self.drawCentredString((rect[2] + rect[0]) / 2, rect[1] + 0.1 * 20, link_text)
        if i == 0:
            self.linkURL(link_url, rect)

        underline = (
            x,
            y - 3,
            x + link_width,
            y - 3,
        )

        self.drawRect(
            *underline,
            fill=1,
            stroke=0,
        )

    def drawHeader(self):
        self.setFont("OpenSans-Light", 10)
        self.setFillColorRGB(0.2, 0.2, 0.2)
        text_width = self.stringWidth(self.header_text, "OpenSans-Light", 10)
        canvas_width, _ = self._pagesize
        x = (canvas_width - text_width) / 2  # Horizontal center
        # x = 30  # Left margin
        y = self._pagesize[1] - 25  # Top margin
        self.drawString(x, y, self.header_text)

    def drawRect(self, x1, y1, x2, y2, *args, **kwargs):
        self.saveState()
        self.rect(x1, y1, x2 - x1, y2 - y1, *args, **kwargs)
        self.restoreState()

    def addTimestamp(self):
        current_time = datetime.now().astimezone()
        current_timezone_name = current_time.tzname()
        timestamp_text = f"Created at {current_time.isoformat()} ({current_timezone_name})"
        self.setFont("OpenSans-Light", 6)
        text_width = self.stringWidth(timestamp_text, "OpenSans-Light", 6)
        canvas_width, canvas_height = self._pagesize
        x = (canvas_width - text_width) / 2  # Horizontal center
        y = 5  # Bottom margin of 1 inch (adjust as needed)
        self.drawString(x, y, timestamp_text)


def register_fonts():
    # Register fonts
    font_path = os.path.join(
        settings.root_dir, "src", "infrastructure", "external_services", "challenge_to_pdf", "extra_fonts", "open_sans"
    )
    pdfmetrics.registerFont(TTFont("OpenSans", os.path.join(font_path, "OpenSans-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("OpenSans-Bold", os.path.join(font_path, "OpenSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("OpenSans-ExtraBold", os.path.join(font_path, "OpenSans-ExtraBold.ttf")))
    pdfmetrics.registerFont(TTFont("OpenSans-ExtraBold", os.path.join(font_path, "OpenSans-ExtraBold.ttf")))

    pdfmetrics.registerFont(TTFont("OpenSans-Italic", os.path.join(font_path, "OpenSans-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("OpenSans-BoldItalic", os.path.join(font_path, "OpenSans-BoldItalic.ttf")))
    pdfmetrics.registerFont(TTFont("OpenSans-LightItalic", os.path.join(font_path, "OpenSans-LightItalic.ttf")))

    pdfmetrics.registerFont(TTFont("OpenSans-Light", os.path.join(font_path, "OpenSans-Light.ttf")))


def set_document_styles():
    # Styles
    styles = getSampleStyleSheet()

    styles["Normal"].fontSize = 10
    styles["Normal"].fontName = "OpenSans"
    styles["Normal"].spaceAfter = 6
    styles["Normal"].spaceBefore = 6

    styles["Definition"].fontSize = 10
    styles["Definition"].fontName = "OpenSans-Light"  # "OpenSans-LightItalic"
    styles["Definition"].leftIndent = 0
    styles["Definition"].spaceAtfer = 6
    styles["Definition"].spaceBefore = 6

    styles["Title"].fontSize = 14
    styles["Title"].fontName = "OpenSans-ExtraBold"
    styles["Title"].textColor = "#0047b9"
    styles["Title"].alignment = 0

    styles["Heading1"].fontSize = 19
    styles["Heading1"].fontName = "OpenSans-ExtraBold"
    styles["Heading1"].textColor = "#0047b9"  # "#0047b9"

    styles["Heading2"].fontSize = 12
    styles["Heading2"].fontName = "OpenSans-ExtraBold"
    styles["Heading2"].textColor = "#0047b9"

    styles["Heading3"].fontSize = 10
    styles["Heading3"].fontName = "OpenSans-Bold"
    styles["Heading3"].textColor = "#0047b9"

    # Make all line spaces 1.5
    for style in styles.byName.keys():
        if hasattr(styles[style], "leading"):
            styles[style].leading = 1.70 * styles[style].fontSize

    return styles
