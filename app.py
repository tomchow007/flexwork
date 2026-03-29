#!/usr/bin/env python3
"""
灵活用工管理平台 - Streamlit Web版
包含数据持久化和所有业务逻辑
"""
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, date

# 页面配置
st.set_page_config(
    page_title="FlexWork - 灵活用工智能管理平台",
    page_icon="💼",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #007aff;
    }
    .metric-label {
        color: #666;
        margin-top: 8px;
    }
    .match-high {
        color: #34c759;
        font-weight: bold;
    }
    .match-medium {
        color: #ff9500;
        font-weight: bold;
    }
    .match-low {
        color: #ff3b30;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


class DataManager:
    """数据管理器 - 负责所有数据的保存和加载"""
    
    def __init__(self):
        # 使用 Streamlit 的 session_state 存储数据
        if 'jobs' not in st.session_state:
            st.session_state.jobs = self.default_jobs()
        if 'candidates' not in st.session_state:
            st.session_state.candidates = self.default_candidates()
        if 'contracts' not in st.session_state:
            st.session_state.contracts = self.default_contracts()
    
    @property
    def jobs(self):
        return st.session_state.jobs
    
    @property
    def candidates(self):
        return st.session_state.candidates
    
    @property
    def contracts(self):
        return st.session_state.contracts
    
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
                "skills": ["Python", "React", "JavaScript"],
                "requirements": "3年以上经验，精通JavaScript",
                "created": "2024-01-01",
                "applicants": 12,
                "job_type": "兼职",
                "urgency": "紧急"
            },
            {
                "id": "job_002",
                "title": "后端开发工程师",
                "salary": "400-600元/天",
                "location": "远程",
                "status": "招聘中",
                "description": "负责后端API开发，要求Python经验",
                "skills": ["Python", "Django", "FastAPI"],
                "requirements": "3年以上Python经验",
                "created": "2024-01-15",
                "applicants": 8,
                "job_type": "兼职",
                "urgency": "普通"
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
            },
            {
                "id": "cand_002",
                "name": "李四",
                "skills": ["Python", "Django", "PostgreSQL"],
                "experience": 5,
                "expected_salary": 500,
                "location": "北京",
                "status": "可联系",
                "phone": "13900139000",
                "email": "lisi@example.com",
                "availability": "全职"
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
                "payment_method": "月结",
                "work_content": "负责前端页面开发和维护"
            }
        ]
    
    def add_job(self, job_data):
        """添加新职位"""
        job_data["id"] = f"job_{len(self.jobs) + 1:03d}"
        job_data["created"] = datetime.now().strftime("%Y-%m-%d")
        job_data["applicants"] = 0
        st.session_state.jobs.append(job_data)
        return job_data["id"]
    
    def add_candidate(self, candidate_data):
        """添加新候选人"""
        candidate_data["id"] = f"cand_{len(self.candidates) + 1:03d}"
        st.session_state.candidates.append(candidate_data)
        return candidate_data["id"]
    
    def add_contract(self, contract_data):
        """添加新合同"""
        contract_data["id"] = f"contract_{len(self.contracts) + 1:03d}"
        st.session_state.contracts.append(contract_data)
        return contract_data["id"]
    
    def update_job(self, job_id, job_data):
        """更新职位"""
        for i, job in enumerate(self.jobs):
            if job["id"] == job_id:
                st.session_state.jobs[i].update(job_data)
                return True
        return False
    
    def delete_job(self, job_id):
        """删除职位"""
        st.session_state.jobs = [j for j in self.jobs if j["id"] != job_id]
    
    def update_contract(self, contract_id, contract_data):
        """更新合同"""
        for i, contract in enumerate(self.contracts):
            if contract["id"] == contract_id:
                st.session_state.contracts[i].update(contract_data)
                return True
        return False
    
    def delete_contract(self, contract_id):
        """删除合同"""
        st.session_state.contracts = [c for c in self.contracts if c["id"] != contract_id]


def init_session_state():
    """初始化 session state"""
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    if 'page' not in st.session_state:
        st.session_state.page = "智能匹配"


