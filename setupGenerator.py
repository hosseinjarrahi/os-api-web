import os

os.system(
    f'pyinstaller ./index.py  --exclude-module _bootlocale --onefile --name socket2.exe --add-data "./print.docx;." --add-data "./template_factor.docx;." --add-data "./template_surat.docx;."'
)

