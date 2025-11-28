from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import uuid
import os

app = FastAPI()

os.makedirs("output", exist_ok=True)

PIPER_MODELS = {
    "id": "voices/indonesian-medium.onnx",
    "en": "voices/english-medium.onnx",
    "jp": "voices/japanese-medium.onnx",
    "es": "voices/spanish-medium.onnx",
    "fr": "voices/french-medium.onnx",
    "de": "voices/german-medium.onnx",
    "ru": "voices/russian-medium.onnx",
    "it": "voices/italian-medium.onnx",
    "pt": "voices/portuguese-medium.onnx",
    "ar": "voices/arabic-medium.onnx",
    "hi": "voices/hindi-medium.onnx",
    "ur": "voices/urdu-medium.onnx",
    "ms": "voices/malay-medium.onnx",
    "zh": "voices/chinese-medium.onnx",
    "mx": "voices/mexican-spanish-medium.onnx",
    "pk": "voices/pakistani-urdu-medium.onnx"
}

@app.post("/tts-advanced")
async def tts_advanced(
    text: str = Form(...),
    voice: str = Form(...)
):
    if voice not in PIPER_MODELS:
        return JSONResponse({"error": "Voice not supported"}, status_code=400)

    model_path = PIPER_MODELS[voice]
    output_wav = f"output/{uuid.uuid4()}.wav"
    output_mp3 = output_wav.replace(".wav", ".mp3")

    cmd = ["piper", "--model", model_path, "--output_file", output_wav]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.communicate(text.encode("utf-8"))

    if not os.path.exists(output_wav):
        return JSONResponse({"error": "TTS failed"}, status_code=500)

    os.system(f"ffmpeg -y -i {output_wav} {output_mp3}")

    if not os.path.exists(output_mp3):
        return JSONResponse({"error": "MP3 conversion failed"}, status_code=500)

    return FileResponse(output_mp3, media_type="audio/mpeg", filename="output.mp3")
