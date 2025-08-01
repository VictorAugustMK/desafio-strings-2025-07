from fastapi import FastAPI, HTTPException
from app.models.file_request import FileRequest
from app.services.text_processor import process_text_file
from app.config import DEFAULT_WIDTH

app = FastAPI()

@app.post("/line-break")
def line_break(data: FileRequest):
    width = data.width or DEFAULT_WIDTH

    try:
        lines = process_text_file(data.path, width)
        return {"lines": lines}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
