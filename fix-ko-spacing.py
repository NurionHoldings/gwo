#!/usr/bin/env python3
"""Apply Korean spacing corrections across ko.json and HTML files."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Longer phrases first to avoid partial replacements
REPLACEMENTS = [
    ("조기발견과 지원연계", "조기 발견과 지원 연계"),
    ("조기발견", "조기 발견"),
    ("지원연계", "지원 연계"),
    ("이탈위험", "이탈 위험"),
    ("변경업무", "변경 업무"),
    ("운영체계", "운영 체계"),
    ("운영모델", "운영 모델"),
    ("운영성과", "운영 성과"),
    ("적응지원", "적응 지원"),
    ("초기지원", "초기 지원"),
    ("조기지원", "조기 지원"),
    ("후속점검", "후속 점검"),
    ("후속조치", "후속 조치"),
    ("후속확인", "후속 확인"),
    ("사례관리", "사례 관리"),
    ("정책지표", "정책 지표"),
    ("인력현황", "인력 현황"),
    ("인력알선", "인력 알선"),
    ("운영경로", "운영 경로"),
    ("위험신호", "위험 신호"),
    ("개선지점", "개선 지점"),
    ("기업관리", "기업 관리"),
    ("보고업무", "보고 업무"),
    ("안전확인", "안전 확인"),
    ("근무환경", "근무 환경"),
    ("작업지시", "작업 지시"),
    ("적응점검", "적응 점검"),
    ("적응지원", "적응 지원"),
    ("통합관리", "통합 관리"),
    ("통합운영", "통합 운영"),
    ("안전관리", "안전 관리"),
    ("정책보고", "정책 보고"),
    ("운영보고", "운영 보고"),
    ("근로기초", "근로 기초"),
    ("채용기업", "채용 기업"),
    ("해외근로자", "해외 근로자"),
    ("해외인력", "해외 인력"),
    ("위탁모델", "위탁 모델"),
    ("위탁업무", "위탁 업무"),
    ("재적응", "재적응"),  # keep
]


def apply_text(text: str) -> str:
    for old, new in REPLACEMENTS:
        if old == new:
            continue
        text = text.replace(old, new)
    return text


def walk_json(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = walk_json(v)
        return obj
    if isinstance(obj, list):
        return [walk_json(v) for v in obj]
    if isinstance(obj, str):
        return apply_text(obj)
    return obj


def main():
    ko_path = ROOT / "assets" / "locales" / "ko.json"
    data = json.loads(ko_path.read_text(encoding="utf-8"))
    ko_path.write_text(
        json.dumps(walk_json(data), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("updated", ko_path.name)

    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new = apply_text(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.name)

    for path in sorted(ROOT.glob("*.py")):
        if path.name == "fix-ko-spacing.py":
            continue
        text = path.read_text(encoding="utf-8")
        new = apply_text(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()
