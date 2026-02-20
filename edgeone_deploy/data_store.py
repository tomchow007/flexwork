import json
import os
from datetime import datetime

class DataStore:
    """数据存储类 - 负责所有数据的持久化"""
    
    def __init__(self, data_dir="web_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.jobs_file = os.path.join(data_dir, "jobs.json")
        self.candidates_file = os.path.join(data_dir, "candidates.json")
        self.contracts_file = os.path.join(data_dir, "contracts.json")
        
        self.load_data()
    
    def load_data(self):
        """加载所有数据"""
        self.jobs = self._load_file(self.jobs_file, self._default_jobs())
        self.candidates = self._load_file(self.candidates_file, self._default_candidates())
        self.contracts = self._load_file(self.contracts_file, self._default_contracts())
    
    def _load_file(self, filepath, default):
        """加载单个文件"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return default
    
    def save_all(self):
        """保存所有数据"""
        self._save_file(self.jobs_file, self.jobs)
        self._save_file(self.candidates_file, self.candidates)
        self._save_file(self.contracts_file, self.contracts)
    
    def _save_file(self, filepath, data):
        """保存单个文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存失败 {filepath}: {e}")
    
    def _default_jobs(self):
        """默认职位数据"""
        return [
            {
                "id": "job_001",
                "title": "前端开发工程师",
                "salary": "300-500元/天",
                "location": "远程",
                "skills": ["React", "Vue", "JavaScript"],
                "description": "负责Web前端开发",
                "status": "招聘中",
                "created": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "id": "job_002",
                "title": "UI设计师",
                "salary": "250-400元/天",
                "location": "上海",
                "skills": ["Figma", "Photoshop", "UI/UX"],
                "description": "负责产品界面设计",
                "status": "招聘中",
                "created": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    
    def _default_candidates(self):
        """默认候选人数据"""
        return [
            {
                "id": "cand_001",
                "name": "张三",
                "skills": ["Python", "React", "JavaScript"],
                "experience": 3,
                "expected_salary": 400,
                "status": "可联系",
                "phone": "13800138000",
                "email": "zhang@example.com"
            },
            {
                "id": "cand_002",
                "name": "李四",
                "skills": ["UI/UX", "Figma", "Photoshop"],
                "experience": 5,
                "expected_salary": 350,
                "status": "可联系",
                "phone": "13900139000",
                "email": "li@example.com"
            }
        ]
    
    def _default_contracts(self):
        """默认合同数据"""
        return [
            {
                "id": "contract_001",
                "job_id": "job_001",
                "candidate_id": "cand_001",
                "job_title": "前端开发工程师",
                "candidate_name": "张三",
                "start_date": "2024-02-01",
                "end_date": "2024-05-01",
                "salary": 400,
                "status": "执行中",
                "total_amount": 48000
            }
        ]
    
    def add_job(self, job_data):
        """添加职位"""
        job_data["id"] = f"job_{len(self.jobs) + 1:03d}"
        job_data["created"] = datetime.now().strftime("%Y-%m-%d")
        self.jobs.append(job_data)
        self.save_all()
        return job_data["id"]
    
    def add_candidate(self, candidate_data):
        """添加候选人"""
        candidate_data["id"] = f"cand_{len(self.candidates) + 1:03d}"
        self.candidates.append(candidate_data)
        self.save_all()
        return candidate_data["id"]
    
    def add_contract(self, contract_data):
        """添加合同"""
        contract_data["id"] = f"contract_{len(self.contracts) + 1:03d}"
        self.contracts.append(contract_data)
        self.save_all()
        return contract_data["id"]
    
    def get_stats(self):
        """获取统计数据"""
        return {
            "total_jobs": len(self.jobs),
            "active_jobs": len([j for j in self.jobs if j["status"] == "招聘中"]),
            "total_candidates": len(self.candidates),
            "available_candidates": len([c for c in self.candidates if c["status"] == "可联系"]),
            "total_contracts": len(self.contracts),
            "active_contracts": len([c for c in self.contracts if c["status"] == "执行中"]),
            "total_amount": sum(c.get("total_amount", 0) for c in self.contracts)
        }
