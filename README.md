# Git Commit Rules

## Format

모든 커밋은 아래 형식을 따른다
**<type>(optional scope): <subject>**

## Types

- feat: 새로운 기능 추가
- fix: 버그 수정
- refactor: 동작 변경 없는 코드 구조 개선
- perf: 성능 개선
- test: 테스트 추가/수정
- docs: 문서만 변경
- chore: 빌드/설정/패키지/스크립트 등 기타 작업
- ci: CI 설정 변경(GitHub Actions 등)
- style: 포맷/린트 등 코드 스타일 변경(로직 변경 없음)

## Scopes

- data : 데이터 로딩/전처리/스플릿/인덱싱
- model : 모델 로직(ALS, popularity 등)
- metrics : 평가 지표
- pipeline : prepare/train/evaluate 파이프라인
- conf : Hydra config(yaml)
- scripts : 실행 스크립트
- tests : 테스트
- repo : 리포지토리 설정(ruff, gitignore 등)
