Generate the Test Execution Guide content from the provided Test Case document, then insert that content into the existing teg-format.yaml template from the project source files.

Requirements:
- First, use the project’s uploaded/source files with names containing “Test Execution Guide” as the content and style reference.
- Second, use teg-format.yaml as the required output schema.
- The final output must follow teg-format.yaml exactly.
- Do not invent new keys, rename fields, reorder sections, or change the YAML structure unless absolutely necessary to fit missing content.
- Populate each YAML field with the corresponding Test Execution Guide content derived from the Test Case document.
- Keep the content aligned with the project’s existing Test Execution Guide writing style, terminology, and level of detail.
- Ensure the generated content is practical for manual QA execution and reflects the steps, preparation, dependencies, and recording expectations implied by the Test Case document.
- The result must be ready for direct use in the project workflow.
- Output only the final filled-in YAML.
- No explanations. No markdown code fences. No extra text.
- Show in code format.