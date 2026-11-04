# 07 복권 가설 — 구조와 초기값의 조합

사용자 확정 대본170초·35개 문장 종료 시각·16개 독립 씬. 세로9:16과 가로16:9를 제작한다. 이번 사용자가 앞선 사례를 요약하는 대본을 명시적으로 제공했으므로 도입부는 그 요청을 따른다. 이후 영상 예고는 추가하지 않는다. 음원 미제공으로 자막 포함 무음 영상과 TTS 원고 제공.

## 논문과 설명용 실험의 구분

근거: [Frankle & Carbin, The Lottery Ticket Hypothesis](https://arxiv.org/abs/1803.03635). 최초 공개2018-03-09, ICLR2019. 학습→가지치기→생존 가중치를 원래 초기값으로 복원→마스크 고정 재학습이 핵심이다. 원논문은 여러 구조·데이터·학습 설정의 실험이며, 원래 초기값의 중요성과 적용 조건을 다룬다. 모든 희소망을 winning ticket이라고 하거나 보편적인 최소망·최소 자유도를 증명했다고 표현하지 않는다.

영상의 가중치와 곡선은 원논문 수치가 아닌 직접 계산한 작은 XOR 설명 실험이다. 원논문 재현이 아니며 화면에도 표시한다. 원논문의 최소 검증 손실에 따른 조기 종료 기준과 이 설명용 목표95%는 다르다. 본 예시로 원논문의 정량적 압축률이나 일반성을 입증하지 않는다.

## 계산 조건

- 합성 XOR: 학습256개, 독립 테스트512개, 시드17/18. 2→6→4→2 tanh MLP, 연결 가중치44개와 바이어스12개.
- Full-batch Adam, 학습률0.02,300회. 초기값 시드707, 새 무작위 초기값 시드708. 두 경우 같은 분포·마스크·데이터·옵티마이저·학습 설정. 바이어스는 모두 보존하며 재학습 시0으로 복원, 영상의 연결 수에는 포함하지 않는다.
- 전체망 학습 후 연결 가중치 절대값 상위33개 선택. 고정 마스크 M을 유지하고 부분망의 생존 연결은 M⊙W0로 복원. 모든 스텝에서 제거 연결은 정확히0.
- 테스트 정확도95% 최초 도달: 전체망30회, 원래 초기값 부분망26회, 새 초기값 부분망21회. 영상은 초기60회의 실제 곡선을 보여준다. 새 초기값이 초반에 더 빠르므로 원래 초기값의 보편적 우월성으로 표현하지 않는다.
- 300회 후 테스트 정확도: 전체망100%, 원래 초기값 부분망100%, 새 초기값 부분망약99.0%. 학습된 전체망을33개 연결로 가지치기한 직후에도 이 예시에서는100%.
- 예비50% 보존 설정은 부분망이 약73%에 머물러 실패했다. pilot_report.json에 보존. 설명 가능한 학습 사례를 위해75% 보존을 사용했다. 시드 반복 탐색이나 통계적 일반성 검정은 하지 않았다.
- 이 예시는 성능·학습 경로를 설명하기 위한 것이며 원논문식 winning-ticket 발견의 엄밀한 재현으로 명명하지 않는다. 영상의 Winning Ticket 표기는 비교 조건을 만족하는 부분망의 개념을 설명한다.

experiment_data.npz에 초기·학습 후·새 초기값·마스크·전체 학습 이력·곡선, experiment_report.json에 설정과 결과, math_verification.json에 마스크·복원·비활성 가중치 검증을 기록한다.

## 재현

```powershell
python longforms/minimal07_lottery/data_model.py
python longforms/minimal07_lottery/build.py --preview
python longforms/minimal07_lottery/build.py
python longforms/minimal07_lottery/verify_caption_boundaries.py --layout shorts
python longforms/minimal07_lottery/verify_caption_boundaries.py --layout longform
```

Python3.12·NumPy·Manim0.21·FFmpeg/FFprobe·Malgun Gothic. 화면 수식은 Text를 사용하며 LaTeX 불필요. narration_timing.json은 확정 시각, narration.md는 원문, tts_script.txt는 발음 원고다. 문장 자막은 최종 concat 후 단일 ASS 트랙으로 합성한다.

출력: exports/minimal07_170s_shorts_final.mp4 (1080×1920), exports/minimal07_170s_longform_final.mp4 (1920×1080). 각170초·30fps. 미리보기는 _preview.mp4.

## 완료 상태

두 비율 최종본과 미리보기 완료. 길이·프레임 수·전체 디코딩, 총210프레임의 자막 경계, 주요 화면 검토 통과. verification_final.json과production_notes.md에 결과 기록.
