from docxtpl import DocxTemplate

def run(template,context):
    doc = DocxTemplate(template)
    doc.render(context)
    doc.save("./print.docx")
    return True