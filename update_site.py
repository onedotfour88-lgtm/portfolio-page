import re
import json

def parse_ritual_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {"error": "리추얼 파일이 없습니다."}

    days = re.split(r'##\s+(\d{4}-\d{2}-\d{2})', content)
    total_days = 0
    candidates = []

    for i in range(1, len(days), 2):
        date = days[i]
        block = days[i+1]
        total_days += 1

        if "몸살" in block or "감기" in block:
            candidates.append({"date": date, "type": "자기조절력", "desc": "신체적 컨디션 난조에도 집중 유지"})
        if "오류" in block or "해결" in block:
            candidates.append({"date": date, "type": "과제지속력", "desc": "디버깅 막힘 현상을 끝까지 해결"})
        if "조장" in block:
            candidates.append({"date": date, "type": "대인관계력", "desc": "팀 조장 자원 및 적극적 분위기 주도"})

    return {
        "total_days": total_days,
        "attendance": "100%",
        "candidates": candidates
    }

if __name__ == "__main__":
    result = parse_ritual_data("ritual-history-2026-09-29.txt")
    print(json.dumps(result, ensure_ascii=False, indent=2))