def main():
    init_session_state()
    dm = st.session_state.data_manager
    
    # 侧边栏导航
    with st.sidebar:
        st.title("🤖 FlexWork")
        st.markdown("---")
        
        pages = ["🎯 智能匹配", "📋 职位管理", "👥 候选人管理", "📄 合同管理", "📊 数据分析"]
        selected_page = st.radio("导航菜单", pages, label_visibility="collapsed")
        
        st.markdown("---")
        
        # 统计信息
        st.markdown("### 📊 数据统计")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("职位", len(dm.jobs))
        with col2:
            st.metric("候选人", len(dm.candidates))
        with col3:
            st.metric("合同", len(dm.contracts))
    
    # 主内容区域
    st.title("灵活用工智能管理平台")
    
    if selected_page == "🎯 智能匹配":
        smart_matching_page(dm)
    elif selected_page == "📋 职位管理":
        job_management_page(dm)
    elif selected_page == "👥 候选人管理":
        candidate_management_page(dm)
    elif selected_page == "📄 合同管理":
        contract_management_page(dm)
    elif selected_page == "📊 数据分析":
        analytics_page(dm)


def smart_matching_page(dm):
    """智能匹配页面"""
    st.header("🔍 智能岗位匹配")
    
    if not dm.jobs:
        st.warning("暂无职位，请先添加职位")
        return
    
    if not dm.candidates:
        st.warning("暂无候选人，请先添加候选人")
        return
    
    # 选择职位
    job_options = {f"{job['title']} - {job['location']}": job for job in dm.jobs if job['status'] == '招聘中'}
    
    if not job_options:
        st.warning("没有正在招聘的职位")
        return
    
    selected_job_name = st.selectbox("选择职位", list(job_options.keys()))
    selected_job = job_options[selected_job_name]
    
    if st.button("🚀 开始智能匹配", type="primary", use_container_width=True):
        with st.spinner("正在匹配中..."):
            # 解析职位薪资
            job_salary = str(selected_job.get("salary", "0-0"))
            try:
                job_salary_clean = job_salary.replace("元/天", "").replace(" ", "")
                parts = job_salary_clean.split("-")
                min_salary = int(parts[0]) if parts and parts[0].isdigit() else 0
                max_salary = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else min_salary
            except:
                min_salary, max_salary = 0, 0
            
            results = []
            for candidate in dm.candidates:
                # 技能匹配
                job_skills = selected_job.get("skills", [])
                cand_skills = candidate.get("skills", [])
                if job_skills:
                    intersect = set(s.lower() for s in cand_skills) & set(s.lower() for s in job_skills)
                    skill_score = (len(intersect) / len(job_skills)) * 100
                else:
                    skill_score = 50
                
                # 薪资匹配
                cand_salary = candidate.get("expected_salary", 0)
                if max_salary > 0:
                    if min_salary <= cand_salary <= max_salary:
                        salary_score = 100
                    else:
                        if cand_salary < min_salary and min_salary > 0:
                            diff = (min_salary - cand_salary) / min_salary
                        elif cand_salary > max_salary:
                            diff = (cand_salary - max_salary) / max_salary if max_salary > 0 else 1
                        else:
                            diff = 1
                        salary_score = max(0, 100 * (1 - min(diff, 1)))
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
            st.subheader("📊 匹配结果")
            
            for i, result in enumerate(results):
                candidate = result["candidate"]
                score = result["score"]
                
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
                    
                    with col1:
                        st.markdown(f"### #{i+1}")
                    
                    with col2:
                        st.markdown(f"**{candidate['name']}**")
                        st.caption(f"技能: {', '.join(candidate.get('skills', []))}")
                    
                    with col3:
                        if score >= 80:
                            st.markdown(f'<span class="match-high">匹配度: {score}%</span>', unsafe_allow_html=True)
                        elif score >= 60:
                            st.markdown(f'<span class="match-medium">匹配度: {score}%</span>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<span class="match-low">匹配度: {score}%</span>', unsafe_allow_html=True)
                        
                        st.caption(f"期望薪资: {candidate.get('expected_salary', 0)}元/天")
                    
                    with col4:
                        if st.button(f"📞 联系", key=f"contact_{i}"):
                            st.info(f"联系方式: {candidate.get('phone', '未提供')} | {candidate.get('email', '未提供')}")
                    
                    st.divider()


