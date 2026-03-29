#!/usr/bin/env python3
"""
灵活用工管理平台 - 完整功能版
包含数据持久化和所有业务逻辑
"""
import streamlit as st
import sys
import json
import os
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QTableWidget, QTableWidgetItem,
    QProgressBar, QMessageBox, QTabWidget, QLineEdit, QDateEdit,
    QComboBox, QSpinBox, QGroupBox, QFormLayout, QListWidget,
    QListWidgetItem, QSplitter, QHeaderView, QDialog, QDialogButtonBox,
    QCalendarWidget, QFileDialog, QInputDialog, QMenu, QSystemTrayIcon
)
from PyQt6.QtCore import Qt, QTimer, QDate, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QAction, QIcon
import random

st.set_page_config(
    page_title="FlexWork - 灵活用工智能管理平台",
    page_icon="💼",
    layout="wide"
)

class DataManager:
    """数据管理器 - 负责所有数据的保存和加载"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 数据文件路径
        self.jobs_file = os.path.join(data_dir, "jobs.json")
        self.candidates_file = os.path.join(data_dir, "candidates.json")
        self.contracts_file = os.path.join(data_dir, "contracts.json")
        
        # 初始化数据
        self.jobs = self.load_json(self.jobs_file, self.default_jobs())
        self.candidates = self.load_json(self.candidates_file, self.default_candidates())
        self.contracts = self.load_json(self.contracts_file, self.default_contracts())
    
    def load_json(self, filepath, default_data):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return default_data
    
    def save_json(self, filepath, data):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    def save_all(self):
        """保存所有数据"""
        self.save_json(self.jobs_file, self.jobs)
        self.save_json(self.candidates_file, self.candidates)
        self.save_json(self.contracts_file, self.contracts)
    
    def default_jobs(self):
        """默认职位数据"""
        return [
            {
                "id": "job_001",
                "title": "前端开发工程师",
                "salary": "300-500元/天",
                "location": "远程",
                "status": "招聘中",
                "description": "负责Web前端开发，要求React/Vue经验",
                "requirements": "3年以上经验，精通JavaScript",
                "created": "2024-01-01",
                "applicants": 12
            }
        ]
    
    def default_candidates(self):
        """默认候选人数据"""
        return [
            {
                "id": "cand_001",
                "name": "张三",
                "skills": ["Python", "React", "JavaScript"],
                "experience": 3,
                "expected_salary": 400,
                "location": "上海",
                "status": "可联系",
                "phone": "13800138000",
                "email": "zhangsan@example.com",
                "availability": "周一至周五"
            }
        ]
    
    def default_contracts(self):
        """默认合同数据"""
        return [
            {
                "id": "contract_001",
                "job_id": "job_001",
                "candidate_id": "cand_001",
                "start_date": "2024-01-15",
                "end_date": "2024-06-15",
                "salary": 450,
                "status": "执行中",
                "work_hours": "每周40小时",
                "payment_method": "月结"
            }
        ]
    
    def add_job(self, job_data):
        """添加新职位"""
        job_data["id"] = f"job_{len(self.jobs) + 1:03d}"
        job_data["created"] = datetime.now().strftime("%Y-%m-%d")
        job_data["applicants"] = 0
        self.jobs.append(job_data)
        self.save_json(self.jobs_file, self.jobs)
        return job_data["id"]
    
    def add_candidate(self, candidate_data):
        """添加新候选人"""
        candidate_data["id"] = f"cand_{len(self.candidates) + 1:03d}"
        self.candidates.append(candidate_data)
        self.save_json(self.candidates_file, self.candidates)
        return candidate_data["id"]
    
    def add_contract(self, contract_data):
        """添加新合同"""
        contract_data["id"] = f"contract_{len(self.contracts) + 1:03d}"
        self.contracts.append(contract_data)
        self.save_json(self.contracts_file, self.contracts)
        return contract_data["id"]


class JobDialog(QDialog):
    """职位发布对话框 - 完整功能"""
    
    def __init__(self, parent=None, job_data=None):
        super().__init__(parent)
        self.job_data = job_data or {}
        self.is_edit = bool(job_data)
        
        title = "编辑职位" if self.is_edit else "发布新职位"
        self.setWindowTitle(title)
        self.setFixedSize(600, 600)
        
        self.init_ui()
        if self.is_edit:
            self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 表单
        form_layout = QFormLayout()
        
        # 职位标题
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("例如：前端开发工程师（远程兼职）")
        form_layout.addRow("职位标题*:", self.title_input)
        
        # 职位描述
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        form_layout.addRow("职位描述:", self.desc_input)
        
        # 技能要求
        self.skills_input = QLineEdit()
        self.skills_input.setPlaceholderText("用逗号分隔，例如：Python, React, Vue")
        form_layout.addRow("技能要求*:", self.skills_input)
        
        # 工作经验
        self.exp_combo = QComboBox()
        self.exp_combo.addItems(["不限", "1年以下", "1-3年", "3-5年", "5年以上"])
        form_layout.addRow("工作经验:", self.exp_combo)
        
        # 薪资范围
        salary_layout = QHBoxLayout()
        self.salary_min = QSpinBox()
        self.salary_min.setRange(0, 10000)
        self.salary_min.setValue(200)
        self.salary_min.setSuffix("元/天")
        
        self.salary_max = QSpinBox()
        self.salary_max.setRange(0, 10000)
        self.salary_max.setValue(500)
        self.salary_max.setSuffix("元/天")
        
        salary_layout.addWidget(self.salary_min)
        salary_layout.addWidget(QLabel("到"))
        salary_layout.addWidget(self.salary_max)
        salary_layout.addStretch()
        form_layout.addRow("薪资范围*:", salary_layout)
        
        # 工作地点
        self.location_combo = QComboBox()
        self.location_combo.addItems(["远程", "上海", "北京", "深圳", "杭州", "广州", "成都", "其他"])
        form_layout.addRow("工作地点:", self.location_combo)
        
        # 工作类型
        self.type_combo = QComboBox()
        self.type_combo.addItems(["全职", "兼职", "实习", "项目制"])
        form_layout.addRow("工作类型:", self.type_combo)
        
        # 紧急程度
        self.urgency_combo = QComboBox()
        self.urgency_combo.addItems(["普通", "紧急", "特急"])
        form_layout.addRow("紧急程度:", self.urgency_combo)
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_data(self):
        """加载现有数据"""
        if self.job_data:
            self.title_input.setText(self.job_data.get("title", ""))
            self.desc_input.setText(self.job_data.get("description", ""))
            self.skills_input.setText(", ".join(self.job_data.get("skills", [])))
            
            # 解析薪资范围
            salary = self.job_data.get("salary", "200-500元/天")
            if "-" in salary:
                min_salary, max_salary = salary.split("-")[:2]
                self.salary_min.setValue(int(min_salary))
                self.salary_max.setValue(int(max_salary.replace("元/天", "")))
    
    def validate_and_accept(self):
        """验证并接受表单"""
        title = self.title_input.text().strip()
        skills = self.skills_input.text().strip()
        
        if not title:
            QMessageBox.warning(self, "输入错误", "职位标题不能为空！")
            return
        
        if not skills:
            QMessageBox.warning(self, "输入错误", "技能要求不能为空！")
            return
        
        if self.salary_min.value() > self.salary_max.value():
            QMessageBox.warning(self, "输入错误", "最低薪资不能高于最高薪资！")
            return
        
        self.accept()
    
    def get_data(self):
        """获取表单数据"""
        return {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "skills": [s.strip() for s in self.skills_input.text().split(",") if s.strip()],
            "experience": self.exp_combo.currentText(),
            "salary": f"{self.salary_min.value()}-{self.salary_max.value()}元/天",
            "location": self.location_combo.currentText(),
            "job_type": self.type_combo.currentText(),
            "urgency": self.urgency_combo.currentText(),
            "status": "招聘中"
        }


class ContractDialog(QDialog):
    """合同创建对话框"""
    
    def __init__(self, parent=None, jobs=None, candidates=None, contract_data=None):
        super().__init__(parent)
        self.jobs = jobs or []
        self.candidates = candidates or []
        self.contract_data = contract_data or {}
        self.setWindowTitle("新建合同" if not contract_data else "编辑合同")
        self.setFixedSize(600, 420)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # 职位下拉
        self.job_combo = QComboBox()
        for job in self.jobs:
            self.job_combo.addItem(f"{job.get('title','未知')} - {job.get('location','')}", job.get('id'))
        form_layout.addRow("职位*:", self.job_combo)

        # 候选人下拉
        self.candidate_combo = QComboBox()
        for candidate in self.candidates:
            skill_preview = ", ".join(candidate.get("skills", [])[:2])
            self.candidate_combo.addItem(f"{candidate.get('name','未知')} - {skill_preview}", candidate.get("id"))
        form_layout.addRow("候选人*:", self.candidate_combo)

        # 开始日期
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        form_layout.addRow("开始日期*:", self.start_date)

        # 结束日期
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate().addMonths(3))
        form_layout.addRow("结束日期*:", self.end_date)

        # 薪资
        self.salary_input = QSpinBox()
        self.salary_input.setRange(0, 10000)
        self.salary_input.setValue(400)
        self.salary_input.setSuffix("元/天")
        form_layout.addRow("约定薪资*:", self.salary_input)

        # 工作内容
        self.work_content = QTextEdit()
        self.work_content.setMaximumHeight(80)
        form_layout.addRow("工作内容:", self.work_content)

        # 付款方式
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["月结", "周结", "项目结", "完成结"])
        form_layout.addRow("付款方式:", self.payment_combo)

        # 合同状态
        self.status_combo = QComboBox()
        self.status_combo.addItems(["待签署", "执行中", "已完成", "已终止"])
        form_layout.addRow("合同状态:", self.status_combo)

        layout.addLayout(form_layout)

        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        if self.contract_data:
            self.load_data()

    def load_data(self):
        data = self.contract_data
        # 选择职位
        job_id = data.get("job_id")
        if job_id:
            idx = next((i for i, j in enumerate(self.jobs) if j.get("id") == job_id), 0)
            self.job_combo.setCurrentIndex(idx)
        # 选择候选人
        cand_id = data.get("candidate_id")
        if cand_id:
            idx = next((i for i, c in enumerate(self.candidates) if c.get("id") == cand_id), 0)
            self.candidate_combo.setCurrentIndex(idx)
        # 日期和其他字段
        try:
            if data.get("start_date"):
                self.start_date.setDate(QDate.fromString(data.get("start_date"), "yyyy-MM-dd"))
            if data.get("end_date"):
                self.end_date.setDate(QDate.fromString(data.get("end_date"), "yyyy-MM-dd"))
        except:
            pass
        try:
            self.salary_input.setValue(int(data.get("salary", self.salary_input.value())))
        except:
            pass
        self.work_content.setPlainText(data.get("work_content", ""))
        self.payment_combo.setCurrentText(data.get("payment_method", self.payment_combo.currentText()))
        self.status_combo.setCurrentText(data.get("status", self.status_combo.currentText()))

    def validate_and_accept(self):
        if self.start_date.date() > self.end_date.date():
            QMessageBox.warning(self, "输入错误", "开始日期不能晚于结束日期！")
            return
        if self.salary_input.value() <= 0:
            QMessageBox.warning(self, "输入错误", "薪资必须大于0！")
            return
        self.accept()

    def get_data(self):
        return {
            "job_id": self.job_combo.currentData(),
            "candidate_id": self.candidate_combo.currentData(),
            "start_date": self.start_date.date().toString("yyyy-MM-dd"),
            "end_date": self.end_date.date().toString("yyyy-MM-dd"),
            "salary": self.salary_input.value(),
            "work_content": self.work_content.toPlainText(),
            "payment_method": self.payment_combo.currentText(),
            "status": self.status_combo.currentText()
        }


class FlexWorkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("灵活用工智能管理平台")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化数据管理器
        self.data_manager = DataManager()
        
        # 设置样式
        self.setup_style()
        
        self.init_ui()
        
        # 创建系统托盘
        self.setup_system_tray()
        
        # 加载数据
        self.refresh_data()
    
    def setup_style(self):
        """设置应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                border: 1px solid #dee2e6;
                background: white;
            }
            QPushButton:hover {
                background: #e9ecef;
            }
            QPushButton#primary {
                background: #007aff;
                color: white;
                border: none;
            }
            QPushButton#primary:hover {
                background: #0056cc;
            }
            QPushButton#success {
                background: #34c759;
                color: white;
                border: none;
            }
            QPushButton#danger {
                background: #ff3b30;
                color: white;
                border: none;
            }
            QTableWidget {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
    
    def init_ui(self):
        """初始化界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        header = QLabel("🤖 灵活用工智能管理平台")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #1a1a1a; margin: 20px 0;")
        main_layout.addWidget(header)
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # 1. 智能匹配标签页
        self.create_matching_tab()
        
        # 2. 职位管理标签页
        self.create_jobs_tab()
        
        # 3. 候选人管理标签页
        self.create_candidates_tab()
        
        # 4. 合同管理标签页
        self.create_contracts_tab()
        
        # 5. 数据分析标签页
        self.create_analytics_tab()
        
        main_layout.addWidget(self.tabs)
        
        # 状态栏
        self.status_bar = QLabel("就绪 | 数据已加载")
        self.status_bar.setStyleSheet("background: white; padding: 10px; border-top: 1px solid #dee2e6;")
        main_layout.addWidget(self.status_bar)
    
    def create_matching_tab(self):
        """创建智能匹配标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 标题
        title = QLabel("🔍 智能岗位匹配")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # 匹配控制区
        control_layout = QHBoxLayout()
        
        self.job_combo = QComboBox()
        control_layout.addWidget(QLabel("选择职位:"))
        control_layout.addWidget(self.job_combo)
        
        match_btn = QPushButton("🚀 开始智能匹配")
        match_btn.clicked.connect(self.start_real_matching)
        match_btn.setObjectName("primary")
        control_layout.addWidget(match_btn)
        
        layout.addLayout(control_layout)
        
        # 结果表格
        self.match_table = QTableWidget(0, 4)
        self.match_table.setHorizontalHeaderLabels(["排名", "候选人", "匹配度", "操作"])
        match_header = self.match_table.horizontalHeader()
        if match_header is not None:
            match_header.setStretchLastSection(True)
        layout.addWidget(self.match_table)
        
        self.tabs.addTab(tab, "🎯 智能匹配")
    
    def create_jobs_tab(self):
        """创建职位管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        title = QLabel("📋 职位管理")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        
        new_btn = QPushButton("➕ 发布新职位")
        new_btn.clicked.connect(self.show_new_job_dialog)
        new_btn.setObjectName("primary")
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.refresh_jobs)
        
        toolbar.addWidget(title)
        toolbar.addStretch()
        toolbar.addWidget(refresh_btn)
        toolbar.addWidget(new_btn)
        
        layout.addLayout(toolbar)
        
        # 职位表格
        self.jobs_table = QTableWidget(0, 6)
        self.jobs_table.setHorizontalHeaderLabels(["职位名称", "薪资", "地点", "状态", "发布日期", "操作"])
        jobs_header = self.jobs_table.horizontalHeader()
        if jobs_header is not None:
            jobs_header.setStretchLastSection(True)
        layout.addWidget(self.jobs_table)
        
        self.tabs.addTab(tab, "📋 职位管理")
    
    def create_candidates_tab(self):
        """创建候选人管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        title = QLabel("👥 候选人管理")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        
        new_btn = QPushButton("➕ 添加候选人")
        new_btn.clicked.connect(self.show_new_candidate_dialog)
        new_btn.setObjectName("primary")
        
        toolbar.addWidget(title)
        toolbar.addStretch()
        toolbar.addWidget(new_btn)
        
        layout.addLayout(toolbar)
        
        # 候选人表格
        self.candidates_table = QTableWidget(0, 5)
        self.candidates_table.setHorizontalHeaderLabels(["姓名", "技能", "经验", "期望薪资", "状态"])
        candidates_header = self.candidates_table.horizontalHeader()
        if candidates_header is not None:
            candidates_header.setStretchLastSection(True)
        layout.addWidget(self.candidates_table)
        
        self.tabs.addTab(tab, "👥 候选人管理")
    
    def create_contracts_tab(self):
        """创建合同管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        title = QLabel("📄 合同管理")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        
        new_btn = QPushButton("➕ 新建合同")
        new_btn.clicked.connect(self.show_new_contract_dialog)
        new_btn.setObjectName("primary")
        
        toolbar.addWidget(title)
        toolbar.addStretch()
        toolbar.addWidget(new_btn)
        
        layout.addLayout(toolbar)
        
        # 合同表格
        self.contracts_table = QTableWidget(0, 6)
        self.contracts_table.setHorizontalHeaderLabels(["合同编号", "职位", "候选人", "期限", "状态", "操作"])
        contracts_header = self.contracts_table.horizontalHeader()
        if contracts_header is not None:
            contracts_header.setStretchLastSection(True)
        layout.addWidget(self.contracts_table)
        
        self.tabs.addTab(tab, "📄 合同管理")
    
    def create_analytics_tab(self):
        """创建数据分析标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("📊 数据分析")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # 统计卡片
        cards_layout = QHBoxLayout()
        
        stats = [
            ("总职位数", "jobs", "#007aff"),
            ("候选人总数", "candidates", "#34c759"),
            ("合同总数", "contracts", "#ff9500"),
            ("匹配成功率", "match_rate", "#af52de"),
        ]
        
        for label, key, color in stats:
            card = QWidget()
            card.setFixedHeight(100)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            
            value_label = QLabel("0")
            value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            text_label = QLabel(label)
            text_label.setStyleSheet("color: #666;")
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            card_layout.addWidget(value_label)
            card_layout.addWidget(text_label)
            
            card.setStyleSheet("""
                background: white;
                border-radius: 12px;
                border: 1px solid #dee2e6;
            """)
            cards_layout.addWidget(card)
        
        layout.addLayout(cards_layout)
        
        # 导出按钮
        export_btn = QPushButton("📥 导出数据报告")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)
        
        self.tabs.addTab(tab, "📊 数据分析")
    
    def setup_system_tray(self):
        """设置系统托盘"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            tray_icon = QSystemTrayIcon(self)
            
            # 创建托盘菜单
            tray_menu = QMenu()
            
            show_action = QAction("显示主窗口", self)
            show_action.triggered.connect(self.show)
            
            exit_action = QAction("退出", self)
            exit_action.triggered.connect(self.close)
            
            tray_menu.addAction(show_action)
            tray_menu.addAction(exit_action)
            
            tray_icon.setContextMenu(tray_menu)
            tray_icon.show()
    
    def refresh_data(self):
        """刷新所有数据"""
        self.refresh_jobs()
        self.refresh_candidates()
        self.refresh_contracts()
        self.update_status_bar()
    
    def refresh_jobs(self):
        """刷新职位表格"""
        self.jobs_table.setRowCount(0)
        
        for i, job in enumerate(self.data_manager.jobs):
            self.jobs_table.insertRow(i)
            
            # 职位名称
            self.jobs_table.setItem(i, 0, QTableWidgetItem(job.get("title", "未知")))
            
            # 薪资
            self.jobs_table.setItem(i, 1, QTableWidgetItem(job.get("salary", "")))
            
            # 地点
            self.jobs_table.setItem(i, 2, QTableWidgetItem(job.get("location", "")))
            
            # 状态
            status_item = QTableWidgetItem(job.get("status", "未知"))
            if job.get("status") == "招聘中":
                status_item.setForeground(QColor("#34c759"))
            elif job.get("status") == "暂停":
                status_item.setForeground(QColor("#ff9500"))
            self.jobs_table.setItem(i, 3, status_item)
            
            # 发布日期
            self.jobs_table.setItem(i, 4, QTableWidgetItem(job.get("created", "")))
            
            # 操作按钮
            action_btn = QPushButton("管理")
            action_btn.clicked.connect(lambda checked, idx=i: self.manage_job(idx))
            self.jobs_table.setCellWidget(i, 5, action_btn)
        
        # 更新职位下拉框
        self.job_combo.clear()
        for job in self.data_manager.jobs:
            self.job_combo.addItem(f"{job.get('title', '未知')} - {job.get('location', '')}")
    
    def refresh_candidates(self):
        """刷新候选人表格"""
        self.candidates_table.setRowCount(0)
        
        for i, candidate in enumerate(self.data_manager.candidates):
            self.candidates_table.insertRow(i)
            
            self.candidates_table.setItem(i, 0, QTableWidgetItem(candidate.get("name", "未知")))
            
            skills = candidate.get("skills", [])
            skills_text = ", ".join(skills[:3]) + ("..." if len(skills) > 3 else "")
            self.candidates_table.setItem(i, 1, QTableWidgetItem(skills_text))
            
            self.candidates_table.setItem(i, 2, QTableWidgetItem(f"{candidate.get('experience', 0)}年"))
            self.candidates_table.setItem(i, 3, QTableWidgetItem(f"{candidate.get('expected_salary', 0)}元/天"))
            
            status_item = QTableWidgetItem(candidate.get("status", "未知"))
            self.candidates_table.setItem(i, 4, status_item)
    
    def refresh_contracts(self):
        """刷新合同表格"""
        self.contracts_table.setRowCount(0)
        
        for i, contract in enumerate(self.data_manager.contracts):
            self.contracts_table.insertRow(i)
            
            # 合同编号
            self.contracts_table.setItem(i, 0, QTableWidgetItem(contract.get("id", "")))
            
            # 查找职位名称
            job_name = "未知"
            for job in self.data_manager.jobs:
                if job.get("id") == contract.get("job_id"):
                    job_name = job.get("title", "未知")
                    break
            
            # 查找候选人名称
            candidate_name = "未知"
            for candidate in self.data_manager.candidates:
                if candidate.get("id") == contract.get("candidate_id"):
                    candidate_name = candidate.get("name", "未知")
                    break
            
            self.contracts_table.setItem(i, 1, QTableWidgetItem(job_name))
            self.contracts_table.setItem(i, 2, QTableWidgetItem(candidate_name))
            
            # 期限
            period = f"{contract.get('start_date', '')} 至 {contract.get('end_date', '')}"
            self.contracts_table.setItem(i, 3, QTableWidgetItem(period))
            
            # 状态
            status_item = QTableWidgetItem(contract.get("status", "未知"))
            self.contracts_table.setItem(i, 4, status_item)
            
            # 操作按钮
            action_btn = QPushButton("查看")
            action_btn.clicked.connect(lambda checked, idx=i: self.view_contract(idx))
            self.contracts_table.setCellWidget(i, 5, action_btn)
    
    def update_status_bar(self):
        """更新状态栏"""
        total_jobs = len(self.data_manager.jobs)
        total_candidates = len(self.data_manager.candidates)
        total_contracts = len(self.data_manager.contracts)
        
        self.status_bar.setText(
            f"就绪 | 职位: {total_jobs} | 候选人: {total_candidates} | 合同: {total_contracts}"
        )
    
    # ===== 功能实现 =====
    
    def show_new_job_dialog(self):
        """显示新建职位对话框"""
        dialog = JobDialog(self)
        if dialog.exec():
            job_data = dialog.get_data()
            job_id = self.data_manager.add_job(job_data)
            
            QMessageBox.information(self, "成功", f"职位发布成功！\n职位ID: {job_id}")
            self.refresh_jobs()
            self.update_status_bar()
    
    def show_new_candidate_dialog(self):
        """显示添加候选人对话框"""
        # 获取输入
        name, ok1 = QInputDialog.getText(self, "添加候选人", "请输入姓名:")
        if not ok1 or not name:
            return
        
        skills, ok2 = QInputDialog.getText(self, "技能", "请输入技能（用逗号分隔）:")
        if not ok2:
            return
        
        salary, ok3 = QInputDialog.getInt(self, "期望薪资", "请输入期望薪资（元/天）:", 300, 0, 10000, 50)
        if not ok3:
            return
        
        # 创建候选人数据
        candidate_data = {
            "name": name,
            "skills": [s.strip() for s in skills.split(",") if s.strip()],
            "expected_salary": salary,
            "experience": 1,
            "location": "远程",
            "status": "可联系",
            "phone": "",
            "email": ""
        }
        
        candidate_id = self.data_manager.add_candidate(candidate_data)
        QMessageBox.information(self, "成功", f"候选人添加成功！\nID: {candidate_id}")
        self.refresh_candidates()
        self.update_status_bar()
    
    def show_new_contract_dialog(self):
        """显示新建合同对话框"""
        if not self.data_manager.jobs or not self.data_manager.candidates:
            QMessageBox.warning(self, "错误", "请先添加职位和候选人！")
            return
        
        dialog = ContractDialog(self, self.data_manager.jobs, self.data_manager.candidates)
        if dialog.exec():
            contract_data = dialog.get_data()
            contract_id = self.data_manager.add_contract(contract_data)
            
            QMessageBox.information(self, "成功", f"合同创建成功！\n合同ID: {contract_id}")
            self.refresh_contracts()
            self.update_status_bar()
    
    def start_real_matching(self):
        """开始真实的智能匹配"""
        if not self.data_manager.jobs:
            QMessageBox.warning(self, "错误", "请先添加职位！")
            return

        if not self.data_manager.candidates:
            QMessageBox.warning(self, "错误", "请先添加候选人！")
            return

        selected_index = self.job_combo.currentIndex()
        if selected_index < 0:
            QMessageBox.warning(self, "错误", "请先选择一个职位！")
            return

        # 清空结果表格
        self.match_table.setRowCount(0)

        # 获取选中的职位
        selected_job = self.data_manager.jobs[selected_index]

        QMessageBox.information(self, "开始匹配", f"开始匹配职位: {selected_job.get('title', '未知')}")

        # 解析职位薪资（兼容 "200-500元/天" 或 "200-500"）
        job_salary = str(selected_job.get("salary", "0-0"))
        try:
            job_salary_clean = job_salary.replace("元/天", "").replace(" ", "")
            parts = job_salary_clean.split("-")
            min_salary = int(parts[0]) if parts and parts[0].isdigit() else 0
            max_salary = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else max(min_salary, 0)
        except:
            min_salary, max_salary = 0, 0

        results = []
        for candidate in self.data_manager.candidates:
            # 技能匹配分数（按职位要求技能命中率）
            job_skills = selected_job.get("skills") or []
            if isinstance(job_skills, str):
                job_skills = [s.strip() for s in job_skills.split(",") if s.strip()]
            cand_skills = candidate.get("skills", []) or []
            if job_skills:
                intersect = set(s.lower() for s in cand_skills) & set(s.lower() for s in job_skills)
                skill_score = (len(intersect) / len(job_skills)) * 100
            else:
                skill_score = 50  # 无明确要求时给中性分

            # 薪资匹配分数（越接近职位范围分数越高）
            cand_salary = candidate.get("expected_salary", 0)
            salary_score = 0
            if max_salary > 0:
                if min_salary <= cand_salary <= max_salary:
                    salary_score = 100
                else:
                    # 根据偏离比例降低分数
                    if cand_salary < min_salary and min_salary > 0:
                        diff = (min_salary - cand_salary) / min_salary
                    elif cand_salary > max_salary:
                        diff = (cand_salary - max_salary) / max_salary if max_salary > 0 else 1
                    else:
                        diff = 1
                    salary_score = max(0, 100 * (1 - diff))
            else:
                salary_score = 50

            total_score = skill_score * 0.7 + salary_score * 0.3

            results.append({
                "candidate": candidate,
                "score": int(round(total_score)),
                "skill_score": int(round(skill_score)),
                "salary_score": int(round(salary_score))
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        # 显示结果
        self.match_table.setRowCount(len(results))
        for i, result in enumerate(results):
            candidate = result["candidate"]

            self.match_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.match_table.setItem(i, 1, QTableWidgetItem(candidate.get("name", "未知")))

            score_item = QTableWidgetItem(f"{result['score']}%")
            if result["score"] >= 80:
                score_item.setForeground(QColor("#34c759"))
            elif result["score"] >= 60:
                score_item.setForeground(QColor("#ff9500"))
            else:
                score_item.setForeground(QColor("#ff3b30"))
            self.match_table.setItem(i, 2, score_item)

            contact_btn = QPushButton("联系")
            contact_btn.clicked.connect(lambda checked, idx=i: self.contact_candidate(idx))
            self.match_table.setCellWidget(i, 3, contact_btn)
    
    def manage_job(self, job_index):
        """管理职位"""
        if 0 <= job_index < len(self.data_manager.jobs):
            job = self.data_manager.jobs[job_index]
            
            # 创建管理菜单
            menu = QMenu(self)
            
            edit_action = menu.addAction("📝 编辑")
            pause_action = menu.addAction("⏸️ 暂停/恢复")
            delete_action = menu.addAction("🗑️ 删除")
            
            action = menu.exec(self.jobs_table.mapToGlobal(
                self.jobs_table.visualItemRect(self.jobs_table.item(job_index, 0)).bottomLeft()
            ))
            
            if action == edit_action:
                self.edit_job(job_index)
            elif action == pause_action:
                self.toggle_job_status(job_index)
            elif action == delete_action:
                self.delete_job(job_index)
    
    def edit_job(self, job_index):
        """编辑职位"""
        job = self.data_manager.jobs[job_index]
        dialog = JobDialog(self, job)
        if dialog.exec():
            # 更新职位数据
            new_data = dialog.get_data()
            self.data_manager.jobs[job_index].update(new_data)
            self.data_manager.save_json(self.data_manager.jobs_file, self.data_manager.jobs)
            self.refresh_jobs()
            QMessageBox.information(self, "成功", "职位更新成功！")
    
    def toggle_job_status(self, job_index):
        """切换职位状态"""
        job = self.data_manager.jobs[job_index]
        current_status = job.get("status", "招聘中")
        
        if current_status == "招聘中":
            new_status = "暂停"
        else:
            new_status = "招聘中"
        
        job["status"] = new_status
        self.data_manager.save_json(self.data_manager.jobs_file, self.data_manager.jobs)
        self.refresh_jobs()
        
        QMessageBox.information(self, "成功", f"职位状态已更新为: {new_status}")
    
    def delete_job(self, job_index):
        """删除职位"""
        reply = QMessageBox.question(
            self, "确认删除",
            "确定要删除这个职位吗？此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.data_manager.jobs[job_index]
            self.data_manager.save_json(self.data_manager.jobs_file, self.data_manager.jobs)
            self.refresh_jobs()
            self.update_status_bar()
            QMessageBox.information(self, "成功", "职位已删除！")
    
    def contact_candidate(self, candidate_index):
        """联系候选人"""
        QMessageBox.information(self, "联系候选人", "联系功能开发中...\n请使用电话或邮件联系候选人。")
    
    def view_contract(self, contract_index):
        """查看合同详情"""
        if 0 <= contract_index < len(self.data_manager.contracts):
            contract = self.data_manager.contracts[contract_index]
            
            details = f"""
            📄 合同详情
            {'='*30}
            合同编号: {contract.get('id', '未知')}
            开始日期: {contract.get('start_date', '未知')}
            结束日期: {contract.get('end_date', '未知')}
            约定薪资: {contract.get('salary', '未知')}元/天
            付款方式: {contract.get('payment_method', '未知')}
            合同状态: {contract.get('status', '未知')}
            
            工作内容:
            {contract.get('work_content', '暂无')}
            """
            
            QMessageBox.information(self, "合同详情", details)
    
    def export_report(self):
        """导出数据报告"""
        options = QFileDialog.Option.ShowDirsOnly
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出报告", "灵活用工平台报告", "CSV文件 (*.csv);;所有文件 (*)", options=options
        )
        
        if file_path:
            try:
                # 导出职位数据
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(["职位ID", "职位名称", "薪资", "地点", "状态", "发布日期"])
                    for job in self.data_manager.jobs:
                        writer.writerow([
                            job.get("id", ""),
                            job.get("title", ""),
                            job.get("salary", ""),
                            job.get("location", ""),
                            job.get("status", ""),
                            job.get("created", "")
                        ])
                
                QMessageBox.information(self, "导出成功", f"数据已导出到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"导出时出错:\n{str(e)}")
    
    def closeEvent(self, a0):
        """关闭应用时的处理"""
        if a0 is None:
            return
        # 保存所有数据
        self.data_manager.save_all()
        
        reply = QMessageBox.question(
            self, "确认退出",
            "确定要退出灵活用工管理平台吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            a0.accept()
        else:
            a0.ignore()


def main():
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("灵活用工管理平台")
    app.setApplicationDisplayName("灵活用工管理平台")
    
    # 创建窗口
    window = FlexWorkApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
