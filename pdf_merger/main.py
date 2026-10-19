from pathlib import Path
from pypdf import PdfWriter


def merge_inputs_pdfs(output_filename="merged_output.pdf"):
  # Set up directory paths
  root_dir = Path(__file__).parent.resolve()
  inputs_dir = root_dir / "inputs"
  output_path = root_dir / output_filename

  # Ensure the inputs directory exists
  if not inputs_dir.exists() or not inputs_dir.is_dir():
    print(f"Error: '{inputs_dir.name}' folder not found at {inputs_dir}")
    return

  # Find and sort all PDF files in alphabetical order
  pdf_files = sorted(inputs_dir.glob("*.pdf"))

  if not pdf_files:
    print(f"No PDF files found in '{inputs_dir.name}/'.")
    return

  # Merge PDFs
  merger = PdfWriter()
  print("Merging PDFs:")

  for pdf in pdf_files:
    print(f"  - Adding: {pdf.name}")
    merger.append(pdf)

  # Save to the root directory
  merger.write(output_path)
  merger.close()

  print(f"\nSuccess! Merged file saved to: {output_path.name}")


if __name__ == "__main__":
  merge_inputs_pdfs()