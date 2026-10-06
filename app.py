import os
import json
import subprocess
import webbrowser
from threading import Timer
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'portfolio_data.json')

DEFAULT_DATA = {
    "story": "여기에 본인의 성장 이야기를 작성하세요.",
    "paper_title": "10번 논문 제목",
    "paper_desc": "논문 연구 요약입니다.",
    "paper_links": ["https://github.com"],
    "app_title": "13번 앱 (준비 중)",
    "app_desc": "프로젝트 상세 설명입니다.",
    "app_links": ["https://"],
    "name": "이시헌",
    "contact": "010-0000-0000 / email@example.com",
    "age": "20대",
    "job": "소프트웨어 개발 / AI 엔지니어링",
    "resume_body": "고난 속에서도 포기하지 않고 문제를 해결해내는 개발자 이시헌입니다."
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "paper_link" in data and "paper_links" not in data:
                    data["paper_links"] = [data["paper_link"]] if data["paper_link"] else []
                if "app_link" in data and "app_links" not in data:
                    data["app_links"] = [data["app_link"]] if data["app_link"] else []
                return data
        except Exception:
            return DEFAULT_DATA
    return DEFAULT_DATA

@app.route('/')
def home():
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return render_template_string(f.read())
    return "<h1>index.html 파일을 찾을 수 없습니다.</h1>"

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def save_data():
    try:
        new_data = request.json
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "success", "message": "로컬 저장 완료!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🚀 클릭 한 번으로 Git Push 수행하는 API
@app.route('/api/git-push', methods=['POST'])
def git_push():
    try:
        repo_dir = os.path.dirname(__file__)
        
        # 1. git add .
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
        
        # 2. git commit -m "update portfolio data"
        # 변경사항이 없을 때 에러가 나는 것을 방지하기 위해 check=False 처리
        subprocess.run(["git", "commit", "-m", "update: 포트폴리오 데이터 자동 반영"], cwd=repo_dir, check=False)
        
        # 3. git push origin main
        result = subprocess.run(["git", "push", "origin", "main"], cwd=repo_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "GitHub 푸쉬 성공! 잠시 후 다른 사람에게도 최신 데이터가 보입니다."})
        else:
            # master 브랜치 시도
            result_master = subprocess.run(["git", "push", "origin", "master"], cwd=repo_dir, capture_output=True, text=True)
            if result_master.returncode == 0:
                return jsonify({"status": "success", "message": "GitHub 푸쉬 성공 (master)!"})
            return jsonify({"status": "error", "message": f"Push 실패: {result.stderr}"}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 이시헌 포트폴리오 (Git 자동 푸쉬 연동) 서버 시작")
    print("웹 브라우저 주소: http://127.0.0.1:5000/")
    print("=" * 50)
    
    Timer(1.2, open_browser).start()
    app.run(port=5000, debug=False)