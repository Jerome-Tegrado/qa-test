# QA Test Workflow Semi-Automation

Semi-automated QA workflow for generating:
- Test Plans (`.docx`)
- Test Cases (`.xlsx`)
- Test Execution Guides (`.docx`)

This project uses structured YAML inputs (often generated from AI prompts) and Python scripts to produce formatted QA documents.

## Quick Start

```bash
git clone https://github.com/Jerome-Tegrado/qa-test.git
cd qa-test
python -m pip install --upgrade pip
pip install pyyaml python-docx openpyxl
```

## Generate Documents

1. Generate Test Plan:

```bash
python tp-generate.py
```

2. Generate Test Case:

```bash
python tc-generate.py
```

3. Generate Test Execution Guide (optional):

```bash
python teg-generate.py "output/test-cases/Test Case_<Feature Name>.xlsx"
```

## Inputs and Prompts

- Prompt templates: `prompts/`
- TP/TC customization (edit these): `input/customize/tp-customize.yaml`, `input/customize/tc-customize.yaml`
- Legacy formatting config (backward compatibility): `input/format/`
- Reference context: `context/`

Use the prompt files to produce YAML content, then place YAML into the expected `input/` locations before running generators.

## Output Policy (Local Only)

Generated files are saved under:
- `output/test-plans/`
- `output/test-cases/`
- `output/test-execution-guides/`

These outputs are local artifacts and should not be pushed to GitHub.  
`output/` is already ignored by `.gitignore`.

## User Guide

For full end-to-end instructions, see:
- `NEW-USER-GUIDE.md`
