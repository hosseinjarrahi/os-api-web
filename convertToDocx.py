from docxtpl import DocxTemplate,InlineImage
from docx.shared import Mm
import userpaths
import qrcode
import os

my_docs = userpaths.get_my_documents()

pdf_file_path = my_docs + "\\print.docx"

rootPath = os.path.dirname(os.path.realpath(__file__))

def run(template,context):
    doc = DocxTemplate(template)
    
    templateName = os.path.basename(template)

    if templateName == 'template_surat.docx':
        img = qrcode.make(context.get('invoice_number'))
        qrPath = rootPath + "\\qr.png"
        img.save(qrPath)
        qr = InlineImage(doc, image_descriptor=qrPath,width=Mm(20),height=Mm(20))
        context['qr'] = qr

    doc.render(context)

    doc.save(pdf_file_path)

    return True