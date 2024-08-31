import win32con
import win32api
import win32print
from time import sleep
import win32com.client
import pythoncom
import traceback
import os
import signal

def getPrinters():
    return win32print.EnumPrinters(2)

def is_printer_available(printer_name):
    printers = [printer[2] for printer in getPrinters()]
    return printer_name in printers

def terminate_word_process():
    # Terminate all instances of Word if the application cannot close normally
    os.system("taskkill /F /IM WINWORD.EXE")

def print_word_file(word_file_path, printer_name, paper_size, count):
    if not is_printer_available(printer_name):
        print(f"Printer '{printer_name}' is not available.")
        return

    paper_size = win32con.DMPAPER_A4  # سایز کاغذ به عنوان مثال A4
    count = 1  # تعداد پرینت
    # Get the default printer
    default_printer = win32print.GetDefaultPrinter()

    try:
        # Set the desired printer as the default printer
        win32print.SetDefaultPrinter(printer_name)

        # Get the handle to the printer
        printer_handle = win32print.OpenPrinter(printer_name)
        pythoncom.CoInitialize()  # اضافه کردن این خط
        try:
            # Get the current printer properties
            dev_mode = win32print.GetPrinter(printer_handle, 2)['pDevMode']

            # Set the paper size
            dev_mode.Fields |= win32con.DM_PAPERSIZE
            dev_mode.PaperSize = paper_size

            # Disable background printing
            dev_mode.Fields |= win32con.DM_PRINTQUALITY
            dev_mode.PrintQuality = win32con.DMRES_DRAFT  # or win32con.DMRES_HIGH

            # Update the printer properties
            win32print.DocumentProperties(0, printer_handle, printer_name, dev_mode, dev_mode, win32con.DM_IN_BUFFER | win32con.DM_OUT_BUFFER)

            # Print the Word file using Word application
            for _ in range(count):
                try:
                    print("________________________________________________________")
                    # راه‌اندازی Word
                    word = win32com.client.Dispatch("Word.Application")
                    doc = word.Documents.Open(word_file_path)

                    print(f"Opened document: {doc.Name}")

                    # تنظیم پرینتر پیش‌فرض
                    word.ActivePrinter = printer_name

                    # پرینت فایل
                    doc.PrintOut()

                    print("Printing...")
                    
                except Exception as e:
                    print(f"An error occurred during printing: {e}")
                    traceback.print_exc()
                finally:
                    # تلاش برای بستن فایل ورد بدون ذخیره تغییرات
                    try:
                        if 'doc' in locals() and win32com.client.IsObject(doc):
                            doc.Close(False)
                    except Exception as close_error:
                        print(f"An error occurred while closing the document: {close_error}")
                        traceback.print_exc()
                    finally:
                        try:
                            if win32com.client.IsObject(word):
                                word.Quit()
                        except Exception as quit_error:
                            print(f"An error occurred while quitting Word: {quit_error}")
                            traceback.print_exc()

                sleep(6)  # Wait time between prints (if multiple prints)
                
        finally:
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)
    finally:
        # Reset the default printer back to the original default printer
        win32print.SetDefaultPrinter(default_printer)
        # در صورتی که ورد هنوز بسته نشده، فرآیند را به صورت اجباری خاتمه دهید
        terminate_word_process()

# Example usage
