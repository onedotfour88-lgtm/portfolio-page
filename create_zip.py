import zipfile
import os

files_to_zip = {
    "index.html": """<!-- index.html 내용 생략 (위의 1번 파일 소스가 들어갑니다) -->""",
    "update_site.py": """# update_site.py 내용 생략 (위의 2번 파일 소스가 들어갑니다)""",
    "README.md": "# 이시헌 포트폴리오 프로젝트\n\n1. `index.html`을 라이브 서버로 열어 확인하세요.\n2. Word 추출 기능은 상단 버튼으로 구동됩니다."
}

# zip 파일 생성
zip_name = "portfolio_vscode.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for filename, content in files_to_zip.items():
        zipf.writestr(filename, content)

print(f"성공적으로 {zip_name} 파일이 생성되었습니다!")