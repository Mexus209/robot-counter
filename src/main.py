from fastapi import FastAPI, Path
from fastapi.responses import FileResponse
import subprocess

app = FastAPI()

processes = {}

@app.get("/")
async def main():
    return FileResponse("public/index.html")

@app.get("/start")
@app.api_route("/start/{start_number}", methods=["GET", "POST"])
async def start_robot(start_number: int = 0):
    if start_number < 0:
        return {"message": "Стартовое число должно быть больше нуля"}
    if "robot" in processes:
        return {"message": "Робот уже запущен."}
    
    process = subprocess.Popen(["python", "robot.py", str(start_number)])

    processes["robot"] = process
    return {"message": f"Робот запущен с числа {start_number}"}

@app.get("/stop")
async def stop_robot():
    if "robot" not in processes:
        print("Робот не запущен.")
        return {"message": "Робот не запущен."}
    
    processes["robot"].terminate()
    del processes["robot"]
    
    print("Робот остановлен")
    return {"message": "Робот остановлен."}
