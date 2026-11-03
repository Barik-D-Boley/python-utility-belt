import re
from pathlib import Path
import shutil

ROOT_DIR = Path(__file__).parent.resolve()

def update_toml_all_extra(toml_text, shortcut):
  """Inserts shortcut into the python-utility-belt[...] list inside the 'all' extra in alphabetical order."""
  pattern = re.compile(r'("python-utility-belt\[)([^\]]+)(\]")')
  match = pattern.search(toml_text)
  if not match:
    return toml_text

  prefix = match.group(1)
  extras_raw = match.group(2)
  suffix = match.group(3)

  extras_list = [e.strip() for e in extras_raw.split(",") if e.strip()]
  if shortcut not in extras_list:
    extras_list.append(shortcut)
    extras_list.sort()

  new_extras_str = ",".join(extras_list)
  replacement = f"{prefix}{new_extras_str}{suffix}"

  return toml_text[:match.start()] + replacement + toml_text[match.end():]

def insert_toml_optional_dep(toml_text, shortcut):
  """Inserts shortcut = [] under [project.optional-dependencies] in alphabetical order (unindented)."""
  section_start = toml_text.find("[project.optional-dependencies]")
  if section_start == -1:
    return toml_text

  next_section = toml_text.find("\n[", section_start + 1)
  section_end = next_section if next_section != -1 else len(toml_text)
  section_content = toml_text[section_start:section_end]

  # Match top-level keys under optional-dependencies
  pattern = re.compile(r'^[ \t]*([a-zA-Z0-9_\-]+)[ \t]*=', re.MULTILINE)
  matches = list(pattern.finditer(section_content))

  new_line = f"{shortcut} = [\n  \n]\n"  # Unindented per TOML style

  insert_pos_in_section = None
  for m in matches:
    key = m.group(1).lower()
    if key == "all" or shortcut.lower() < key:
      insert_pos_in_section = m.start()
      break

  if insert_pos_in_section is not None:
    abs_pos = section_start + insert_pos_in_section
    updated_text = toml_text[:abs_pos] + new_line + toml_text[abs_pos:]
  else:
    abs_pos = section_start + len(section_content)
    if not toml_text[:abs_pos].endswith("\n"):
      new_line = "\n" + new_line
    updated_text = toml_text[:abs_pos] + new_line + toml_text[abs_pos:]

  return update_toml_all_extra(updated_text, shortcut)


def insert_run_py_tool(run_py_text, shortcut, folder_name):
  """Inserts new tool metadata dictionary into TOOLS in run.py in alphabetical order."""
  tools_start = run_py_text.find("TOOLS = {")
  if tools_start == -1:
    return run_py_text

  # Find the closing brace of the TOOLS dictionary
  tools_end_match = re.search(r'\n\}', run_py_text[tools_start:])
  if not tools_end_match:
    return run_py_text

  tools_end = tools_start + tools_end_match.start()
  tools_block = run_py_text[tools_start:tools_end]

  # Strictly match tool shortcut keys indented by EXACTLY 2 spaces ("shortcut": {)
  pattern = re.compile(r'^[ ]{2}"([a-zA-Z0-9_\-]+)":[ \t]*\{', re.MULTILINE)
  matches = list(pattern.finditer(tools_block))

  new_entry = (
    f'  "{shortcut}": {{\n'
    f'    "script": Path("{folder_name}/main.py"),\n'
    f'    "extra": "{shortcut}",\n'
    f'    "modules": [],\n'
    f'  }},\n'
  )

  insert_pos = None
  for m in matches:
    key = m.group(1).lower()
    if shortcut.lower() < key:
      insert_pos = m.start()
      break

  if insert_pos is not None:
    abs_pos = tools_start + insert_pos
    return run_py_text[:abs_pos] + new_entry + run_py_text[abs_pos:]
  else:
    abs_pos = tools_end
    if not run_py_text[:abs_pos].endswith("\n"):
      new_entry = "\n" + new_entry
    return run_py_text[:abs_pos] + new_entry + run_py_text[abs_pos:]


def insert_readme_table_row(readme_text, shortcut, tool_name, description, folder_name):
  """Inserts a new row into the root README.md table in alphabetical order cleanly."""
  table_header_idx = readme_text.find("| Shortcut | Tool Name |")
  if table_header_idx == -1:
    return readme_text

  divider_idx = readme_text.find("\n", table_header_idx)
  if divider_idx == -1:
    return readme_text
  divider_end = readme_text.find("\n", divider_idx + 1)
  if divider_end == -1:
    return readme_text

  table_start = divider_end + 1
  table_end_match = re.search(r'\n[ \t]*\n', readme_text[table_start:])
  table_end = table_start + table_end_match.start() if table_end_match else len(readme_text)

  table_block = readme_text[table_start:table_end]
  new_row = f"| `{shortcut}` | **{tool_name}** | {description} | Lightweight (~1 MB) | None | [`{folder_name}/`](./{folder_name}) |\n"

  # Match table row shortcuts: | `shortcut` |
  pattern = re.compile(r'^[ \t]*\|[ \t]*`([^`]+)`', re.MULTILINE)
  matches = list(pattern.finditer(table_block))

  insert_pos = None
  for m in matches:
    key = m.group(1).lower()
    if shortcut.lower() < key:
      insert_pos = m.start()
      break

  if insert_pos is not None:
    abs_pos = table_start + insert_pos
    return readme_text[:abs_pos] + new_row + readme_text[abs_pos:]
  else:
    abs_pos = table_start + len(table_block)
    if not readme_text[:abs_pos].endswith("\n"):
      new_row = "\n" + new_row
    return readme_text[:abs_pos] + new_row + readme_text[abs_pos:]


