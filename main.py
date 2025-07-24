from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()


# Class that represent the student's structure
class Student(BaseModel):
    reference: str
    first_name: str
    last_name: str
    age: int


# Initialize an empty list to store students
students: List[Student] = []


# GET /hello endpoint
@app.get("/hello")
def home():
    return JSONResponse(content="Hello world", status_code=200)


# GET /welcome endpoint
@app.get("/welcome/")
def welcome(name: str):
    """
        name is a query parameter
    """
    return JSONResponse(content=f"Welcome {name}", status_code=200)


# POST /students endpoint
@app.post("/students")
def create_student(student: Student):
    """
        Create a new student
    """

    if not student or student is None:
        return JSONResponse(
            content="Missing data",
            status_code=400
        )

    elif student in students:
        return JSONResponse(
            content=f"Student with reference {student.reference} already exists",
            status_code=400
        )
    else:
        students.append(student)
        return JSONResponse(
            content=f"Student {student.first_name} {student.last_name} has been added to the list",
            status_code=201
        )

# GET /students endpoint
@app.get("/students")
def get_students():
    """
        Get the list of students
    """

    return JSONResponse(
        content=[student.dict() for student in students], # using list comprehension to convert a student into a dictionary
        status_code=200
    )

# PUT /students endpoint
@app.put("/students")
def update_student(student: Student):
    """
        Update an existing student
    """
    for i, existing_student in enumerate(students):
        if existing_student.reference == student.reference:
            students[i] = student

            return JSONResponse(
                content=f"Student with reference {student.reference} has been updated",
                status_code=200
            )

    students.append(student)

    return JSONResponse(
        content=f"Student {student.first_name} {student.last_name} has been added to the list",
        status_code=201
    )

# GET /students-authorized endpoint

BEARER_HEADER = "bon courage"

@app.get("/students-authorized")
def get_students(request: Request):
    """
        Get the list of students who have authorization
    """

    headers = request.headers

    if not 'Authorization' in headers:
        return JSONResponse(
            content="Unauthorized",
            status_code=401
        )

    elif headers['Authorization'] != BEARER_HEADER:
        return JSONResponse(
            content="You haven't permission to access this resource",
            status_code=403
        )

    return JSONResponse(
        content=[student.dict() for student in students],
        status_code=200
    )



if __name__ == "__main__":
    uvicorn.run(app, port=8000)
