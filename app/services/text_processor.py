from app.config import INPUT_DIR, OUTPUT_DIR
import re

def process_text_file(filename: str, width: int) -> list[str]:
    file_path = INPUT_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError

    text = file_path.read_text(encoding="utf-8")
    text = re.sub(r'\s+', ' ', text)

    paragraphs = text.split("\n\n")
    lines = []

    for paragraph in paragraphs:
        words = paragraph.split()
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + (1 if current_line else 0) <= width:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        lines.append("")

    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    output_file = OUTPUT_DIR / f"{filename}_quebrado.txt"
    output_file.write_text("\n".join(lines), encoding="utf-8")

    return lines



