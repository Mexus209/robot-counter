from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import subprocess
import model
from crud import *
from database import SessionLocal, engine
from datetime import datetime

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    start_time = datetime.now()
    processes["robot"] = {"process": process, "start_time": start_time, "start_number": start_number}
    return {"message": f"Робот запущен с числа {start_number}"}

@app.get("/stop")
async def stop_robot(db: Session = Depends(get_db)):
    if "robot" not in processes:
        print("Робот не запущен.")
        return {"message": "Робот не запущен."}
    
    end_time = datetime.now()
    start_number = processes["robot"]["start_number"]
    start_time = processes["robot"]["start_time"]
    duration = end_time - start_time
    duration = str(duration).split('.')[0]

    robot = model.Robot(start_number=start_number, start_time=str(start_time).split('.')[0], duration=duration)
    create_robot(db, robot)

    processes["robot"]["process"].terminate()
    del processes["robot"]
        
    print("Робот остановлен")
    return {"message": f"Робот остановлен. Время работы: {duration}"}

@app.get("/db")
async def show_robots(db: Session = Depends(get_db)):
    return get_robots(db)

@app.get("/db/{id}")
async def show_robot(db: Session = Depends(get_db), id: int = 0):
    robot = get_robot(db, id)
    if robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot