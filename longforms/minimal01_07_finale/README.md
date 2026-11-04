# 01–07 통합 마무리

163초, 1920×1080 30fps, 롱폼 전용. 음원 미제공으로 무음·자막. 사용자 확정 문장 종료 시각을 그대로 사용.

실행: `python longforms/minimal01_07_finale/build.py --preview` → `python longforms/minimal01_07_finale/build.py`

검증: `python longforms/minimal01_07_finale/verify_caption_boundaries.py --layout longform`

기존07의 시각 요소·실험 데이터와 기존02–07 화면 프레임 재사용. 각 씬의 spec.md에 조건 기록. 원본 에피소드 소스는 변경하지 않음.

## 완료 상태

최종 출력: `exports/minimal01_07_finale_163s_longform_final.mp4`

163.000초·4,890프레임·1920×1080·30fps 검증 완료. H.264, 무음. 33문장의 경계 전후 99프레임에서 단일 자막 참조와 비교 통과(최소 텍스트 마스크 IoU 0.9781). 주요20시점 및 수정된 마지막 씬 시각 검토 완료.
