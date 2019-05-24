# coding=utf-8
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, \
    QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from zhixuewang import Zhixuewang
from zhixuewang.exceptions import UserOrPassError
import sys

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.userLabel = QLabel("考号")
        self.userEdit = QLineEdit()
        self.passLabel = QLabel("密码")
        self.passEdit = QLineEdit()
        self.passEdit.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("登录")
        self.loginButton.clicked.connect(self.atLogin)
        self.loginErrLabel = QLabel("考号或密码错误")
        self.loginErrLabel.hide()

        self.loginLayout = QGridLayout()
        self.loginLayout.addWidget(self.userLabel, 1, 0)
        self.loginLayout.addWidget(self.userEdit, 1, 1)
        self.loginLayout.addWidget(self.passLabel, 2, 0)
        self.loginLayout.addWidget(self.passEdit, 2, 1)
        self.loginLayout.addWidget(self.loginButton, 3, 0)
        self.loginLayout.addWidget(self.loginErrLabel, 3, 1)

        self.authorInfo = QLabel("Origami404 @ github")
        self.githubUrl = QLabel("https://github.com/Origami404/CommandZhixue")
        self.sign = QLabel("考试快乐~ QwQ")

        self.infoLayout = QGridLayout()
        self.infoLayout.addWidget(self.authorInfo, 1, 0)
        self.infoLayout.addWidget(self.githubUrl, 2, 0)
        self.infoLayout.addWidget(self.sign, 3, 0)

        self.examLabel = QLabel("考试列表")
        self.examTable = QTableWidget(self)
        self.examTable.setColumnCount(1)
        self.examTable.setHorizontalHeaderLabels(['名称'])
        self.examTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.examTable.cellActivated.connect(self.atActivatedExam)
        self.examTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.scoreLabel = QLabel("自己成绩")
        self.scoreTable = QTableWidget(self)
        self.scoreTable.setColumnCount(3)
        self.scoreTable.setHorizontalHeaderLabels(['科目', '分数', '班级排名'])
        self.scoreTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.scoreTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.classScoreLabel = QLabel("本班成绩")
        self.classScoreInfoTable = QTableWidget(self)
        self.classScoreInfoTable.setColumnCount(4)
        self.classScoreInfoTable.setHorizontalHeaderLabels(['科目', '平均分', '最高分', '最低分'])
        self.classScoreInfoTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.classScoreInfoTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.gradeScoreInfoLabel = QLabel("全级成绩")
        self.gradeScoreInfoTable = QTableWidget(self)
        self.gradeScoreInfoTable.setColumnCount(4)
        self.gradeScoreInfoTable.setHorizontalHeaderLabels(['科目', '平均分', '最高分', '最低分'])
        self.gradeScoreInfoTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.gradeScoreInfoTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.guiLayout = QGridLayout()
        self.guiLayout.addLayout(self.loginLayout, 0, 0)
        self.guiLayout.addLayout(self.infoLayout, 0, 1)
        self.guiLayout.addWidget(self.examLabel, 1, 0)
        self.guiLayout.addWidget(self.examTable, 2, 0)
        self.guiLayout.addWidget(self.scoreLabel, 1, 1)
        self.guiLayout.addWidget(self.scoreTable, 2, 1)
        self.guiLayout.addWidget(self.classScoreLabel, 3, 0)
        self.guiLayout.addWidget(self.classScoreInfoTable, 4, 0)
        self.guiLayout.addWidget(self.gradeScoreInfoLabel, 3, 1)
        self.guiLayout.addWidget(self.gradeScoreInfoTable, 4, 1)
        self.setLayout(self.guiLayout)

        self.setStyleSheet('''
            QLabel {
                font-size: 12px;
                font-family: 微软雅黑;
            }
        ''')


    def atLogin(self):
        user = self.userEdit.text()
        password = self.passEdit.text()
        try:
            self.zxw = Zhixuewang(user, password)
        except UserOrPassError as e:
            self.loginErrLabel.show()
        else:
            self.loginErrLabel.hide()
            self.initExamList()
    

    def initExamList(self):
        self.examList = self.zxw.get_exams()
        self.examTable.setRowCount(len(self.examList))
        for i, exam in enumerate(self.examList):
            self.examTable.setItem(i, 0, QTableWidgetItem(str(exam.examName)))


    def atActivatedExam(self, row, column):
        subject = self.zxw.get_self_grade(self.examList[row].examId)
        self.scoreTable.setRowCount(len(subject))
        self.classScoreInfoTable.setRowCount(len(subject))
        self.gradeScoreInfoTable.setRowCount(len(subject))
        for (i, score) in enumerate(subject):
            self.scoreTable.setItem(i, 0, QTableWidgetItem(score.subjectName))
            self.scoreTable.setItem(i, 1, QTableWidgetItem(str(score.score)))
            self.scoreTable.setItem(i, 2, QTableWidgetItem(str(score.classRank.rank)))

            self.classScoreInfoTable.setItem(i, 0, QTableWidgetItem(score.subjectName))
            self.classScoreInfoTable.setItem(i, 1, QTableWidgetItem(str(score.classRank.avgScore)))
            self.classScoreInfoTable.setItem(i, 2, QTableWidgetItem(str(score.classRank.highScore)))
            self.classScoreInfoTable.setItem(i, 3, QTableWidgetItem(str(score.classRank.lowScore)))

            self.gradeScoreInfoTable.setItem(i, 0, QTableWidgetItem(score.subjectName))
            self.gradeScoreInfoTable.setItem(i, 1, QTableWidgetItem(str(score.gradeRank.avgScore)))
            self.gradeScoreInfoTable.setItem(i, 2, QTableWidgetItem(str(score.gradeRank.highScore)))
            self.gradeScoreInfoTable.setItem(i, 3, QTableWidgetItem(str(score.gradeRank.lowScore)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainGUI()
    w.show()
    sys.exit(app.exec_())