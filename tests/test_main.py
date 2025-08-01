
import os
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def setup_module(module):
    input_path = Path(os.getenv("INPUT_PATH", "/input"))
    output_path = Path(os.getenv("OUTPUT_PATH", "/output"))
    input_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    test_file = input_path / "test.txt"
    test_file.write_text("Este é um teste de quebra de texto para verificar se a API está funcionando corretamente.")

def teardown_module(module):
    output_path = Path(os.getenv("OUTPUT_PATH", "output"))

    if output_path.exists():
        for file in output_path.iterdir():
            if file.is_file() and file.name.startswith("test.txt"):
                file.unlink()

def test_line_break_endpoint():
    response = client.post("/line-break", json={"path": "test.txt"})
    assert response.status_code == 200
    data = response.json()
    assert "lines" in data
    assert isinstance(data["lines"], list)
    assert all(len(line) <= 40 for line in data["lines"])
