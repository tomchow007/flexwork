#!/usr/bin/env python3
"""
灵活用工平台 - Web 版本（带数据持久化）
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from data_store import DataStore

# 页面配置
st.set_page_config(
    page_title="灵活用工平台",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #007aff;
    }
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007aff;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化数据存储
@st.cache_resource
def init_data_store():
    return DataStore()

store = init_data_store()

# 侧边栏导航
st.sidebar.markdown("## 🤖 灵活用工平台")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "导航",
    ["🏠 仪表板", "📋 职位管理", "👥 候选人管理", "📄 合同管理", "🎯 智能匹配", "📊 数据分析", "⚙️ 设置"]
)

st.sidebar.markdown("---")
stats = store.get_stats()
st.sidebar.info(f"""
📊 当前状态
- 职位: {stats['total_jobs']}
- 候选人: {stats['total_candidates']}  
- 合同: {stats['total_contracts']}
- 合同金额: ¥{stats['total_amount']:,}
""")

# ==================== 仪表板 ====================
if page == "🏠 仪表板":
    st.markdown('<div class="main-header"><h1>🏠 灵活用工仪表板</h1></div>', unsafe_allow_html=True)
    
    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_jobs']}</div>
            <div class="stat-label">职位总数</div>
            <div style="color: #34c759;">活跃: {stats['active_jobs']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_candidates']}</div>
            <div class="stat-label">候选人总数</div>
            <div style="color: #34c759;">可联系: {stats['available_candidates']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_contracts']}</div>
            <div class="stat-label">合同总数</div>
            <div style="color: #34c759;">执行中: {stats['active_contracts']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">¥{stats['total_amount']:,}</div>
            <div class="stat-label">合同总金额</div>
            <div style="color: #ff9500;">本月新增: +¥0</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 图表区域
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 职位状态分布")
        status_counts = {}
        for job in store.jobs:
            status = job['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="职位分布",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 合同趋势")
        if store.contracts:
            dates = [c['start_date'][:7] for c in store.contracts]  # YYYY-MM
            amounts = [c['total_amount'] for c in store.contracts]
            
            df = pd.DataFrame({
                '月份': dates,
                '金额': amounts
            })
            df = df.groupby('月份').sum().reset_index()
            
            fig = px.line(df, x='月份', y='金额', title="月度合同金额")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("暂无合同数据")

# ==================== 职位管理 ====================
elif page == "📋 职位管理":
    st.markdown('<div class="main-header"><h1>📋 职位管理</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 职位列表", "➕ 发布新职位"])
    
    with tab1:
        if store.jobs:
            # 创建可编辑的表格
            for i, job in enumerate(store.jobs):
                with st.expander(f"📌 {job['title']} - {job['status']}"):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        **薪资**: {job['salary']}  
                        **地点**: {job['location']}  
                        **技能**: {', '.join(job.get('skills', []))}  
                        **描述**: {job.get('description', '无')}  
                        **发布日期**: {job.get('created', '未知')}
                        """)
                    
                    with col2:
                        if st.button("✏️ 编辑", key=f"edit_{i}"):
                            st.session_state['edit_job'] = job
                    
                    with col3:
                        if st.button("🗑️ 删除", key=f"del_{i}"):
                            store.jobs.pop(i)
                            store.save_all()
                            st.rerun()
        else:
            st.info("暂无职位数据")
    
    with tab2:
        with st.form("new_job_form"):
            title = st.text_input("职位名称 *", placeholder="例如：前端开发工程师")
            
            col1, col2 = st.columns(2)
            with col1:
                salary_min = st.number_input("最低薪资", min_value=0, value=200, step=50)
            with col2:
                salary_max = st.number_input("最高薪资", min_value=0, value=500, step=50)
            
            location = st.selectbox("工作地点", ["远程", "上海", "北京", "深圳", "杭州", "广州", "成都"])
            skills = st.text_input("技能要求 *", placeholder="Python, React, Vue (用逗号分隔)")
            description = st.text_area("职位描述", height=100)
            
            col1, col2, col3 = st.columns(3)
            with col2:
                submitted = st.form_submit_button("📢 发布职位", use_container_width=True)
            
            if submitted:
                if title and skills:
                    new_job = {
                        "title": title,
                        "salary": f"{salary_min}-{salary_max}元/天",
                        "location": location,
                        "skills": [s.strip() for s in skills.split(",") if s.strip()],
                        "description": description,
                        "status": "招聘中"
                    }
                    job_id = store.add_job(new_job)
                    st.markdown(f'<div class="success-message">✅ 职位发布成功！ ID: {job_id}</div>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown('<div class="warning-message">❌ 职位名称和技能要求不能为空！</div>', unsafe_allow_html=True)

# ==================== 候选人管理 ====================
elif page == "👥 候选人管理":
    st.markdown('<div class="main-header"><h1>👥 候选人管理</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["👥 候选人列表", "➕ 添加候选人"])
    
    with tab1:
        if store.candidates:
            for i, candidate in enumerate(store.candidates):
                with st.expander(f"👤 {candidate['name']} - {candidate['status']}"):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        **技能**: {', '.join(candidate.get('skills', []))}  
                        **经验**: {candidate.get('experience', 0)}年  
                        **期望薪资**: {candidate.get('expected_salary', 0)}元/天  
                        **联系方式**: {candidate.get('phone', '无')} | {candidate.get('email', '无')}
                        """)
                    
                    with col2:
                        if st.button("✏️ 编辑", key=f"edit_cand_{i}"):
                            pass
                    
                    with col3:
                        if st.button("🗑️ 删除", key=f"del_cand_{i}"):
                            store.candidates.pop(i)
                            store.save_all()
                            st.rerun()
        else:
            st.info("暂无候选人数据")
    
    with tab2:
        with st.form("new_candidate_form"):
            name = st.text_input("姓名 *")
            skills = st.text_input("技能 *", placeholder="Python, React, Vue (用逗号分隔)")
            
            col1, col2 = st.columns(2)
            with col1:
                experience = st.number_input("工作经验（年）", min_value=0, max_value=50, value=3)
            with col2:
                salary = st.number_input("期望薪资（元/天）", min_value=0, value=300, step=50)
            
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("电话", placeholder="13800138000")
            with col2:
                email = st.text_input("邮箱", placeholder="name@example.com")
            
            col1, col2, col3 = st.columns(3)
            with col2:
                submitted = st.form_submit_button("➕ 添加候选人", use_container_width=True)
            
            if submitted:
                if name and skills:
                    new_candidate = {
                        "name": name,
                        "skills": [s.strip() for s in skills.split(",") if s.strip()],
                        "experience": experience,
                        "expected_salary": salary,
                        "phone": phone,
                        "email": email,
                        "status": "可联系"
                    }
                    cand_id = store.add_candidate(new_candidate)
                    st.markdown(f'<div class="success-message">✅ 候选人 {name} 添加成功！ ID: {cand_id}</div>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown('<div class="warning-message">❌ 姓名和技能不能为空！</div>', unsafe_allow_html=True)

# ==================== 合同管理 ====================
elif page == "📄 合同管理":
    st.markdown('<div class="main-header"><h1>📄 合同管理</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if store.contracts:
            for i, contract in enumerate(store.contracts):
                with st.expander(f"📄 {contract['job_title']} - {contract['candidate_name']}"):
                    st.markdown(f"""
                    **合同编号**: {contract['id']}  
                    **期限**: {contract['start_date']} 至 {contract['end_date']}  
                    **薪资**: {contract.get('salary', 0)}元/天  
                    **状态**: {contract['status']}  
                    **总金额**: ¥{contract.get('total_amount', 0):,}
                    """)
                    
                    if st.button("查看详情", key=f"view_{i}"):
                        st.info("详情功能开发中")
        else:
            st.info("暂无合同数据")
    
    with col2:
        st.subheader("📊 合同统计")
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.2rem; font-weight: bold;">{stats['total_contracts']}</div>
            <div>总合同数</div>
        </div>
        <div class="metric-card">
            <div style="font-size: 1.2rem; font-weight: bold;">{stats['active_contracts']}</div>
            <div>执行中合同</div>
        </div>
        <div class="metric-card">
            <div style="font-size: 1.2rem; font-weight: bold;">¥{stats['total_amount']:,}</div>
            <div>合同总金额</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ 新建合同", use_container_width=True):
            st.info("合同创建功能开发中...")

# ==================== 智能匹配 ====================
elif page == "🎯 智能匹配":
    st.markdown('<div class="main-header"><h1>🎯 智能匹配</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("选择职位")
        active_jobs = [j for j in store.jobs if j['status'] == '招聘中']
        if active_jobs:
            job_options = [f"{j['title']} - {j['location']}" for j in active_jobs]
            selected_job = st.selectbox("职位列表", job_options)
            
            if st.button("开始智能匹配", type="primary", use_container_width=True):
                # 获取选中的职位
                job_index = job_options.index(selected_job)
                job = active_jobs[job_index]
                
                # 匹配算法
                results = []
                for candidate in store.candidates:
                    if candidate['status'] in ['可联系', '待面试']:
                        # 计算技能匹配度
                        job_skills = set(job.get('skills', []))
                        candidate_skills = set(candidate.get('skills', []))
                        matched_skills = job_skills.intersection(candidate_skills)
                        
                        if job_skills:
                            match_score = len(matched_skills) / len(job_skills) * 100
                        else:
                            match_score = 50
                        
                        # 薪资匹配度
                        try:
                            salary_range = job['salary'].replace('元/天', '').split('-')
                            min_salary = int(salary_range[0])
                            max_salary = int(salary_range[1])
                            
                            if min_salary <= candidate['expected_salary'] <= max_salary:
                                salary_match = 100
                            else:
                                salary_match = max(0, 100 - abs(candidate['expected_salary'] - min_salary) / 10)
                        except:
                            salary_match = 50
                        
                        # 综合分数
                        total_score = match_score * 0.7 + salary_match * 0.3
                        
                        results.append({
                            "候选人": candidate['name'],
                            "技能": ", ".join(list(matched_skills)[:3]),
                            "匹配度": f"{total_score:.1f}%",
                            "期望薪资": f"{candidate['expected_salary']}元/天",
                            "状态": candidate['status']
                        })
                
                if results:
                    results.sort(key=lambda x: float(x['匹配度'][:-1]), reverse=True)
                    st.session_state['match_results'] = results
                else:
                    st.warning("没有找到匹配的候选人")
        else:
            st.warning("暂无招聘中的职位")
    
    with col2:
        st.subheader("匹配结果")
        if 'match_results' in st.session_state:
            for i, result in enumerate(st.session_state['match_results'][:5]):
                score = float(result['匹配度'][:-1])
                color = "#34c759" if score >= 80 else "#ff9500" if score >= 60 else "#ff3b30"
                
                st.markdown(f"""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: bold;">{i+1}. {result['候选人']}</span>
                        <span style="color: {color}; font-weight: bold;">{result['匹配度']}</span>
                    </div>
                    <div style="color: #666; font-size: 0.9rem;">{result['技能']}</div>
                    <div style="color: #666; font-size: 0.9rem;">{result['期望薪资']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("点击「开始智能匹配」查看结果")

# ==================== 数据分析 ====================
elif page == "📊 数据分析":
    st.markdown('<div class="main-header"><h1>📊 数据分析</h1></div>', unsafe_allow_html=True)
    
    # 技能云图
    st.subheader("🔤 技能分布")
    all_skills = []
    for c in store.candidates:
        all_skills.extend(c.get('skills', []))
    
    from collections import Counter
    skill_counts = Counter(all_skills).most_common(10)
    
    if skill_counts:
        skill_df = pd.DataFrame({
            '技能': [s[0] for s in skill_counts],
            '数量': [s[1] for s in skill_counts]
        })
        
        fig = px.bar(skill_df, x='技能', y='数量', title="热门技能TOP10",
                     color='数量', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    # 薪资分析
    st.subheader("💰 薪资分布")
    if store.candidates:
        salaries = [c['expected_salary'] for c in store.candidates]
        
        fig = px.histogram(
            x=salaries,
            nbins=10,
            title="候选人期望薪资分布",
            labels={'x': '薪资（元/天）', 'y': '人数'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 导出数据
    if st.button("📥 导出分析报告", use_container_width=True):
        st.success("报告已生成！")

# ==================== 设置 ====================
else:
    st.markdown('<div class="main-header"><h1>⚙️ 设置</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 数据管理")
        if st.button("💾 备份数据", use_container_width=True):
            store.save_all()
            st.success("数据已保存！")
        
        if st.button("🔄 重置数据", use_container_width=True):
            if st.checkbox("确认重置所有数据？"):
                store.jobs = store._default_jobs()
                store.candidates = store._default_candidates()
                store.contracts = store._default_contracts()
                store.save_all()
                st.success("数据已重置！")
                st.rerun()
    
    with col2:
        st.subheader("⚙️ 应用设置")
        theme = st.selectbox("主题", ["亮色", "暗色"])
        language = st.selectbox("语言", ["中文", "English"])
        
        if st.button("保存设置", use_container_width=True):
            st.success("设置已保存！")

# 页脚
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 灵活用工平台 | 版本 2.0")
