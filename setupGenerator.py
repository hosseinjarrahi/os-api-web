import os

os.system(
    f'pyinstaller ./index.py  --onefile --name socket2.exe --add-data "./print.docx;." --add-data "./template_factor.docx;." --add-data "./template_surat.docx;."'
)

