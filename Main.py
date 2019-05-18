from getpass import getpass
import os
import platform
from zhixuewang import Zhixuewang
from zhixuewang.exceptions import UserOrPassError
def clear_screen(): 
    os_version = platform.platform()
    if os_version[0] == 'W':
        os.system('cls')
    else:
        os.system('clear')


print('Init finish. Wait for input.')
zxw = None
while zxw == None:
    print('Exec login subprogramme')
    user = input('User Name: ')
    password = getpass()
    try:
        zxw = Zhixuewang(user, password)
    except UserOrPassError as e:
        print('User name or password error.')
print('Login successfully.')

op = 1
exams = None
while op != 2:
    is_vaild_exam_num = False
    choosen_examnum = -1
    while not is_vaild_exam_num:
        clear_screen()
        if exams == None:
            exams = zxw.get_exams()
        for i, exam in enumerate(exams):
            print(f'{i}. {exam.examName}')
        choosen_examnum = int(input('Choosen an exam: '))
        if choosen_examnum < 0 or choosen_examnum >= len(exams):
            print('No such an exam.')
        else:
            is_vaild_exam_num = True

    clear_screen()
    grades = zxw.get_self_grade(exams[choosen_examnum].examId)

    print(f'Self Score Table: {exams[choosen_examnum].examName}')
    print('Name - Score - ClassRank')
    for g in grades:
        print(f'{g.subjectName} - {g.score} - {g.classRank.rank}')
    print('\n')

    print(f'Score Info In Class: {exams[choosen_examnum].examName}')
    print('Name - Avg - Highest - Lowest')
    for g in grades:
        print(f'{g.subjectName} - {g.classRank.avgScore} - {g.classRank.highScore} - {g.classRank.lowScore}')
    print('\n')

    print(f'Score Info In Grade: {exams[choosen_examnum].examName}')
    print('Name - Avg - Highest - Lowest')
    for g in grades:
        print(f'{g.subjectName} - {g.gradeRank.avgScore} - {g.gradeRank.highScore} - {g.gradeRank.lowScore}')
    print('\n')

    op = int(input('Wait for input. 1 to continue, 2 to exit:\n'))