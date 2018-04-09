import json

def loadSetupData():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)

    return course["course_setup"]

def loadStudentGrades(st_id):
    try:
        new_file = open('gc_grades.json', 'r+')
        if new_file.readlines() == []:
           new_file.write("{}")
           new_file.close()
    except:
        new_file = open('gc_grades.json', "w")
        new_file.write("{}")
        new_file.close()

    with open('gc_grades.json') as data_file:
        student_grades = json.load(data_file)


    return student_grades

def UserInput():
    st_id = raw_input("Please enter your name. ")
    return st_id

def askForAssignmentMarks(st_id, grades, student_grades):
    current_grades = {st_id : {}}

    for key in grades:
        if st_id in student_grades.keys():
            if student_grades[st_id][key] > -1:
                answer = raw_input("Your grade from " + key + " is " + str(student_grades[st_id][key]) + ". Do you want to change your grade for " + key + "?" + " Please write yes or no.")
            if answer == "yes":
                student_answer = int(raw_input("What is your Current Grade for " + key + "? Please insert -1 if you don't have a grade yet."))
                if (student_answer >= 0 and student_answer <= 100) or (student_answer == -1):
                    current_grades[st_id][key] = student_answer
                else:
                    current_grades[st_id][key] = student_grades[st_id][key]
                    print "You should import a number between 0 and 100."
            elif answer == "no":
                current_grades[st_id][key] = student_grades[st_id][key]
        else:
            student_answer1 = int(raw_input("What is your Current Grade for " + key + "? Please insert -1 if you don't have a grade yet."))
            if (student_answer1 >= 0) and (student_answer1 <= 100) or (student_answer1 == -1):
                current_grades[st_id][key] = student_answer1


    return current_grades

def saveGrades(student_grades, current_grades):
    print (json.dumps(current_grades))
    student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

def printCurrentGrade(st_id, grades,current_grades):
    curr_grade = 0
    for key in current_grades[st_id]:
        if current_grades[st_id][key] != -1:
            calc_grade = float(current_grades[st_id][key]) * grades[key] / 100
            curr_grade = curr_grade + calc_grade

    print float(curr_grade)
    return curr_grade

def printLetterGrade(curr_grade, matrix):
    for i in range(len(matrix)):
        if matrix[i]["min"] <= curr_grade and matrix[i]["max"] >= curr_grade:
            print matrix[i]["mark"]


def main():
    course = loadSetupData()
    grades = course["grade_breakdown"]
    conv_matrix = course["conv_matrix"]
    st_id = UserInput()
    student_grades = loadStudentGrades(st_id)
    current_grades = askForAssignmentMarks(st_id, grades, student_grades)
    saveGrades(student_grades, current_grades)
    curr_grade = printCurrentGrade(st_id, grades, current_grades)
    printLetterGrade(curr_grade, conv_matrix)

main()