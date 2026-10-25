import subprocess
import win32com.client
from pathlib import Path

# Close any orphaned PowerPoint processes from prior crashed runs
try:
  subprocess.run(["taskkill", "/F", "/IM", "POWERPNT.EXE"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception:
  pass

script_dir = Path(__file__).parent.resolve()
input_dir = script_dir / "input"
output_dir = script_dir / "output"
output_dir.mkdir(parents=True, exist_ok=True)

files = sorted(input_dir.glob("*.pptx"))

if not files:
  print(f"No .pptx files found in '{input_dir}'.")
  exit()

default_name = "merged_output.pptx"
custom_name = input(f"\nEnter output file name (press Enter for default '{default_name}'): ").strip()

filename = custom_name if custom_name else default_name
if not filename.endswith(".pptx"):
  filename += ".pptx"

output_path = output_dir / filename

ppt_app = win32com.client.Dispatch("PowerPoint.Application")

print(f"Merging {len(files)} presentation(s)...")

try:
  # Open the first file as the base presentation
  merged_prs = ppt_app.Presentations.Open(str(files[0].resolve()))

  # Append all subsequent presentations
  for file in files[1:]:
    merged_prs.Slides.InsertFromFile(str(file.resolve()), merged_prs.Slides.Count)

  # Save to the target output file
  merged_prs.SaveAs(str(output_path.resolve()))
  merged_prs.Close()
  print(f"Done! Merged file saved to '{output_path}'.\n")

finally:
  ppt_app.Quit()