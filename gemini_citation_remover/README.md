# Citation Cleaner

A lightweight Python utility designed to process text (`.txt`) and Word (`.docx`) files and remove bracketed citations or inline reference tags (such as `[1]`, `[note]`, or `[citation]`) while leaving normal text and standard parentheses intact.

## Prerequisites

* Python 3.6 or higher
* `pip` package manager

## Usage

1. **Place your files**: Add any `.txt` or `.docx` files that need cleaning into the `input/` folder.
2. Run the script from the project root directory (`python-utility-belt`):

```bash
python run.py cite
```

3. **Check results**: Open the `output/` folder to view your cleaned files.

## Example

**Input (`input/cover_letter.txt`):**
```text
Dear Hiring Manager [1],
As a Mechanical Engineering student at BYU–Idaho (4.00 GPA), I am eager to apply [note].
```

**Output (`output/cover_letter.txt`):**
```text
Dear Hiring Manager,
As a Mechanical Engineering student at BYU–Idaho (4.00 GPA), I am eager to apply.
```