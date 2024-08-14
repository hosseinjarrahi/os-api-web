import win32con
import win32api
import win32print
from time import sleep

def getPrinters():
    return win32print.EnumPrinters(2)


def print_pdf(pdf_file_path, printer_name, paper_size,count):
    # Open the PDF file in binary mode
    with open(pdf_file_path, 'rb') as pdf_file:
        # Get the default printer
        default_printer = win32print.GetDefaultPrinter()

        try:
            # Set the desired printer as the default printer
            win32print.SetDefaultPrinter(printer_name)

            # Get the handle to the printer
            printer_handle = win32print.OpenPrinter(printer_name)

            try:
                # Get the current printer properties
                dev_mode = win32print.GetPrinter(printer_handle, 2)['pDevMode']

                # Set the paper size

                # Set the paper size to a custom size that matches the content dimensions
                dev_mode.Fields |= win32con.DM_PAPERSIZE
                dev_mode.PaperSize = paper_size
                # dev_mode.PaperWidth = content_width  # Specify the width in tenths of a millimeter
                # dev_mode.PaperLength = content_height  # Specify the height in tenths of a millimeter

                # Disable background printing
                dev_mode.Fields |= win32con.DM_PRINTQUALITY
                dev_mode.PrintQuality = win32con.DMRES_DRAFT  # or win32con.DMRES_HIGH

                # Update the printer properties
                win32print.DocumentProperties(0, printer_handle, printer_name, dev_mode, dev_mode, win32con.DM_IN_BUFFER | win32con.DM_OUT_BUFFER)

                # Print the PDF file
                for _ in range(count):
                    job_info = ("Print Job", None, "RAW")
                    win32print.StartDocPrinter(printer_handle, 1, job_info)
                    win32print.StartPagePrinter(printer_handle)
                    win32print.WritePrinter(printer_handle, pdf_file.read())
                    win32print.EndPagePrinter(printer_handle)
                    win32print.EndDocPrinter(printer_handle)
                    print("Printing...")
                    sleep(6)
                    
            finally:
                # Close the printer handle
                win32print.ClosePrinter(printer_handle)
        finally:
            # Reset the default printer back to the original default printer
            win32print.SetDefaultPrinter(default_printer)