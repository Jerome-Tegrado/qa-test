Generate the Test Plan content from the provided user story, then insert that content into the existing tp-format.yaml template from the project source files.

Requirements:
- First, use the project's uploaded/source files with names containing "Test Plan" as the content and style reference.
- Second, use tp-format.yaml as the required output schema.
- The final output must follow tp-format.yaml exactly.
- Do not invent new keys, rename fields, reorder sections, or change the YAML structure unless absolutely necessary to fit missing content.
- Populate each YAML field with the corresponding Test Plan content derived from the user story.
- Keep the content aligned with the project's existing Test Plan writing style, terminology, and level of detail.
- Keep list lengths dynamic where applicable; for `objectives`, include only needed major verification goals and do not force a fixed count.
- Keep list lengths dynamic where applicable; for `risks`, include only the needed risk/mitigation pairs and do not force exactly 3 items.
- Keep `intro`, `scope.in_scope`, and `scope.out_scope` concise and direct.
- Include Playwright only if automation support is needed.
- Default `environment_block` Hardware/Software to `Desktop / Windows 10 / Google Chrome` unless the story requires otherwise.
- Include `Test Data Sources` only when needed by story/test conditions.
- Keep `deliverables` limited to `Test Plan Document` and `Test Cases Document`.
- Keep `entry` and `exit` as compact 1-2 sentence paragraph text, short and direct, not list-style.
- The result must be ready for direct use in the project workflow.
- Output only the final filled-in YAML.
- No explanations. No markdown code fences. No extra text.
