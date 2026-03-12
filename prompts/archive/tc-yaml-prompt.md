Generate the Test Case content from the provided Test Plan document, then insert that content into the existing tc-format.yaml template from the project source files.

Requirements:
- First, use the project’s uploaded/source files with names containing “Test Case” as the content and style reference.
- Second, use tc-format.yaml as the required output schema.
- The final output must follow tc-format.yaml exactly.
- Do not invent new keys, rename fields, reorder sections, or change the YAML structure unless absolutely necessary to fit missing content.
- Populate each YAML field with the corresponding Test Case content derived from the Test Plan document.
- Keep the content aligned with the project’s existing Test Case writing style, terminology, and level of detail.
- Ensure the generated entries are executable manual test cases and reflect the coverage defined in the Test Plan.
- The result must be ready for direct use in the project workflow.
- Output only the final filled-in YAML.
- No explanations. No markdown code fences. No extra text.
- Show in code format.