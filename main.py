import sys
import threading
import time
from hashlib import md5
import random

import requests
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
import PyQt5.QtGui
from bs4 import BeautifulSoup
from baiduspider import BaiduSpider
import json


class DataStore:
    @classmethod
    def save_value(cls, name, value):
        text = ''
        with open('data/data.txt', 'r', encoding='utf-8') as f:
            text = f.read()
            if text != '':
                dictObj = json.loads(text)
                dictObj[name] = str(value)
                text = json.dumps(dictObj)
            else:
                dictObj = {name: str(value)}
                text = json.dumps(dictObj)
            f.close()
        with open('data/data.txt', 'w', encoding='utf-8') as f:
            f.write(text)
            f.close()

    @classmethod
    def read_value(cls, name):
        with open('data/data.txt', 'r', encoding='utf-8') as f:
            text = f.read()
            if text != '':
                dictObj = json.loads(text)
                if dict.__contains__(dictObj, name):
                    return dictObj[name]
                else:
                    return None
            else:
                f.close()
                return None

    @classmethod
    def save_history(cls, history_list):
        with open('data/history.txt', 'w+', encoding='utf-8') as f:
            for item in history_list:
                f.write(item + '\n')
            f.close()

    @classmethod
    def read_history(cls):
        result = []
        with open('data/history.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                result.append(line.strip())
            f.close()
        return result


class BaseParser:
    def getContent(self):
        return ''


class QingXiaParser(BaseParser):
    __text = ''

    def __init__(self, text):
        self.__text = text

    def getContent(self):
        soup = BeautifulSoup(self.__text, 'lxml')
        tag = soup.find('div', 'timutext')
        return str(tag)


class ZuJuanParser(BaseParser):
    __text = ''

    def __init__(self, text):
        self.__text = text

    def getContent(self):
        soup = BeautifulSoup(self.__text, 'lxml')
        tag = soup.find('div', 'quest-cnt')
        return str(tag)


class ZaiXianZJParser(BaseParser):
    __text = ''

    def __init__(self, text):
        self.__text = text

    def getContent(self):
        soup = BeautifulSoup(self.__text, 'lxml')
        tag = soup.find('div', 'q-tit')
        return str(tag)


class WordProcessor:
    @classmethod
    def isStrangeWord(cls, wordList, word, level):
        affix = ['s','es','ies','ed']
        dst = ['','','y','']
        for i in range(len(affix)):
            if str.endswith(word, affix[i]):
                word = str.replace(word, affix[i], dst[i])
        index = cls.get_element_number(wordList, word)
        if index != 'no match':
            if index > level:
                return True
            else:
                return False
        else:
            return True

    def get_element_number(a_list, search_term):
        try:
            return a_list.index(search_term)
        except ValueError:
            return 'no match'


# 窗口UI，使用Qt Designer设计，PyUIC生成
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(13)
        self.tabWidget.setFont(font)
        self.tabWidget.setIconSize(QtCore.QSize(40, 40))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.tab_1)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("华文楷体")
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setContentsMargins(5, -1, 5, 15)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.label_trans_result_1 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_trans_result_1.setFont(font)
        self.label_trans_result_1.setObjectName("label_trans_result_1")
        self.verticalLayout_4.addWidget(self.label_trans_result_1)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.loading = QtWidgets.QLabel(self.frame_2)
        self.loading.setEnabled(True)
        self.loading.setMidLineWidth(1)
        self.loading.setText("")
        self.loading.setObjectName("loading")
        self.verticalLayout_4.addWidget(self.loading)
        self.listWidget = QtWidgets.QListWidget(self.frame_2)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_4.addWidget(self.listWidget)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_3 = QtWidgets.QFrame(self.tab_3)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.word_edit = QtWidgets.QLineEdit(self.frame_3)
        self.word_edit.setObjectName("word_edit")
        self.horizontalLayout_2.addWidget(self.word_edit)
        self.search_dict = QtWidgets.QPushButton(self.frame_3)
        self.search_dict.setObjectName("search_dict")
        self.horizontalLayout_2.addWidget(self.search_dict)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_trans_result_2 = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_trans_result_2.sizePolicy().hasHeightForWidth())
        self.label_trans_result_2.setSizePolicy(sizePolicy)
        self.label_trans_result_2.setMaximumSize(QtCore.QSize(16777204, 16777215))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.label_trans_result_2.setFont(font)
        self.label_trans_result_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_trans_result_2.setObjectName("label_trans_result_2")
        self.verticalLayout.addWidget(self.label_trans_result_2)
        self.gridLayout_4.addWidget(self.frame_3, 0, 0, 1, 1, QtCore.Qt.AlignTop)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_4 = QtWidgets.QFrame(self.tab_4)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.history_count = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(10)
        self.history_count.setFont(font)
        self.history_count.setObjectName("history_count")
        self.horizontalLayout_5.addWidget(self.history_count)
        self.clear_history = QtWidgets.QPushButton(self.frame_4)
        self.clear_history.setObjectName("clear_history")
        self.horizontalLayout_5.addWidget(self.clear_history, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.listWidget_2 = QtWidgets.QListWidget(self.frame_4)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_5.addWidget(self.listWidget_2)
        self.gridLayout_5.addWidget(self.frame_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.frame_5 = QtWidgets.QFrame(self.tab_5)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(15, 5, -1, 5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.sort_type_2 = QtWidgets.QRadioButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.sort_type_2.setFont(font)
        self.sort_type_2.setObjectName("sort_type_2")
        self.horizontalLayout_4.addWidget(self.sort_type_2)
        self.sort_type_1 = QtWidgets.QRadioButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.sort_type_1.setFont(font)
        self.sort_type_1.setObjectName("sort_type_1")
        self.horizontalLayout_4.addWidget(self.sort_type_1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.label_5 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(15, -1, -1, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.auto_level = QtWidgets.QRadioButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.auto_level.setFont(font)
        self.auto_level.setAutoExclusive(False)
        self.auto_level.setObjectName("auto_level")
        self.horizontalLayout_6.addWidget(self.auto_level)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.option_level_edit = QtWidgets.QLineEdit(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.option_level_edit.sizePolicy().hasHeightForWidth())
        self.option_level_edit.setSizePolicy(sizePolicy)
        self.option_level_edit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.option_level_edit.setClearButtonEnabled(False)
        self.option_level_edit.setObjectName("option_level_edit")
        self.horizontalLayout_3.addWidget(self.option_level_edit, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.gridLayout_6.addWidget(self.frame_5, 0, 0, 1, 1, QtCore.Qt.AlignTop)
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.pushButton.clicked.connect(MainWindow.loadResult)
        self.search_dict.clicked.connect(MainWindow.loadWord)
        self.listWidget.itemClicked['QListWidgetItem*'].connect(MainWindow.wordListItemClicked)
        self.clear_history.clicked.connect(MainWindow.clearHistory)
        self.sort_type_1.toggled['bool'].connect(MainWindow.optionSortWithLetter)
        self.sort_type_2.toggled['bool'].connect(MainWindow.optionSortWithOrder)
        self.auto_level.toggled['bool'].connect(MainWindow.optionAutoLevel)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "介绍"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "简介"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "在这输入一个短句"))
        self.pushButton.setText(_translate("MainWindow", "搜索"))
        self.label_trans_result_1.setText(_translate("MainWindow", "翻译结果："))
        self.label_3.setText(_translate("MainWindow", "你可能不认识的单词："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "搜题查"))
        self.word_edit.setPlaceholderText(_translate("MainWindow", "在这里输入你想查询的单词"))
        self.search_dict.setText(_translate("MainWindow", "查询"))
        self.label_trans_result_2.setText(_translate("MainWindow", "翻译结果："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "查单词"))
        self.history_count.setText(_translate("MainWindow", "共0条记录"))
        self.clear_history.setText(_translate("MainWindow", "清空"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "历史记录"))
        self.label_4.setText(_translate("MainWindow", "搜索结果排序方式："))
        self.sort_type_2.setText(_translate("MainWindow", "按单词出现次序"))
        self.sort_type_1.setText(_translate("MainWindow", "按单词首字母"))
        self.label_5.setText(_translate("MainWindow", "搜题查："))
        self.auto_level.setText(_translate("MainWindow", "自动推测词汇量级"))
        self.label_2.setText(_translate("MainWindow", "用户词汇量级："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "设置"))


class MyWindow(QMainWindow, Ui_MainWindow):
    __wordList = []
    __keyword = ''
    __history = []
    __level = 0
    __sort_type = 0  # 0为顺序排序，1 为首字母排序
    __auto_level = 0

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("搜题翻译")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.tabWidget.setCurrentIndex(0)
        self.label.setText("作者：Dobando\n介绍："
                           "这是我学完Python后写的第一个项目（2021.5），并且这个作品参加某个Python"
                           "编程比赛成功进入了决赛XD（2021.7）"
                           "现在把它开源了。\n"
                           "我使用BaiduSpider百度爬虫库和百度翻译api成功将搜题和翻译结合了起来"
                           "我们只需要通过一个短句即可自动匹配出用户正在做的试题(主要是针对英语试题，阅读完型等)，"
                           "并推测出用户可能会查询的单词。\n")
        self.on_created()

    # 初始化程序
    def on_created(self):
        # 加载词频表和历史记录
        initThread = InitThread(callback=self.word_table_loaded)
        initThread.start()

        self.loading.setVisible(False)
        # 读取数据
        level_value = DataStore.read_value('level')
        sort_type = DataStore.read_value('sort_type')
        auto_level = DataStore.read_value('auto_level')
        self.__level = int(5000 if level_value is None else level_value)
        self.__sort_type = int(0 if sort_type is None else sort_type)
        self.__auto_level = int(0 if auto_level is None else auto_level)
        self.option_level_edit.setText(level_value)
        if self.__sort_type == 0:
            self.sort_type_2.setChecked(True)
        elif self.__sort_type == 1:
            self.sort_type_1.setChecked(True)
        if self.__auto_level == 0:
            self.auto_level.setChecked(True)
            self.option_level_edit.setEnabled(False)

    # 窗口关闭事件
    def closeEvent(self, a0: QtGui.QCloseEvent):
        # 保存数据
        DataStore.save_value('level', self.__level)
        DataStore.save_value('sort_type', self.__sort_type)
        DataStore.save_value('auto_level', self.__auto_level)
        DataStore.save_history(self.__history)

    # 词频表加载成功
    def word_table_loaded(self, mlist, historyList):
        self.__wordList = mlist
        self.__history = historyList
        self.listWidget_2.addItems(self.__history)
        self.history_count.setText("共{}条记录".format(len(self.__history)))
        # 自动生成词汇量级
        if self.__auto_level == 0:
            length = len(historyList)
            min_index = 10000
            step = int(length / 5)
            if length == 0:
                return
            if length < 5:
                step = 1
            for i in range(0, length, step):
                try:
                    cur_index = list.index(mlist, historyList[i])
                except ValueError:
                    cur_index = 10000
                if cur_index < min_index:
                    min_index = cur_index
            self.__level = min_index
            self.option_level_edit.setText(str(min_index))

    # 解析爬取内容
    def parse_all_content(self, contentArr):
        formattedArr = []
        if len(contentArr) == 0:
            self.listWidget.addItem("匹配失败")
            self.listWidget.setVisible(True)
            self.loading.setVisible(False)
            return
        contentArr = self.content_filter(contentArr)
        for item in contentArr:
            # 排除符号干扰
            old_char = [',', '.', '(', ')','_','?','!','\"']
            new_char = [' , ', ' . ', ' ( ', ' ) ',' _ ',' ? ',' ! ',' \" ']
            for i in range(len(old_char)):
                item = str.replace(item, old_char[i], new_char[i])
            # 排除html元素名
            matchObj = re.findall(r'<(.+?)>', item)
            if matchObj is not None:
                for field in matchObj:
                    item = item.replace('<'+field+'>', " ")

            matchObj = re.findall(r'[a-zA-Z]+', item)
            if matchObj is not None:
                for word in matchObj:
                    lowerWord = str.lower(word)
                    if len(word) > 3 and WordProcessor.isStrangeWord(self.__wordList, lowerWord, self.__level):
                        formattedArr.append(lowerWord)
        formattedArr = list(set(formattedArr))  # 去重
        if self.__sort_type == 1:
            formattedArr.sort()
        for item in formattedArr:
            self.listWidget.addItem(item)
        self.listWidget.setVisible(True)
        self.loading.setVisible(False)

    # 过滤内容，从搜索结果匹配到最精准的文章
    def content_filter(self, contentArr):
        length = len(contentArr)
        max_weight = 0
        cur_index = 0
        list_a = self.__keyword.split(' ')
        for i in range(length):
            cur_weight = 0
            list_b = str.split(contentArr[i], ' ')
            for j in range(len(list_a) - 1):
                try:
                    if list_b.index(list_a[j + 1]) - list_b.index(list_a[j]) == 1:
                        cur_weight += 1
                except ValueError:
                    cur_weight += 0
            if cur_weight > max_weight:
                max_weight = cur_weight
                cur_index = i
        return [contentArr[cur_index]]

    # 搜索
    def loadResult(self):
        self.__keyword = self.lineEdit.text()
        if len(self.__keyword) < 10:
            QMessageBox.warning(self, "警告", "不符合搜索要求", QMessageBox.No)
        else:
            searchThread = SearchThread(key=self.__keyword, callback=self.parse_all_content)
            searchThread.start()
            self.listWidget.clear()
            self.listWidget.setVisible(False)
            self.loading.setVisible(True)
            load_anim = PyQt5.QtGui.QMovie('images/加载中.gif')
            self.loading.setMovie(load_anim)
            load_anim.start()
        return

    # 单词列表被点击
    def wordListItemClicked(self):
        item = self.listWidget.selectedItems()[0]
        trans_thread = TranslateThread(item.text(), self.translate_ok, 0)
        trans_thread.start()
        # 添加到历史记录
        list.append(self.__history, item.text())
        self.listWidget_2.addItem(item.text())
        self.history_count.setText("共{}条记录".format(len(self.__history)))

    # 翻译完成回调
    def translate_ok(self, result, type):
        if type == 0:
            self.label_trans_result_1.setText('翻译结果：' + result)
        elif type == 1:
            self.label_trans_result_2.setText('翻译结果：' + result)

    # 加载记录单词
    def loadWord(self):
        dst_word = self.word_edit.text()
        trans_thread = TranslateThread(dst_word, self.translate_ok, 1)
        trans_thread.start()
        # 添加到历史记录
        list.append(self.__history, self.word_edit.text())
        self.listWidget_2.addItem(self.word_edit.text())
        self.history_count.setText("共{}条记录".format(len(self.__history)))

    # 清空历史记录
    def clearHistory(self):
        self.__history = []
        self.listWidget_2.clear()
        self.history_count.setText("共{}条记录".format(len(self.__history)))

    def optionSortWithLetter(self):
        if self.sort_type_1.isChecked():
            self.__sort_type = 1
        return

    def optionSortWithOrder(self):
        if self.sort_type_2.isChecked():
            self.__sort_type = 0
        return

    def optionAutoLevel(self):
        if self.auto_level.isChecked():
            self.__auto_level = 0
            self.option_level_edit.setEnabled(False)
        else:
            self.__auto_level = 1
            self.option_level_edit.setEnabled(True)
        return

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if str(a0.key()) == '16777220': # 按下回车
            if self.option_level_edit.hasFocus():
                self.__level = int(self.option_level_edit.text())
                self.option_level_edit.clearFocus()


class SearchThread(threading.Thread):
    __key = ""
    __contentArr = []  # 文章内容
    __callback = None
    spider = BaiduSpider()
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.181 Safari/537.36'}

    def __init__(self, key, callback):
        threading.Thread.__init__(self)
        self.__key = key
        self.__callback = callback

    def run(self):
        # 从‘青夏教育’爬取文章
        itemArr = (self.spider.search_web(
            query=self.__key + " site:www.1010jiajiao.com",
            exclude=["all"]))['results']
        urlArr = []
        for item in itemArr:
            if "url" in item:
                urlArr.append(item['url'])
        length = len(urlArr)
        for i in range(3 if length > 4 else length):
            resp = requests.get(urlArr[i], headers=self.header)
            parser = QingXiaParser(resp.text)
            content = parser.getContent()
            if content != "None":
                self.__contentArr.append(content)
            time.sleep(0.2)

        # 从‘组卷网’爬取文章
        itemArr = (self.spider.search_web(
            query=self.__key + " site:zujuan.xkw.com",
            exclude=["all"]))['results']
        urlArr = []
        for item in itemArr:
            if "url" in item:
                urlArr.append(item['url'])
        length = len(urlArr)
        for i in range(3 if length > 4 else length):
            resp = requests.get(urlArr[i], headers=self.header)
            parser = ZuJuanParser(resp.text)
            content = parser.getContent()
            if content != "None":
                self.__contentArr.append(content)
            time.sleep(0.2)

        # 从‘在线组卷’爬取文章
        itemArr = (self.spider.search_web(
            query=self.__key + " site:www.zujuan.com",
            exclude=["all"]))['results']
        urlArr = []
        for item in itemArr:
            if "url" in item:
                urlArr.append(item['url'])
        length = len(urlArr)
        for i in range(3 if length > 4 else length):
            resp = requests.get(urlArr[i], headers=self.header)
            parser = ZaiXianZJParser(resp.text)
            content = parser.getContent()
            if content != "None":
                self.__contentArr.append(content)
            time.sleep(0.2)

        # 搜索完成回调
        self.__callback(self.__contentArr)


class TranslateThread(threading.Thread):
    # 百度翻译api对接设置
    __app_id = '20190309000275453'
    __app_key = 'unIX1yBJczZXLgwoRYvc'
    __callback = None
    __query = ''
    __type = 0

    def __init__(self, query, callback, type):
        threading.Thread.__init__(self)
        self.__query = query
        self.__callback = callback
        self.__type = type

    def run(self):
        self.__callback(self.translate_word(self.__query), self.__type)

    def translate_word(self, query):
        # 与百度翻译api对接
        from_lang = 'en'
        to_lang = 'zh'
        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.__app_id + query + str(salt) + self.__app_key)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        post_data = {'appid': self.__app_id, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
        result = requests.post(url, params=post_data, headers=headers).json()
        if 'trans_result' in result:
            return result['trans_result'][0]['dst']
        else:
            return ''

    # md5加密处理数据
    def make_md5(self, encoding='utf-8'):
        return md5(str.encode(encoding)).hexdigest()


class InitThread(threading.Thread):
    __callback = None

    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.__callback = callback

    def run(self):
        wordArr = []
        file = open("assets/词频表.txt", "r")
        for line in file.readlines():
            line = line.strip('\n').strip();
            wordArr.append(line)
        self.__callback(wordArr, DataStore.read_history())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
    QDialogButtonBox {
        dialogbuttonbox-buttons-have-icons: 1;
        dialog-no-icon: url(images/关闭.png);
    }
    QMessageBox {
        messagebox-warning-icon: url(images/提示.png);
    }''')
    myWin = MyWindow()
    tabWidget = myWin.tabWidget
    tabWidget.setTabIcon(0, QIcon('images/首页.png'))
    tabWidget.setTabIcon(1, QIcon('images/搜索.png'))
    tabWidget.setTabIcon(2, QIcon('images/词典.png'))
    tabWidget.setTabIcon(3, QIcon('images/记录.png'))
    tabWidget.setTabIcon(4, QIcon('images/设置.png'))
    myWin.show()
    sys.exit(app.exec_())
