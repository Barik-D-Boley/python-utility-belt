import sys
import subprocess
import importlib.util
from pathlib import Path

# Tool metadata: script path, subfolder requirements file, and modules to check
TOOLS = {
  "pdf": {
    "script": Path("pdf_trimmer/main.py"),
    "reqs": Path("pdf_trimmer/requirements.txt"),
    "modules": ["pypdf"],
  },
  "bg": {
    "script": Path("img_bg_remover/main.py"),
    "reqs": Path("img_bg_remover/requirements.txt"),
    "modules": ["rembg", "onnxruntime", "PIL", "numpy"],
  },
  "qr": {
    "script": Path("qr_code_generator/main.py"),
    "reqs": Path("qr_code_generator/requirements.txt"),
    "modules": ["qrcode", "PIL", "numpy"],
  },
}

# Returns a list of modules from module_list that are not installed.
def check_missing_modules(module_list):
  missing = []
  for mod in module_list:
    if importlib.util.find_spec(mod) is None:
      missing.append(mod)
  return missing

# Prompts the user to install missing dependencies from a requirements.txt file.
def prompt_and_install(reqs_path):
  print(f"\n[!] Missing required packages for this tool.")
  choice = input("Would you like to install them now? (y/n): ").strip().lower()
  
  if choice in ["y", "yes"]:
    print("\n--> Installing dependencies...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(reqs_path)])
    if result.returncode == 0:
      print("--> Dependencies installed successfully!\n")
      return True
    else:
      print("[X] Installation failed. Please check your pip configuration.")
      return False
  else:
    print("--> Cannot run tool without required dependencies.")
    return False

def main():
  # Checks that the command has a valid shortcut; returns list of shortcuts if not a valid input
  if len(sys.argv) < 2 or sys.argv[1] not in TOOLS:
    print("\nAvailable tools:")
    for key in TOOLS:
      print(f"  - {key}: {TOOLS[key]['script'].parent.name}")
    print("\nUsage: python run.py <tool_shortcut>  (e.g., python run.py pdf)\n")
    return

  # Extracts tool metadata for the selected shortcut
  tool_info = TOOLS[sys.argv[1]]
  script_path = tool_info["script"]
  reqs_path = tool_info["reqs"]
  required_modules = tool_info["modules"]

  # Checks for missing dependencies and offer auto-install
  missing = check_missing_modules(required_modules)
  if missing:
    installed_ok = prompt_and_install(reqs_path)
    if not installed_ok:
      return

  # Resolves absolute directory path for Windows compatibility
  tool_dir = script_path.parent.resolve()
  script_file = script_path.name

  # Safety check: Ensure the subfolder actually exists
  if not tool_dir.exists():
    print(f"\n[X] Error: Directory '{tool_dir}' does not exist.")
    return

  subprocess.run([sys.executable, script_file], cwd=str(tool_dir))

if __name__ == "__main__":
  main()