def create_new_tool(tools_dict):
  print("\n=== Tool Generator Scaffold ===")
  shortcut = input("Shortcut name (e.g., 'xyz'): ").strip().lower()

  if not shortcut:
    print("Error: Shortcut cannot be empty.")
    return

  if shortcut in tools_dict or shortcut == "new":
    print(f"Error: Shortcut '{shortcut}' already exists!")
    return

  tool_name = input("Display Name (e.g., 'XYZ Extractor'): ").strip()
  folder_name = input("Folder Name (e.g., 'xyz_extractor'): ").strip()
  description = input("Short Description: ").strip()

  tool_dir = ROOT_DIR / folder_name

  if tool_dir.exists():
    print(f"Error: Directory '{folder_name}' already exists!")
    return

  # 1. Create directory structure
  (tool_dir / "input").mkdir(parents=True, exist_ok=True)
  (tool_dir / "output").mkdir(parents=True, exist_ok=True)
  (tool_dir / "input" / ".gitkeep").touch()
  (tool_dir / "output" / ".gitkeep").touch()

  # Starter main.py with 2-space indents
  main_py_code = (
    "from pathlib import Path\n\n\n"
    "def main():\n"
    "  root_dir = Path(__file__).parent.resolve()\n"
    "  input_dir = root_dir / \"input\"\n"
    "  output_dir = root_dir / \"output\"\n\n"
    f"  print(\"Running {tool_name}...\")\n\n\n"
    "if __name__ == \"__main__\":\n"
    "  main()\n"
  )
  (tool_dir / "main.py").write_text(main_py_code, encoding="utf-8")

  # Starter tool README.md
  tool_readme = (
    f"# {tool_name}\n\n"
    f"{description}\n\n"
    "## Prerequisites\n\n"
    "- Python 3.8 or higher\n"
    "- `pip` package manager\n\n"
    "## Usage\n\n"
    f"1. Place your target file(s) inside the `{folder_name}/input/` folder.\n"
    "2. Run the script from the project root directory (`python-utility-belt`):\n\n"
    "```bash\n"
    f"python run.py {shortcut}\n"
    "```\n\n"
    "3. Check the console output.\n"
  )
  (tool_dir / "README.md").write_text(tool_readme, encoding="utf-8")

  # Post-setup checklist file
  checklist_content = (
    "====================================================================\n"
    f"POST-SETUP CHECKLIST FOR: {tool_name} ({shortcut})\n"
    "====================================================================\n\n"
    f"[ ] 1. SCRIPT LOGIC\n"
    f"    - Write core tool functionality in: {folder_name}/main.py\n"
    "[ ] 2. DEPENDENCIES (pyproject.toml)\n"
    f"    - Add required packages to pyproject.toml under [project.optional-dependencies]:\n"
    f"      {shortcut} = [\"package-name>=1.0.0\"]\n\n"
    "[ ] 3. MODULE CHECKING (run.py)\n"
    f"    - In run.py, update the 'modules' list for '{shortcut}' in TOOLS dict:\n"
    "      \"modules\": [\"package_import_name\"]\n\n"
    "[ ] 4. TOOL DOCUMENTATION\n"
    f"    - Update {folder_name}/README.md with usage steps and console output examples.\n\n"
    "[ ] 5. ROOT DOCUMENTATION (README.md)\n"
    "    - Update row in root README.md 'Available Tools' table:\n"
    "      * Update Primary Dependencies column (replace 'None' with actual packages)\n"
    "      * Adjust Footprint size if heavy (e.g. Heavy ~500MB+)\n\n"
    "[ ] 6. TESTING & CLEANUP\n"
    f"    - Run 'python run.py {shortcut}' to test execution and auto-dependency prompts.\n"
    "    - Delete this CHECKLIST.txt file when complete!\n"
    "====================================================================\n"
  )
  (tool_dir / "CHECKLIST.txt").write_text(checklist_content, encoding="utf-8")

  # 2. Update pyproject.toml (Unindented, Alphabetical)
  toml_path = ROOT_DIR / "pyproject.toml"
  if toml_path.exists():
    toml_text = toml_path.read_text(encoding="utf-8")
    updated_toml = insert_toml_optional_dep(toml_text, shortcut)
    toml_path.write_text(updated_toml, encoding="utf-8")

  # 3. Update run.py (Alphabetical & Scope-Guarded)
  run_py_path = ROOT_DIR / "run.py"
  if run_py_path.exists():
    run_py_text = run_py_path.read_text(encoding="utf-8")
    updated_run_py = insert_run_py_tool(run_py_text, shortcut, folder_name)
    run_py_path.write_text(updated_run_py, encoding="utf-8")

  # 4. Update Root README.md Table (Clean Alignment)
  root_readme_path = ROOT_DIR / "README.md"
  if root_readme_path.exists():
    readme_text = root_readme_path.read_text(encoding="utf-8")
    updated_readme = insert_readme_table_row(readme_text, shortcut, tool_name, description, folder_name)
    root_readme_path.write_text(updated_readme, encoding="utf-8")

  # Delete root __pycache__ directory if generated
  pycache_dir = ROOT_DIR / "__pycache__"
  if pycache_dir.exists():
    shutil.rmtree(pycache_dir, ignore_errors=True)

  print(f"\n[Success] Created tool scaffold '{tool_name}'!")
  print(f"Location: {folder_name}/")
  print(f"Created: {folder_name}/CHECKLIST.txt")
  print(f"Updated: pyproject.toml, run.py, and root README.md")
  print(f"To run your new tool: python run.py {shortcut}\n")