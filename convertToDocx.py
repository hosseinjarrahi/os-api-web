from docxtpl import DocxTemplate

doc = DocxTemplate("template.docx")
context = { 'items' : [
    {'item_name':'پارکین گ های من و مارینی','item_unit':'یونیت','item_number':5},
    {'item_name':'پارکین گ های من و مارینی','item_unit':'یونیت','item_number':5},
    {'item_name':'پارکین گ های من و مارینی','item_unit':'یونیت','item_number':5},
    {'item_name':'پارکین گ های من و مارینی','item_unit':'unit','item_number':5},
    {'item_name':'پارکین گ های من و مارینی','item_unit':'unit','item_number':5},
    {'item_name':'پارکین گ های من و مارینی','item_unit':'unit','item_number':5},
] }
doc.render(context)
doc.save("generated_doc.docx")
