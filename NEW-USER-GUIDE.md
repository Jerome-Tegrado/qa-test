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
- `input/customize/test-plan.yaml`
- `input/customize/test-case.yaml`

## 3. Customize Format Per User (Before Generation)

Each user can tailor TP/TC outputs to match their own preferred style and structure (font, spacing, size, layout, wording, and defaults).
For TP and TC customization, edit only these two files:
- `input/customize/test-plan.yaml`
- `input/customize/test-case.yaml`
You do not need to edit templates or Python scripts for normal TP/TC personalization.

1. Test Plan customization (DOCX output):
- Edit only `input/customize/test-plan.yaml`.
- `defaults`: default Test Plan content values (title, scope, objectives, approach, schedule, environment, resources, risks, deliverables, entry, exit).
- `style`: font family/sizes, paragraph spacing/alignment, label bolding.
- `layout`: table style/width and table-section spacing behavior.
- `behavior`: intro prefix label and ordered labeled-block mapping (environment/approach labels and aliases).

2. Test Case customization (XLSX output):
- Edit only `input/customize/test-case.yaml`.
- `defaults`: workbook setup (`sheet_name`, `start_row`, `start_column`), column headers/letters/widths, default row values.
- `style`: header/body font, color, fill, alignment, wrap, border.
- `layout`: row heights and page setup/margins.
- `behavior`: generation rules (`freeze_header_row`, `status_dropdown_options`, `blank_rows_when_no_data`).

3. Test Execution Guide:
- Update `input/format/teg-format.yaml` for TEG structure/style mapping.
- If needed, adjust formatting logic in `teg-generate.py`.

## 4. System Workflow (Run in Order)

## Step 1: Generate Test Plan YAML

In Claude/ChatGPT project:
1. Use `prompts/tp/tp-prompt.md`.
2. Provide in the square-bracket field of the prompt:
- Full user story/PBI + acceptance criteria.

3. Execute the prompt using your chosen AI model.
4. Make sure the AI returns the result in a YAML code block format (with a copy button).
5. If the AI already returns YAML in code block format, click copy (or copy the YAML content).
6. If not, ask: "Show me the YAML content in code format."
7. Then copy the YAML content.
8. Paste output into:
- `input/tp/tp.yaml`

9. Generate DOCX:

```bash
python tp-generate.py
```

10. You will see the output in `output/test-plans/`.

## Step 2: Generate Test Case YAML

In Claude/ChatGPT project:
1. Use `prompts/tc/tc-prompt.md`.
2. Provide in the square-bracket field of the prompt:
- Generated Test Plan content
- Full user story/PBI/AC and approved requirements

3. Execute the prompt using your chosen AI model.
4. Make sure the AI returns the result in a YAML code block format (with a copy button).
5. If the AI already returns YAML in code block format, click copy (or copy the YAML content).
6. If not, ask: "Show me the YAML content in code format."
7. Then copy the YAML content.
8. Paste output into:
- `input/tc/tc.yaml`

9. Generate XLSX:

```bash
python tc-generate.py
```

10. You will see the output in `output/test-cases/`.

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
- Require strict output: YAML only in a code block format (no explanation). Use the copy button, then paste only the YAML content into your local `.yaml` file.
- Validate before finalizing documents.

## 6. Output Folder Guide (Local Only, Do Not Push)

Generated files are created in these folders:
- Test Plan (DOCX): `output/test-plans/`
- Test Case (XLSX): `output/test-cases/`
- Test Execution Guide (DOCX): `output/test-execution-guides/`
