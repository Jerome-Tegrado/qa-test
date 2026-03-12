# QA Test Documentation System - User Guide (For New Users)

## 1. Setup

1. Clone the repository.

```bash
git clone https://github.com/Jerome-Tegrado/qa-test.git
cd qa-test
```

2. Install Python dependencies.

```bash
python -m pip install --upgrade pip
pip install pyyaml python-docx openpyxl
```

## 2. Create Your AI Project (Claude or ChatGPT)

1. Choose AI workspace:
- Free option: Claude
- Paid option: ChatGPT Plus

2. Create one project/workspace for this QA system.

3. Upload/add these files as project context:
- All files in the `context/` folder

## 3. Customize Format Per User (Before Generation)

Each user can change TP/TC format style (font, spacing, size, layout, etc.).
You can either make manual code changes or use AI coding agents to help. This is usually easier.

1. Test Plan formatting (DOCX):
- Update style/template structure in `templates/Test-Plan-Template.docx`.
- If needed, update styling logic in `tp-generate.py` (font size, spacing, typography behavior).
- Update generated Test Plan content in `input/tp/tp.yaml` (this is the file consumed by `tp-generate.py`).

2. Test Case formatting (XLSX):
- Update `input/format/tc-format.yaml`
- Typical changes in `input/format/tc-format.yaml` (applied by `tc-generate.py`): columns/headers/width, `header_style`, `body_style`, `row_style`, `page_setup`, and `generation_rules`.
- For Test Case content/instructions, update `input/tc/tc.yaml` (or adjust `prompts/tc/tc-prompt.md`), not `input/format/tc-format.yaml`.

3. Test Execution Guide:
- Update `input/format/teg-format.yaml` for TEG structure/style mapping.
- If needed, adjust formatting logic in `teg-generate.py`.

## 4. System Workflow (Run in Order)

## Step 1: Generate Test Plan YAML

In Claude/ChatGPT project:
1. Use `prompts/tp/tp-prompt.md`.
2. Provide in the square-bracket field of the prompt:
- Full user story/PBI + acceptance criteria.

3. Then execute the prompt using your chosen AI model.

4. Paste output into:
- `input/tp/tp.yaml`

5. Generate DOCX:

```bash
python tp-generate.py
```

6. You will see the output in `output/test-plans/`.

## Step 2: Generate Test Case YAML

In Claude/ChatGPT project:
1. Use `prompts/tc/tc-prompt.md`.
2. Provide in the square-bracket field of the prompt:
- Generated Test Plan content
- Full user story/PBI/AC and approved requirements

3. Execute the prompt using your chosen AI model.

4. Paste output into:
- `input/tc/tc.yaml`

5. Generate XLSX:

```bash
python tc-generate.py
```

6. You will see the output in `output/test-cases/`.

## Step 3: Validate TP and TC

In Claude/ChatGPT project:
1. Use `prompts/validator/tp-tc-validator-prompt.md`.
2. Provide:
- Correct and actual information (the user story/PBI)
- Current Test Plan
- Current Test Case
3. Check result:
- If `ALIGNED WITH THE USER STORY`, proceed.
- If `NOT ALIGNED WITH THE USER STORY`, apply fixes and re-run validation.

## Step 4: Optional - Generate Test Execution Guide

You can produce a manual testing execution guide for each test case set.

Current system generation command:

```bash
python teg-generate.py "output/test-cases/Test Case_<Feature Name>.xlsx"
```

Output:
- `output/test-execution-guides/`

Note: In the current codebase, TEG generation is driven by the generated Test Case Excel input.

## 5. Prompting Best Practice

For every AI generation step:
- Use the corresponding prompt file as the base instruction.
- Attach required source files and input information.
- Require strict output: YAML only (no explanation, no markdown fences).
- Validate before finalizing documents.

## 6. Output Folder Guide (Local Only, Do Not Push)

Generated files are created in these folders:
- Test Plan (DOCX): `output/test-plans/`
- Test Case (XLSX): `output/test-cases/`
- Test Execution Guide (DOCX): `output/test-execution-guides/`
