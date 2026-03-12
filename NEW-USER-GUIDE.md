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
- If you want default information to appear immediately in every generated Test Plan, set it in `input/format/tp-format.yaml`.
- Test Plan content fields you can set in `input/format/tp-format.yaml`: `tp_title`, `intro`, `scope.in_scope`, `scope.out_scope`, `objectives[]`, `approach_block`, `schedule[]` (`phase`, `start`, `end`), `environment_block`, `resources[]` (`role`, `name`, `responsibilities`), `risks[]` (`risk`, `mitigation`), `deliverables[]`, `entry`, and `exit`.
- For Test Plan styling, update `tp-generate.py`.
- Common style controls in `tp-generate.py`: paragraph alignment/line spacing/spacing-before/spacing-after, bullet formatting, table formatting (`Table Grid`, headers, widths), heading/body font sizing, default font family, label bolding (for fields like Purpose, In Scope, Out of Scope, Methodologies, Type of Testing, Tools Used, Environment, Entry, and Exit), and section spacing rules.

2. Test Case formatting (XLSX):
- Update `input/format/tc-format.yaml` for all Test Case Excel formatting customization.
- Column setup: `columns` (`key`, `header`, `column`, `width`).
- Header style: `header_style` (`font_name`, `font_size`, `bold`, `font_color`, `fill_color`, `horizontal_alignment`, `vertical_alignment`, `wrap_text`).
- Body style: `body_style` (`font_name`, `font_size`, `bold`, `font_color`, `horizontal_alignment`, `vertical_alignment`, `wrap_text`, `border.style`, `border.color`).
- Row sizing: `row_style` (`header_height`, `body_height`).
- Page layout: `page_setup` (`orientation`, `fit_to_width`, `fit_to_height`, `margins.left/right/top/bottom/header/footer`).
- Generation behavior: `generation_rules` (`freeze_header_row`, `status_dropdown_options`, `blank_rows_when_no_data`) and `workbook` (`sheet_name`, `start_row`, `start_column`).

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
