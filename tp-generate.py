import re
from pathlib import Path
from datetime import datetime

import yaml
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx.oxml.ns import qn

BASE = Path(__file__).parent
TEMPLATE = BASE / "templates" / "Test-Plan-Template.docx"
INPUT = BASE / "input" / "tp" / "tp.yaml"
OUTPUT_DIR = BASE / "output"
TP_OUTPUT_DIR = OUTPUT_DIR / "test-plans"


def safe_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:80]


def normalize_text(text: str) -> str:
    """
    For single-paragraph fields only.
    Converts embedded line breaks into spaces.
    """
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\n", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def ensure_prefixed_label(text: str, label: str) -> str:
    normalized_text = normalize_text(text)
    if not label:
        return normalized_text

    if not normalized_text:
        return label

    if normalized_text.lower().startswith(label.lower()):
        return normalized_text

    return f"{label} {normalized_text}"


def normalize_label_key(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (label or "").strip().lower())


def parse_labeled_block(block_text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    if not block_text:
        return parsed

    for raw_line in block_text.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        label, value = line.split(":", 1)
        key = normalize_label_key(label)
        parsed[key] = normalize_text(value)
    return parsed


def ordered_labeled_block(
    source_text: str,
    *,
    target_labels: list[str],
    aliases: dict[str, list[str]],
) -> str:
    parsed = parse_labeled_block(source_text)
    lines: list[str] = []

    for target_label in target_labels:
        target_key = normalize_label_key(target_label)
        candidate_keys = [target_key] + [normalize_label_key(x) for x in aliases.get(target_key, [])]

        value = ""
        for key in candidate_keys:
            if key in parsed and parsed[key]:
                value = parsed[key]
                break

        if value:
            lines.append(f"{target_label} {value}".rstrip())

    return "\n".join(lines)


def clean_run_text(text: str) -> str:
    """
    Cleans text already inside template runs.
    """
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\n", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def set_para_format(
    paragraph,
    *,
    align=WD_ALIGN_PARAGRAPH.LEFT,
    line_spacing=1.15,
    space_before_pt=0,
    space_after_pt=0,
):
    pf = paragraph.paragraph_format
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before_pt)
    pf.space_after = Pt(space_after_pt)
    paragraph.alignment = align


def is_heading_or_title(paragraph) -> bool:
    style_name = paragraph.style.name.lower() if paragraph.style and paragraph.style.name else ""
    text = paragraph.text.strip()

    if not text:
        return False

    if "title" in style_name or "heading" in style_name:
        return True

    if re.match(r"^\d+(\.\d+)*\.?\s+\S+", text):
        return True

    return False


def is_bullet_paragraph(paragraph) -> bool:
    style_name = paragraph.style.name.lower() if paragraph.style and paragraph.style.name else ""
    return "list bullet" in style_name or "bullet" in style_name


def clean_existing_paragraphs(doc: Document):
    for p in doc.paragraphs:
        raw = "".join(run.text for run in p.runs)
        cleaned = clean_run_text(raw)
        if p.runs:
            p.runs[0].text = cleaned
            for run in p.runs[1:]:
                run.text = ""

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    raw = "".join(run.text for run in p.runs)
                    cleaned = clean_run_text(raw)
                    if p.runs:
                        p.runs[0].text = cleaned
                        for run in p.runs[1:]:
                            run.text = ""


def replace_placeholder_preserve_runs(paragraph, mapping: dict[str, str]):
    full_text = "".join(run.text for run in paragraph.runs)
    full_text = clean_run_text(full_text)
    original_text = full_text

    for key, value in mapping.items():
        if key in full_text:
            full_text = full_text.replace(key, normalize_text(value))

    if full_text == original_text:
        return

    if paragraph.runs:
        paragraph.runs[0].text = full_text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(full_text)


def replace_in_doc(doc: Document, mapping: dict[str, str]):
    for p in doc.paragraphs:
        replace_placeholder_preserve_runs(p, mapping)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    replace_placeholder_preserve_runs(p, mapping)


def find_paragraph(doc: Document, needle: str):
    for p in doc.paragraphs:
        if needle in p.text:
            return p
    return None


def bold_leading_label(paragraph, label_text: str):
    text = paragraph.text.strip()
    if not text.startswith(label_text):
        return

    remainder = text[len(label_text):].lstrip()

    for run in paragraph.runs:
        run.text = ""

    if paragraph.runs:
        paragraph.runs[0].text = label_text
        paragraph.runs[0].bold = True
    else:
        r = paragraph.add_run(label_text)
        r.bold = True

    if remainder:
        r2 = paragraph.add_run(" " + remainder)
        r2.bold = False


def apply_label_bolding(doc: Document):
    labels = [
        "Purpose/Executive Summary:",
        "In Scope:",
        "Out of Scope:",
        "Methodologies:",
        "Type of Testing:",
        "Tools Used:",
        "Hardware/Software:",
        "Staging URL or App Version:",
        "Test Data Sources:",
        "Entry Criteria:",
        "Exit Criteria:",
    ]

    for p in doc.paragraphs:
        for label in labels:
            bold_leading_label(p, label)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for label in labels:
                        bold_leading_label(p, label)


def insert_bullets_at_placeholder(paragraph, items: list[str]):
    for item in items:
        p = paragraph.insert_paragraph_before(normalize_text(item))
        p.style = "List Bullet"
        set_para_format(
            p,
            align=WD_ALIGN_PARAGRAPH.LEFT,
            line_spacing=1.15,
            space_before_pt=0,
            space_after_pt=3,
        )

    paragraph.text = ""
    set_para_format(
        paragraph,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.0,
        space_before_pt=0,
        space_after_pt=0,
    )


def bold_table_header_row(table):
    hdr_cells = table.rows[0].cells
    for cell in hdr_cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
            set_para_format(
                p,
                align=WD_ALIGN_PARAGRAPH.LEFT,
                line_spacing=1.0,
                space_before_pt=0,
                space_after_pt=0,
            )


def insert_table_after(paragraph, headers: list[str], rows: list[tuple]):
    paragraph.text = ""
    set_para_format(
        paragraph,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.0,
        space_before_pt=0,
        space_after_pt=0,
    )

    parent = paragraph._parent
    table = parent.add_table(rows=1, cols=len(headers), width=Inches(6.5))
    table.style = "Table Grid"

    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = str(h)

    for r in rows:
        row_cells = table.add_row().cells
        for i, val in enumerate(r):
            row_cells[i].text = "" if val is None else str(val)

    paragraph._element.addnext(table._element)
    bold_table_header_row(table)

    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                set_para_format(
                    p,
                    align=WD_ALIGN_PARAGRAPH.LEFT,
                    line_spacing=1.0,
                    space_before_pt=0,
                    space_after_pt=0,
                )

    return table


def insert_multiline_block_at_placeholder(
    doc: Document,
    placeholder: str,
    block_text: str,
    *,
    justified=False,
    space_after_pt=3,
):
    """
    Replaces one placeholder paragraph with multiple paragraphs,
    one per non-empty line.
    """
    p = find_paragraph(doc, placeholder)
    if not p:
        return

    lines = [line.strip() for line in block_text.splitlines() if line.strip()]

    for line in lines:
        new_p = p.insert_paragraph_before(line)
        set_para_format(
            new_p,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY if justified else WD_ALIGN_PARAGRAPH.LEFT,
            line_spacing=1.15,
            space_before_pt=0,
            space_after_pt=space_after_pt,
        )

    p.text = ""
    set_para_format(
        p,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.0,
        space_before_pt=0,
        space_after_pt=0,
    )


def format_document_spacing(doc: Document):
    """
    Desired layout:
    - Title
      visible space after
    - Section heading
      visible space before
    - If next content is normal paragraph -> small space after heading
    - If next content is a table -> no space after heading
    """
    paragraphs = doc.paragraphs

    table_section_titles = {
        "5. Test Schedule",
        "7. Resources & Responsibilities",
        "8. Risks & Mitigations",
    }

    for p in paragraphs:
        text = p.text.strip()
        style_name = p.style.name.lower() if p.style and p.style.name else ""

        if not text:
            set_para_format(
                p,
                align=WD_ALIGN_PARAGRAPH.LEFT,
                line_spacing=1.0,
                space_before_pt=0,
                space_after_pt=0,
            )
            continue

        if "title" in style_name or text.lower().startswith("test plan:"):
            set_para_format(
                p,
                align=WD_ALIGN_PARAGRAPH.LEFT,
                line_spacing=1.15,
                space_before_pt=0,
                space_after_pt=14,
            )
            continue

        if is_heading_or_title(p):
            heading_space_after = 0 if text in table_section_titles else 6

            set_para_format(
                p,
                align=WD_ALIGN_PARAGRAPH.LEFT,
                line_spacing=1.15,
                space_before_pt=18,
                space_after_pt=heading_space_after,
            )
            continue

        if is_bullet_paragraph(p):
            set_para_format(
                p,
                align=WD_ALIGN_PARAGRAPH.LEFT,
                line_spacing=1.15,
                space_before_pt=0,
                space_after_pt=3,
            )
            continue

        set_para_format(
            p,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY,
            line_spacing=1.15,
            space_before_pt=0,
            space_after_pt=6,
        )

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    set_para_format(
                        p,
                        align=WD_ALIGN_PARAGRAPH.LEFT,
                        line_spacing=1.0,
                        space_before_pt=0,
                        space_after_pt=0,
                    )


def set_run_font(run, font_name="Calibri", font_size_pt: int | None = None):
    run.font.name = font_name
    if font_size_pt is not None:
        run.font.size = Pt(font_size_pt)

    if run._element.rPr is None:
        run._element.get_or_add_rPr()

    run._element.rPr.rFonts.set(qn("w:ascii"), font_name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), font_name)
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    run._element.rPr.rFonts.set(qn("w:cs"), font_name)


