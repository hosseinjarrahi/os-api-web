import os

os.system(
    f'pyinstaller ./index.py --exclude-module _bootlocale --onefile --name osConnector.exe'
)

# os.system(
#     f'pyinstaller ./readerLoop.py --collect-all ultralytics --add-binary C:\\Users\\Hossein\\.pyenv\\pyenv-win\\versions\\3.12.3\\Lib\\site-packages\\pyzbar\\libzbar-64.dll;. --add-binary C:\\Users\\Hossein\\.pyenv\\pyenv-win\\versions\\3.12.3\\Lib\\site-packages\\pyzbar\\libiconv.dll;. --onefile --name loop.exe'
# )


