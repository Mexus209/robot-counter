from sqlalchemy.orm import Session
import model

def get_robot(db: Session, id: int):
    robot = db.query(model.Robot).filter(model.Robot.id == id).first()
    if robot is None:
        return None
    return {
        "Robot №": robot.id, 
        "Start time": robot.start_time, 
        "Start number": robot.start_number, 
        "Duration": robot.duration
        }

def get_robots(db: Session, skip: int = 0, limit: int = 100):
    robots = db.query(model.Robot).offset(skip).limit(limit).all()
    if not robots:
        return {"message": "Базы данных роботов не обнаружено"}
    return [{
        "Robot №": robot.id, 
        "Start time": robot.start_time, 
        "Start number": robot.start_number, 
        "Duration": robot.duration
        } for robot in robots]

def create_robot(db: Session, robot: model.Robot):
    db_robot = model.Robot(start_number=robot.start_number, start_time=robot.start_time, duration=robot.duration)
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot