import sys
from docx import Document

def extract(path, out):
    doc = Document(path)
    lines = []
    for para in doc.paragraphs:
        t = para.text.rstrip()
        if t:
            lines.append(t)
    for i, tbl in enumerate(doc.tables):
        lines.append(f"\n===== TABLE {i+1} =====")
        for row in tbl.rows:
            cells = [c.text.strip().replace('\n', ' | ') for c in row.cells]
            lines.append(" || ".join(cells))
    with open(out, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"OK wrote {len(lines)} lines to {out}")

extract("Bao_cao_tien_do_2_tuan_TinyML.docx", "_bao_cao_extracted.txt")
