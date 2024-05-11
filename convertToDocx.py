from docxtpl import DocxTemplate
import userpaths

my_docs = userpaths.get_my_documents()

pdf_file_path = my_docs + "\\print.docx"

def run(template,context):
    doc = DocxTemplate(template)
    doc.render(context)
    doc.save(pdf_file_path)
    return True