import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader, PdfWriter

# Parses a string like '13, 17-19, 21' into a sorted list of 0-based page indices.
def parse_page_selection(selection_str, total_pages):
  pages_to_keep = set()
  
  # Split the input string by commas
  parts = selection_str.split(',')
  
  for part in parts:
    part = part.strip()
    if not part:
      continue
      
    if '-' in part:
      # Handle ranges (e.g., "17-19")
      try:
        start, end = part.split('-')
        start_idx = int(start.strip()) - 1
        end_idx = int(end.strip()) - 1
        
        # Ensure the indices stay within the document's bounds
        start_idx = max(0, start_idx)
        end_idx = min(total_pages - 1, end_idx)
        
        if start_idx <= end_idx:
          pages_to_keep.update(range(start_idx, end_idx + 1))
      except ValueError:
        print(f"  [!] Warning: Could not parse range '{part}'")
    else:
      # Handle single pages (e.g., "13")
      try:
        idx = int(part) - 1
        if 0 <= idx < total_pages:
          pages_to_keep.add(idx)
      except ValueError:
        print(f"  [!] Warning: Could not parse page number '{part}'")
        
  # Return a sorted list so pages remain in sequential order
  return sorted(list(pages_to_keep))

def main():
  # Check if the input folder exists
  if not os.path.exists("input"):
    print("Error: The 'input' folder does not exist. Please create it and place your PDF inside.")
    return

  # Automatically find PDF files in the 'input' folder
  pdf_files = [f for f in os.listdir("input") if f.lower().endswith('.pdf')]
  
  if not pdf_files:
    print("Error: No PDF files found in the 'input' folder. Please add one and try again.")
    return

  # Handle PDF selection
  if len(pdf_files) == 1:
    filename = pdf_files[0]
    print(f"Found PDF: '{filename}'")
  else:
    print("Multiple PDFs found in the 'input' folder:\n")
    for idx, f in enumerate(pdf_files, 1):
      print(f"{idx}. {f}")
      
    while True:
      try:
        choice = int(input("\nSelect a PDF number to process:\n> "))
        if 1 <= choice <= len(pdf_files):
          filename = pdf_files[choice - 1]
          print(f"Selected: '{filename}'")
          break
        else:
          print(f"Please enter a number between 1 and {len(pdf_files)}.")
      except ValueError:
        print("Invalid input. Please enter a valid number.")

  input_pdf = os.path.join("input", filename)

  try:
    # Read the PDF and get the page count
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    print(f"This document has {total_pages} pages.")
    
    # Ask for user input right away
    selection = input("\nEnter the pages you want to keep (e.g., 17-19, 13, 18, 21):\n> ")
    
    pages_to_keep = parse_page_selection(selection, total_pages)
    
    if not pages_to_keep:
      print("No valid pages selected. Exiting.")
      return
      
    print(f"\nExtracting {len(pages_to_keep)} pages...")
    
    # Create a new PDF writer and add only the selected pages
    writer = PdfWriter()
    for page_num in pages_to_keep:
      writer.add_page(reader.pages[page_num])
      
    # Ensure the output directory exists
    if not os.path.exists("output"):
      os.makedirs("output")
      
    print("\nOpening Save window...")
    
    # Hide the main Tkinter blank root window
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # Bring save dialog window to front

    # Extract filename without the '.pdf' extension
    base_name = os.path.splitext(filename)[0]

    user_input = input("\nEnter the name of the file (press enter for default name):\n> ").strip()

    if user_input:
      pdf_name = user_input if user_input.lower().endswith(".pdf") else f"{user_input}.pdf"
    else:
      pdf_name = f"{base_name}-trimmed.pdf"

    # Open OS File Save window defaulting to the root project folder
    output_pdf = filedialog.asksaveasfilename(
      initialdir=os.path.abspath("."),
      initialfile=pdf_name,
      title="Save Trimmed PDF As",
      defaultextension=".pdf",
      filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )

    # Exit gracefully if the user cancels or closes the window
    if not output_pdf:
      print("Save cancelled by user. Exiting.")
      return
    
    with open(output_pdf, "wb") as f:
      writer.write(f)
      
    print(f"Done! Saved natively to: '{output_pdf}'")
    
  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == "__main__":
  main()