def job_management_page(dm):
    """职位管理页面"""
    st.header("📋 职位管理")
    
    # 添加职位的表单
    with st.expander("➕ 发布新职位", expanded=False):
        with st.form("add_job_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("职位标题*", placeholder="例如：前端开发工程师（远程兼职）")
                location = st.selectbox("工作地点", ["远程", "上海", "北京", "深圳", "杭州", "广州", "成都", "其他"])
                salary_min = st.number_input("最低薪资（元/天）", min_value=0, value=200)
                salary_max = st.number_input("最高薪资（元/天）", min_value=0, value=500)
                job_type = st.selectbox("工作类型", ["全职", "兼职", "实习", "项目制"])
            
            with col2:
                skills = st.text_input("技能要求*", placeholder="用逗号分隔，例如：Python, React, Vue")
                urgency = st.selectbox("紧急程度", ["普通", "紧急", "特急"])
                experience = st.selectbox("工作经验", ["不限", "1年以下", "1-3年", "3-5年", "5年以上"])
            
            description = st.text_area("职位描述", height=100)
            requirements = st.text_area("任职要求", height=100)
            
            submitted = st.form_submit_button("发布职位", type="primary", use_container_width=True)
            
            if submitted:
                if not title or not skills:
                    st.error("请填写职位标题和技能要求")
                elif salary_min > salary_max:
                    st.error("最低薪资不能高于最高薪资")
                else:
                    job_data = {
                        "title": title,
                        "description": description,
                        "skills": [s.strip() for s in skills.split(",") if s.strip()],
                        "experience": experience,
                        "salary": f"{salary_min}-{salary_max}元/天",
                        "location": location,
                        "job_type": job_type,
                        "urgency": urgency,
                        "requirements": requirements,
                        "status": "招聘中"
                    }
                    job_id = dm.add_job(job_data)
                    st.success(f"职位发布成功！ID: {job_id}")
                    st.rerun()
    
    # 显示职位列表
    if dm.jobs:
        # 转换为 DataFrame 显示
        jobs_df = pd.DataFrame(dm.jobs)
        display_df = jobs_df[["title", "salary", "location", "status", "created", "id"]]
        display_df.columns = ["职位名称", "薪资", "地点", "状态", "发布日期", "ID"]
        
        # 状态颜色标记
        def color_status(val):
            if val == "招聘中":
                return "background-color: #d4edda; color: #155724"
            elif val == "暂停":
                return "background-color: #fff3cd; color: #856404"
            return ""
        
        st.dataframe(display_df.style.applymap(color_status, subset=["状态"]), use_container_width=True)
        
        # 职位操作
        st.subheader("🔧 职位操作")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            job_to_edit = st.selectbox("选择要编辑的职位", [f"{job['title']} ({job['id']})" for job in dm.jobs], key="edit_job")
            if st.button("✏️ 编辑职位", use_container_width=True):
                job_id = job_to_edit.split("(")[-1].rstrip(")")
                job = next((j for j in dm.jobs if j["id"] == job_id), None)
                if job:
                    st.session_state.editing_job = job
                    st.rerun()
        
        with col2:
            job_to_toggle = st.selectbox("选择要切换状态的职位", [f"{job['title']} ({job['id']})" for job in dm.jobs], key="toggle_job")
            if st.button("🔄 切换状态", use_container_width=True):
                job_id = job_to_toggle.split("(")[-1].rstrip(")")
                job = next((j for j in dm.jobs if j["id"] == job_id), None)
                if job:
                    job["status"] = "暂停" if job["status"] == "招聘中" else "招聘中"
                    st.success(f"职位状态已更新为: {job['status']}")
                    st.rerun()
        
        with col3:
            job_to_delete = st.selectbox("选择要删除的职位", [f"{job['title']} ({job['id']})" for job in dm.jobs], key="delete_job")
            if st.button("🗑️ 删除职位", use_container_width=True):
                job_id = job_to_delete.split("(")[-1].rstrip(")")
                dm.delete_job(job_id)
                st.success("职位已删除")
                st.rerun()
        
        # 编辑表单
        if 'editing_job' in st.session_state:
            st.subheader("📝 编辑职位")
            job = st.session_state.editing_job
            
            with st.form("edit_job_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    edit_title = st.text_input("职位标题", job.get("title", ""))
                    edit_location = st.selectbox("工作地点", ["远程", "上海", "北京", "深圳", "杭州", "广州", "成都", "其他"], 
                                                  index=["远程", "上海", "北京", "深圳", "杭州", "广州", "成都", "其他"].index(job.get("location", "远程")))
                
                with col2:
                    edit_skills = st.text_input("技能要求", ", ".join(job.get("skills", [])))
                    edit_status = st.selectbox("状态", ["招聘中", "暂停"], index=0 if job.get("status") == "招聘中" else 1)
                
                edit_description = st.text_area("职位描述", job.get("description", ""), height=100)
                
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.form_submit_button("保存修改", type="primary", use_container_width=True):
                        job["title"] = edit_title
                        job["location"] = edit_location
                        job["skills"] = [s.strip() for s in edit_skills.split(",") if s.strip()]
                        job["status"] = edit_status
                        job["description"] = edit_description
                        del st.session_state.editing_job
                        st.success("职位已更新")
                        st.rerun()
                
                with col2_btn:
                    if st.form_submit_button("取消", use_container_width=True):
                        del st.session_state.editing_job
                        st.rerun()
    else:
        st.info("暂无职位，请点击上方发布新职位")


def candidate_management_page(dm):
    """候选人管理页面"""
    st.header("👥 候选人管理")
    
    # 添加候选人的表单
    with st.expander("➕ 添加候选人", expanded=False):
        with st.form("add_candidate_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("姓名*")
                skills = st.text_input("技能*", placeholder="用逗号分隔，例如：Python, React, Vue")
                expected_salary = st.number_input("期望薪资（元/天）", min_value=0, value=300)
            
            with col2:
                experience = st.number_input("工作经验（年）", min_value=0, value=1, step=1)
                location = st.selectbox("所在城市", ["远程", "上海", "北京", "深圳", "杭州", "广州", "成都"])
                phone = st.text_input("电话")
                email = st.text_input("邮箱")
            
            status = st.selectbox("状态", ["可联系", "面试中", "已录用", "不合适"])
            availability = st.text_input("可工作时间", placeholder="例如：周一至周五")
            
            submitted = st.form_submit_button("添加候选人", type="primary", use_container_width=True)
            
            if submitted:
                if not name or not skills:
                    st.error("请填写姓名和技能")
                else:
                    candidate_data = {
                        "name": name,
                        "skills": [s.strip() for s in skills.split(",") if s.strip()],
                        "experience": experience,
                        "expected_salary": expected_salary,
                        "location": location,
                        "status": status,
                        "phone": phone,
                        "email": email,
                        "availability": availability
                    }
                    candidate_id = dm.add_candidate(candidate_data)
                    st.success(f"候选人添加成功！ID: {candidate_id}")
                    st.rerun()
    
    # 显示候选人列表
    if dm.candidates:
        candidates_df = pd.DataFrame(dm.candidates)
        display_df = candidates_df[["name", "skills", "experience", "expected_salary", "status", "location", "id"]]
        display_df.columns = ["姓名", "技能", "经验(年)", "期望薪资(元/天)", "状态", "地点", "ID"]
        
        # 将技能列表转换为字符串显示
        display_df["技能"] = display_df["技能"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        
        st.dataframe(display_df, use_container_width=True)
        
        # 删除候选人
        st.subheader("🗑️ 删除候选人")
        candidate_to_delete = st.selectbox("选择要删除的候选人", [f"{c['name']} ({c['id']})" for c in dm.candidates])
        if st.button("删除", type="secondary", use_container_width=True):
            candidate_id = candidate_to_delete.split("(")[-1].rstrip(")")
            dm.candidates = [c for c in dm.candidates if c["id"] != candidate_id]
            st.success("候选人已删除")
            st.rerun()
    else:
        st.info("暂无候选人，请点击上方添加候选人")


def contract_management_page(dm):
    """合同管理页面"""
    st.header("📄 合同管理")
    
    # 新建合同
    with st.expander("➕ 新建合同", expanded=False):
        if not dm.jobs or not dm.candidates:
            st.warning("请先添加职位和候选人")
        else:
            with st.form("add_contract_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    job_options = {f"{job['title']} - {job['location']}": job["id"] for job in dm.jobs}
                    selected_job = st.selectbox("选择职位", list(job_options.keys()))
                    job_id = job_options[selected_job]
                
                with col2:
                    candidate_options = {f"{c['name']} - {', '.join(c.get('skills', [])[:2])}": c["id"] for c in dm.candidates}
                    selected_candidate = st.selectbox("选择候选人", list(candidate_options.keys()))
                    candidate_id = candidate_options[selected_candidate]
                
                start_date = st.date_input("开始日期", value=date.today())
                end_date = st.date_input("结束日期", value=date.today().replace(month=date.today().month+3))
                salary = st.number_input("约定薪资（元/天）", min_value=0, value=400)
                payment_method = st.selectbox("付款方式", ["月结", "周结", "项目结", "完成结"])
                status = st.selectbox("合同状态", ["待签署", "执行中", "已完成", "已终止"])
                work_content = st.text_area("工作内容", height=80)
                
                submitted = st.form_submit_button("创建合同", type="primary", use_container_width=True)
                
                if submitted:
                    if start_date > end_date:
                        st.error("开始日期不能晚于结束日期")
                    else:
                        contract_data = {
                            "job_id": job_id,
                            "candidate_id": candidate_id,
                            "start_date": start_date.strftime("%Y-%m-%d"),
                            "end_date": end_date.strftime("%Y-%m-%d"),
                            "salary": salary,
                            "payment_method": payment_method,
                            "status": status,
                            "work_content": work_content
                        }
                        contract_id = dm.add_contract(contract_data)
                        st.success(f"合同创建成功！ID: {contract_id}")
                        st.rerun()
    
    # 显示合同列表
    if dm.contracts:
        contracts_display = []
        for contract in dm.contracts:
            job = next((j for j in dm.jobs if j["id"] == contract["job_id"]), {})
            candidate = next((c for c in dm.candidates if c["id"] == contract["candidate_id"]), {})
            
            contracts_display.append({
                "合同编号": contract["id"],
                "职位": job.get("title", "未知"),
                "候选人": candidate.get("name", "未知"),
                "期限": f"{contract['start_date']} 至 {contract['end_date']}",
                "薪资": f"{contract['salary']}元/天",
                "状态": contract["status"],
                "付款方式": contract["payment_method"]
            })
        
        contracts_df = pd.DataFrame(contracts_display)
        st.dataframe(contracts_df, use_container_width=True)
        
        # 合同操作
        st.subheader("🔧 合同操作")
        col1, col2 = st.columns(2)
        
        with col1:
            contract_to_edit = st.selectbox("选择要编辑的合同", [f"{c['id']} - {c.get('job_title', '')}" for c in dm.contracts])
            if st.button("✏️ 编辑合同状态", use_container_width=True):
                contract_id = contract_to_edit.split(" ")[0]
                contract = next((c for c in dm.contracts if c["id"] == contract_id), None)
                if contract:
                    st.session_state.editing_contract = contract
                    st.rerun()
        
        with col2:
            contract_to_delete = st.selectbox("选择要删除的合同", [f"{c['id']} - {c.get('job_title', '')}" for c in dm.contracts], key="del_contract")
            if st.button("🗑️ 删除合同", use_container_width=True):
                contract_id = contract_to_delete.split(" ")[0]
                dm.delete_contract(contract_id)
                st.success("合同已删除")
                st.rerun()
        
        # 编辑合同状态
        if 'editing_contract' in st.session_state:
            contract = st.session_state.editing_contract
            st.subheader("📝 编辑合同")
            
            new_status = st.selectbox("合同状态", ["待签署", "执行中", "已完成", "已终止"], 
                                      index=["待签署", "执行中", "已完成", "已终止"].index(contract["status"]))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("保存", type="primary", use_container_width=True):
                    contract["status"] = new_status
                    del st.session_state.editing_contract
                    st.success("合同状态已更新")
                    st.rerun()
            with col2:
                if st.button("取消", use_container_width=True):
                    del st.session_state.editing_contract
                    st.rerun()
    else:
        st.info("暂无合同，请点击上方新建合同")


def analytics_page(dm):
    """数据分析页面"""
    st.header("📊 数据分析")
    
    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">总职位数</div>
        </div>
        """.format(len(dm.jobs)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">候选人总数</div>
        </div>
        """.format(len(dm.candidates)), unsafe_allow_html=True)
    
    with col3:
        active_contracts = len([c for c in dm.contracts if c["status"] == "执行中"])
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">执行中合同</div>
        </div>
        """.format(active_contracts), unsafe_allow_html=True)
    
    with col4:
        match_rate = 0
        if len(dm.candidates) > 0:
            match_rate = int((len(dm.contracts) / max(len(dm.candidates), len(dm.jobs))) * 100)
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">匹配转化率</div>
        </div>
        """.format(f"{match_rate}%"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 职位状态分布
    st.subheader("📊 职位状态分布")
    if dm.jobs:
        job_status_df = pd.DataFrame(dm.jobs)
        status_counts = job_status_df["status"].value_counts()
        st.bar_chart(status_counts)
    
    # 合同状态分布
    st.subheader("📄 合同状态分布")
    if dm.contracts:
        contract_status_df = pd.DataFrame(dm.contracts)
        status_counts = contract_status_df["status"].value_counts()
        st.bar_chart(status_counts)
    
    # 导出功能
    st.subheader("📥 导出数据")
    export_type = st.selectbox("选择导出内容", ["职位数据", "候选人数据", "合同数据"])
    
    if st.button("导出为CSV", type="primary"):
        if export_type == "职位数据" and dm.jobs:
            df = pd.DataFrame(dm.jobs)
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 下载CSV文件",
                data=csv,
                file_name=f"flexwork_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        elif export_type == "候选人数据" and dm.candidates:
            df = pd.DataFrame(dm.candidates)
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 下载CSV文件",
                data=csv,
                file_name=f"flexwork_candidates_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        elif export_type == "合同数据" and dm.contracts:
            df = pd.DataFrame(dm.contracts)
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 下载CSV文件",
                data=csv,
                file_name=f"flexwork_contracts_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("没有可导出的数据")


if __name__ == "__main__":
    main()
