import io
from pathlib import Path
from tkinter import Tk, filedialog
from PIL import Image, ImageOps
from pypdf import PdfReader, PdfWriter

# Supported image extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}

# Default target page size in points if no PDF is provided (8.5 x 11 inches / Letter)
DEFAULT_PAGE_WIDTH = 612.0
DEFAULT_PAGE_HEIGHT = 792.0


# Finds the first PDF in the files list and returns its (width, height) in points.
def get_target_pdf_dimensions(files):
  for file in files:
    if file.suffix.lower() == ".pdf":
      try:
        reader = PdfReader(file)
        if reader.pages:
          first_page = reader.pages[0]
          return float(first_page.mediabox.width), float(first_page.mediabox.height)
      except Exception as e:
        print(f"    [!] Couldn't read page size from {file.name}: {e}")
  return DEFAULT_PAGE_WIDTH, DEFAULT_PAGE_HEIGHT


def merge_input_files():
  # Set up directory paths
  root_dir = Path(__file__).parent.resolve()
  input_dir = root_dir / "input"

  # Ensure input directory exists
  if not input_dir.exists() or not input_dir.is_dir():
    print(f"Error: '{input_dir.name}' folder not found at {input_dir}")
    return

  # Separate PDFs and Images, sort each group A-Z, then place PDFs before Images
  pdf_files = sorted(
    [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"],
    key=lambda x: x.name.lower()
  )
  image_files = sorted(
    [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS],
    key=lambda x: x.name.lower()
  )
  files = pdf_files + image_files

  if not files:
    print(f"No PDFs or supported images found in '{input_dir.name}/'.")
    return

  # Ask for output filename in console first (defaults to merged_output.pdf on Enter)
  user_input = input("Enter output filename (default: merged_output.pdf): ").strip()
  if not user_input:
    default_name = "merged_output.pdf"
  elif not user_input.lower().endswith(".pdf"):
    default_name = f"{user_input}.pdf"
  else:
    default_name = user_input

  # Launch OS File Explorer "Save As" window with the typed/default filename
  root = Tk()
  root.withdraw()  # Hide the main Tkinter root window
  root.attributes("-topmost", True)  # Bring the Save dialog window to the front

  save_path_str = filedialog.asksaveasfilename(
    initialdir=root_dir,
    initialfile=default_name,
    defaultextension=".pdf",
    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
    title="Save Merged PDF As"
  )
  root.destroy()

  # Exit if user cancels the Save dialog
  if not save_path_str:
    print("Save operation cancelled.")
    return

  output_path = Path(save_path_str)

  # Detect target page dimensions from the first PDF in input (or fall back to Letter size)
  target_w, target_h = get_target_pdf_dimensions(files)

  merger = PdfWriter()
  print("\nMerging files:")

  dpi = 150.0  # High quality conversion DPI
  scale = dpi / 72.0
  canvas_w = int(target_w * scale)
  canvas_h = int(target_h * scale)

  for file in files:
    ext = file.suffix.lower()

    if ext == ".pdf":
      print(f"  - Adding PDF: {file.name}")
      merger.append(file)

    elif ext in IMAGE_EXTENSIONS:
      print(f"  - Resizing & Adding Image: {file.name}")
      try:
        with Image.open(file) as img:
          img_rgb = img.convert("RGB")

          # Fit image inside target canvas dimensions without stretching/distorting
          fitted_img = ImageOps.contain(img_rgb, (canvas_w, canvas_h))

          # Create a white background canvas matching the target PDF page dimensions
          canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))

          # Center the image on the canvas
          paste_x = (canvas_w - fitted_img.width) // 2
          paste_y = (canvas_h - fitted_img.height) // 2
          canvas.paste(fitted_img, (paste_x, paste_y))

          # Save to PDF stream with target DPI so physical dimensions match the PDF points
          pdf_bytes = io.BytesIO()
          canvas.save(pdf_bytes, format="PDF", resolution=dpi)
          pdf_bytes.seek(0)
          merger.append(pdf_bytes)
      except Exception as e:
        print(f"    [X] Failed to convert image {file.name}: {e}")

  # Save directly to the path chosen in File Explorer
  merger.write(output_path)
  merger.close()

  print(f"\nSuccess! Merged file saved to: {output_path}")


if __name__ == "__main__":
  merge_input_files()