from fastapi import FastAPI, HTTPException
from pathlib import Path
from app.models import FileRequest
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

INPUT_DIR = Path(os.getenv("INPUT_PATH", "/input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", "/output"))


def justify_line(line: str, width: int) -> str:
    words = line.strip().split()
    if len(words) == 1:
        return words[0].ljust(width)
    total_spaces = width - sum(len(word) for word in words)
    gaps = len(words) - 1
    spaces = [total_spaces // gaps + (1 if i < total_spaces % gaps else 0) for i in range(gaps)]

    justified = ''.join(
        word + (' ' * spaces[i] if i < gaps else '') for i, word in enumerate(words)
    )
    return justified


def justify_paragraph(paragraph: str, width: int) -> list[str]:
    words = paragraph.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= width:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(justify_line(current_line, width))
            current_line = word

    if current_line:
        lines.append(current_line.ljust(width))

    return lines


