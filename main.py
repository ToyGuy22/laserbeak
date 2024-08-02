from fastapi import FastAPI
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from typing_extensions import Self

# https://www.youtube.com/watch?v=0sOvCWFmrtA
# 1:33:28

TASK_TYPES: list = ["copy", "create"]
all_tasks: list = []


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Task(BaseModel):
    #example job id convention 240802_001 yymmdd_jobNum
    id: str
    date_ran: datetime  = Field(default_factory=datetime_now)
    task_type: str
    description: str 
    success: bool

    @field_validator('task_type')
    def check_task_type(cls, v):
        if v not in TASK_TYPES:
            raise ValueError('Task type is not one of the allowed types.')
        return v
    

app = FastAPI()

# Tasks
@app.post("/tasks/")
async def insert_task(new_task: Task):
    print(new_task.date_ran.strftime("%H:%M:%S"))
    return new_task

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    return {"task_id": task_id}


# # Jobs
# @app.post("/jobs/")
# async def insert_task(new_job: Job):
#     return new_job

# @app.get("/jobs/{job_id}")
# async def get_task(job_id: str):
#     return {"job_id": job_id}