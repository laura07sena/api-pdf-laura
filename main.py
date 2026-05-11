from fastapi import FastAPI
from pydantic import BaseModel
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
from io import BytesIO

app = FastAPI()

class Tabla(BaseModel):
    tabla: str

@app.post("/generar_pdf")
def generar_pdf(data: Tabla):
    tabla = json.loads(data.tabla)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    y = 750
    pdf.setFont("Helvetica", 10)

    for fila in tabla:
        linea = " | ".join([f"{k}: {v}" for k, v in fila.items()])
        pdf.drawString(40, y, linea)
        y -= 20
        if y < 40:
            pdf.showPage()
            y = 750

    pdf.save()

    pdf_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {"pdf": pdf_base64}
