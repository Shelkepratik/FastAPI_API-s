from fastapi import FastAPI,Path,Query,HTTPException
import json

app=FastAPI()

def show_info():
    with open("student.json","r") as file:
        info=json.load( file)
        return info
    
# GET API 1: View all students
@app.get("/view")
def display_student_info():
    data=show_info()
    return data


#GET API 2:search student by city
@app.get("/view/city/{city}")
def student_by_city(city:str=Path(...)):
    data=show_info()
    result={}

    for student_id,student in data.items():
        """
        data.items() returns both the key and value from the dictionary.
            Variable	Value
            student_id	"S001"
            student	{"name": "Pratik", "city": "Pune"}
        """
        if student["city"].lower()==city.lower():
            result[student_id]=student
            """result["S001"] = {"name": "Pratik", "city": "Pune"}"""
    return result

#GET API 3:search student course
@app.get("/view/course/{course}")
def show_course(course:str=Path(...)):
    data=show_info()
    result={}
    """syntax=for key,value in dictionary_name.items()"""
    for student_id,student in data.items():
        if student["course"].lower()==course.lower():
            result[student_id]=student

    return result


#GET API 4:view student with marks above a value

@app.get("/view/marks")
def view_marks(minimum: int):
    result = {}
    data=show_info()
    for student_id, student in data.items():
        if student["marks"] >= minimum:
            result[student_id] = student

    return result

# GET API 5: View student by ID
@app.get("/view/{student_id}")
def view_student(student_id:str=Path(...,description="student_ID",example="S001")):
    data=show_info()
    if student_id in data:
        return data[student_id]

    raise HTTPException(status_code=404,detail="student not fount")

