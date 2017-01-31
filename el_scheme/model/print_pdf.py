__author__ = 'Fredrik Salovius'


from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import black, gray, green, blue, lightgrey, darkgrey
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Image, BaseDocTemplate, Frame, Paragraph, PageTemplate
import StringUtils
class PdfPrinter():
    def __init__(self):
        self.style = getSampleStyleSheet()['Normal']
        self.file_path = StringUtils.resource_path('el_schema.pdf')
        print self.file_path
        self.data = []

    def set_filepath(self, path):
        self.file_path = path

    def set_data(self, data):
        self.data = data

    def print_pdf(self, lst):
        self.set_data(lst)
        doc = BaseDocTemplate(self.file_path, pagesize=A4, leftMargin=1.5 * inch, rightMargin=1.5 * inch, topMargin=0)
        frame = Frame(doc.leftMargin, doc.height, doc.width, doc.height)
        # Create the canvas, draw page and att to document
        template = PageTemplate(frames=frame, onPage=self.buildDocument)
        doc.addPageTemplates([template])
        story = []
        story.append(Paragraph(" ", self.style))
        doc.build(story)

    def buildDocument(self, canvas, doc):

        startX = doc.leftMargin
        startY = doc.height
        title = 'test'
        tableText = canvas.beginText()
        tableText.setFillColor(black)
        tableText.setTextOrigin(startX + 3, startY + 4)
        tableText.setFont("Courier", 18)
        tableText.setLeading(20)
        tableText.textLine(title)
        # For formatting purposes, we need the longest string width
        longestWidth = 0
        for k in range(len(self.data)):
            for index in range(len(self.data[k]['data'])):
                data = self.data[k]['data']
                print data[index]
                width = canvas.stringWidth(data[index][0], fontName="Courier", fontSize=18)
                if width > longestWidth:
                    longestWidth = width
        offset = longestWidth+10

        for k in range(len(self.data)):
            for index in range(len(self.data[k]['data'])):
                data = self.data[k]['data']
                startOfLineX = tableText.getX()
                startOfLineY = tableText.getY()
                text = data[index]
                category = text[0]
                actualData = text[1]
                tableText.setLeading(20)
                tableText.textOut("%s:" % category)
                length = canvas.stringWidth(category, "Courier", 18)
                tableText.setXPos(offset)
                tableText.textOut("%s %s" % (actualData, 'apa'))
                currentPos = tableText.getX()
                tableText.setXPos(-offset)
                tableText.textLine()

        canvas.drawText(tableText)
    def create_table(self, canvas, doc, table_dict):
        startX = doc.leftMargin
        startY = doc.height
        title = 'test'
        tableText = canvas.beginText()
        tableText.setFillColor(black)
        tableText.setTextOrigin(startX + 3, startY + 4)
        tableText.setFont("Courier", 18)
        tableText.setLeading(20)
        tableText.textLine("{0}: {1}\t\t{2}".format(table_dict['title'][0], table_dict['title'][1], table_dict['title'][2]))
        # For formatting purposes, we need the longest string width
        longestWidth = 0
        data = table_dict['data']
        for index in range(len(data)):
            width = canvas.stringWidth(data[index][0], fontName="Courier", fontSize=18)
            if width > longestWidth:
                longestWidth = width
        offset = longestWidth + 10
        # Room          Device name         Other information
        # 100           100
        for index in range(len(data)):
            startOfLineX = tableText.getX()
            startOfLineY = tableText.getY()
            tableText.setLeading(20)
            for item in data[index]:
                tableText.textOut(item)
                tableText.setXPos(100)
            tableText.setXPos(-offset)
            tableText.textLine()

        canvas.drawText(tableText)

if __name__ == '__main__':
    printer = PdfPrinter()
    lst2 = [{
               'title': ['Fuse','1','16A'],
                'data': [
                    ['Room','Outlet, switch,lamp','Number of outlets'],
                    ['Hall','Socket-1','Outlests: 2'],
                    ['','Socket-2','Outlets: 2'],
                    ['','Switch-1','Outlets: 2'],
                    ['','Lamp-1', 'Controller: Switch-1'],
                    ['Kontor', 'Socket-3','Outlets; 2'],
                    ['', 'Socket-4','Outlets: 2'],
                    ['', 'Lamp-2','Switch-1']
                ]
            }]
    printer.print_pdf(lst2)





