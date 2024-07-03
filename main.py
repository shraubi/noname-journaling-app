from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import time
import uvicorn
from threading import Lock

app = FastAPI()
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")
templates = Jinja2Templates(directory="templates")

class Stroke(BaseModel):
    key: str
    text: str

class Editor:
    def __init__(self):
        self.lock = Lock()
        self.text = ""
        self.letter = ""
        self.last_stroke_time = time.time()
        self.blur_threshold = 2  # when start blurring
        self.idle_threshold = 5  # when delete text

    def handle_stroke(self, key: str, text: str):
        with self.lock:
            self.text = text
            self.letter = key
            self.last_stroke_time = time.time()
        return {"text": self.text, "letter": self.letter, "blur": False, "idle": False}

    def check_idle(self):
        with self.lock:
            current_time = time.time()
            time_since_last_stroke = current_time - self.last_stroke_time
            blur = time_since_last_stroke > self.blur_threshold
            idle = time_since_last_stroke > self.idle_threshold
            if idle:
                self.text = "" 
                self.letter = ""
        return {"text": self.text, "letter": self.letter, "blur": blur, "idle": idle}

editor = Editor()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/stroke")
async def stroke(stroke_data: Stroke):
    return editor.handle_stroke(stroke_data.key, stroke_data.text)

@app.get("/check-idle")
async def check_idle():
    return editor.check_idle()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
