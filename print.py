import win32api
import win32print
import win32con

printer_list = win32print.EnumPrinters(2)
print(printer_list)

def print_pdf(pdf_file_path, printer_name, paper_size):
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
                dev_mode.PaperWidth = content_width  # Specify the width in tenths of a millimeter
                dev_mode.PaperLength = content_height  # Specify the height in tenths of a millimeter

                # Disable background printing
                dev_mode.Fields |= win32con.DM_PRINTQUALITY
                dev_mode.PrintQuality = win32con.DMRES_DRAFT  # or win32con.DMRES_HIGH

                # Update the printer properties
                win32print.DocumentProperties(0, printer_handle, printer_name, dev_mode, dev_mode, win32con.DM_IN_BUFFER | win32con.DM_OUT_BUFFER)

                # Print the PDF file
                win32api.ShellExecute(
                    0,
                    "print",
                    pdf_file_path,
                    '/d:"%s"' % printer_name,
                    ".",
                    0
                )
                print("Printing...")
            finally:
                # Close the printer handle
                win32print.ClosePrinter(printer_handle)
        finally:
            # Reset the default printer back to the original default printer
            win32print.SetDefaultPrinter(default_printer)

# Specify the path to the PDF file, the printer name, and the desired paper size
pdf_file_path = "C:\\Users\\a\\Desktop\\os-api-web\\generated_doc.docx"
printer_name = "HP LaserJet Professional M1212nf MFP"
paper_size = win32con.DMPAPER_A4  # Example: Set the paper size to A4
content_width = 210  # Specify the content width in tenths of a millimeter
content_height = 297  # Specify the content height in tenths of a millimeter

# Call the function to print the PDF file with the specified paper size
print_pdf(pdf_file_path, printer_name, paper_size)