def force_document_font(doc: Document, font_name="Calibri"):
    for p in doc.paragraphs:
        for run in p.runs:
            set_run_font(run, font_name)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        set_run_font(run, font_name)


def apply_typography(doc: Document):
    # H1: 14, H2: 12, Body: 11
    for p in doc.paragraphs:
        text = p.text.strip()
        style_name = p.style.name.lower() if p.style and p.style.name else ""

        if "title" in style_name or text.lower().startswith("test plan:"):
            size = 14
        elif is_heading_or_title(p):
            size = 12
        else:
            size = 11

        for run in p.runs:
            set_run_font(run, "Calibri", size)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        set_run_font(run, "Calibri", 11)


def main():
    data = yaml.safe_load(INPUT.read_text(encoding="utf-8"))
    doc = Document(str(TEMPLATE))

    clean_existing_paragraphs(doc)

    intro_with_label = ensure_prefixed_label(
        data.get("intro", ""),
        "Purpose/Executive Summary:",
    )

    mapping = {
        "{{TP_TITLE}}": normalize_text(data.get("tp_title", "")),
        "{{INTRO}}": intro_with_label,
        "{{IN_SCOPE}}": normalize_text(data.get("scope", {}).get("in_scope", "")),
        "{{OUT_SCOPE}}": normalize_text(data.get("scope", {}).get("out_scope", "")),
        "{{ENTRY}}": normalize_text(data.get("entry", "")),
        "{{EXIT}}": normalize_text(data.get("exit", "")),
    }

    replace_in_doc(doc, mapping)

    normalized_environment_block = ordered_labeled_block(
        data.get("environment_block", ""),
        target_labels=[
            "Hardware/Software:",
            "Staging URL or App Version:",
            "Test Data Sources:",
        ],
        aliases={
            "hardwaresoftware": ["hardwareos", "hardwaresoftware"],
            "stagingurlorappversion": ["environmenturlappversion", "stagingurl", "appversion"],
            "testdatasources": ["testdata", "testdatasource", "testdatasources"],
        },
    )

    insert_multiline_block_at_placeholder(
        doc,
        "{{ENVIRONMENT_BLOCK}}",
        normalized_environment_block,
        justified=False,
        space_after_pt=3,
    )

    normalized_approach_block = ordered_labeled_block(
        data.get("approach_block", ""),
        target_labels=[
            "Methodologies:",
            "Type of Testing:",
            "Tools Used:",
        ],
        aliases={
            "methodologies": ["methodology", "methodologies"],
            "typeoftesting": ["typesoftesting", "typeoftesting"],
            "toolsused": ["toolsused"],
        },
    )

    insert_multiline_block_at_placeholder(
        doc,
        "{{APPROACH_BLOCK}}",
        normalized_approach_block,
        justified=False,
        space_after_pt=3,
    )

    p_obj = find_paragraph(doc, "{{OBJECTIVES}}")
    if p_obj:
        insert_bullets_at_placeholder(p_obj, data.get("objectives", []))

    p_del = find_paragraph(doc, "{{DELIVERABLES}}")
    if p_del:
        insert_bullets_at_placeholder(p_del, data.get("deliverables", []))

    p_sched = find_paragraph(doc, "{{TABLE_SCHEDULE}}")
    if p_sched:
        rows = [
            (
                normalize_text(x.get("phase", "")),
                normalize_text(x.get("start", "")),
                normalize_text(x.get("end", "")),
            )
            for x in data.get("schedule", [])
        ]
        insert_table_after(p_sched, ["Phase", "Start Date", "End Date"], rows)

    p_res = find_paragraph(doc, "{{TABLE_RESOURCES}}")
    if p_res:
        rows = [
            (
                normalize_text(x.get("role", "")),
                normalize_text(x.get("name", "")),
                normalize_text(x.get("responsibilities", "")),
            )
            for x in data.get("resources", [])
        ]
        insert_table_after(p_res, ["Role", "Name", "Responsibilities"], rows)

    p_risk = find_paragraph(doc, "{{TABLE_RISKS}}")
    if p_risk:
        rows = [
            (
                normalize_text(x.get("risk", "")),
                normalize_text(x.get("mitigation", "")),
            )
            for x in data.get("risks", [])
        ]
        insert_table_after(p_risk, ["Risk", "Mitigation"], rows)

    apply_label_bolding(doc)
    format_document_spacing(doc)
    force_document_font(doc, "Calibri")
    apply_typography(doc)

    TP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    title = safe_filename(data.get("tp_title", "TestPlan"))
    out_path = TP_OUTPUT_DIR / f"Test Plan_{title}.docx"
    try:
        doc.save(str(out_path))
    except PermissionError:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = TP_OUTPUT_DIR / f"Test Plan_{title}_{ts}.docx"
        doc.save(str(out_path))

    print(f"✅ Generated: {out_path}")


if __name__ == "__main__":
    main()
