# EP.04 · 보어 모형과 원자의 안정성

사용자 제공 확정 대본 **23문장·113초**, 30fps, 전체 문장 자막. 음원 미제공으로 무음이다. 9:16 1080×1920 / 16:9 1920×1080을 독립 배치한다.

## 제작 구조

`script.json`은 대본·문장 종료 시각의 원본이다. 대본과 씬 spec을 먼저 고정한 뒤 제작했다. `direction.py`는 공통 애니메이션, `layouts.py`는 화면비별 좌표, `shared/bohr.py`는 도형과 수소 에너지·파장 계산을 담당한다. 씬별 `scene.py`로 독립 렌더·교체한다.

- 0–7초: 핵·전자 전하와 인력, 안정성 질문.
- 7–34초: 원운동의 속도 방향과 중심 가속도, 복사와 나선, 실제 안정성 대비.
- 34–55초: 1913 보어, 연속 궤도 후보 제거, 비복사 정상상태 가정.
- 55–71초: 수소 방전관, 연속 스펙트럼과 선 스펙트럼.
- 71–95초: 비등간격 준위, 3→2와 4/5/6→2의 전이·빛, 관측과 계산 비교.
- 95–113초: 허용 상태의 이유라는 미해결 질문. 마지막 112–113초 정지.

## 실행

```powershell
.venv/Scripts/python.exe scripts/render.py quantum04 --preview
.venv/Scripts/python.exe scripts/render.py quantum04
.venv/Scripts/python.exe scripts/render.py quantum04_shorts
.venv/Scripts/python.exe scripts/render.py quantum04_longform
```

직접 실행: `python quantum_series/episodes/ep04_bohr/build.py --layout both`.
한 씬 수정: `--scene 05_transitions --layout shorts` (같은 품질·종료 모드 나머지 MP4 필요).
쇼츠는 standalone, 가로는 join이 기본이며 `--ending`으로 변경 가능하다. 본문·자막·113초를 모두 유지한다. 예고·복습·구독 유도·별도 엔드카드 없음.

출력: `exports/quantum04_shorts.mp4`, `exports/quantum04_longform.mp4`, 각각 `_ending.png`. 미리보기는 `_preview.mp4`. 중간 영상·로그는 `media/quantum04/`에 있다. 빌더는 씬별 프레임 수, 최종 3390프레임·113초·30fps·해상도를 검사한다.

## 물리 조건·한계와 출처

- 핵의 크기, 전자 크기, 원형 궤도 반지름은 개념도이며 축척 비례가 아니다. 실제 첫 세 궤도의 반지름 비율 1:4:9를 재현하지 않으므로 화면에 명시한다. 원형 궤도는 역사적 보어 모형이며 현대 전자의 실제 경로가 아니다.
- 고전 나선은 복사 손실의 결과를 상징하며 복사 방정식을 수치 적분한 경로가 아니다. 방사 파동도 정확한 각도 분포가 아닌 에너지 방출 기호다. 전자 위치에서 접선 속도와 중심 가속도 화살표를 회전시킨다.
- 정상상태에서 복사하지 않는다는 것은 보어의 새 가정이다. 전자가 정지한다는 의미가 아니다. 안정적인 실제 원자 기호도 오비탈의 정량 모사가 아니다.
- 수소 준위 `E(n)=-13.598287/n² eV`, `hc=1239.841984 eV nm`로 진공 파장을 계산한다. 화면의 식 −13.6은 반올림이다. 준위 세로 위치는 실제 에너지에 선형 비례하며 높은 준위의 라벨은 연결선으로 분리한다.
- 전이 화살표는 에너지 상태 변화이며 공간 이동 경로가 아니다. 전자 기호는 높은 상태에서 사라지고 낮은 상태에 등장한다. n=3,4,5,6→2의 대표 가시광 선만 보여주며 다른 수소 방출선을 부정하지 않는다.
- 관측 대표값은 NIST의 공기 중 약 656.28, 486.13, 434.05, 410.17 nm, 계산은 단순 보어 모형의 진공 파장이다. 공기/진공·미세구조 차이를 동일시하지 않는다. 약 nm 단위 일치를 설명하며 완전한 정밀 측정 일치나 실측 강도를 재현하지 않는다. 선 높이·두께는 의미 없는 가독성 표시다.
- 스펙트럼은 400–700 nm의 동일 선형 파장축이다. 색은 화면용 근사이며 실제 분광 감도·밝기를 모사하지 않는다.
- 마지막 희미한 파동 호는 남은 질문을 나타내는 연결 요소이며 완성된 현대 오비탈이 아니다. 다음 편 소스나 음원을 생성된 것으로 표시하지 않는다.

자료: [NIST 수소 선 자료](https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2_a.htm), [NIST 미세구조 주석](https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable7.htm), [닐스 보어 연구소의 역사 자료](https://nbi.ku.dk/english/www/niels/bohr/bohratomet/).

## 검수 재실행

`python quantum_series/episodes/ep04_bohr/inspect_video.py --preview` / `python quantum_series/episodes/ep04_bohr/inspect_video.py`. 전체 디코딩, 프레임 수와 길이 확인 후 주요 시각의 PNG와 검수용 contact sheet를 `media/quantum04/qa/`에 저장한다. 실제 실행 결과는 `verification.json`, `physics_verification.json`, `render_report.json`을 참고한다.

검수 완료: 두 비율 미리보기와 최종 주요 프레임 시각 확인, 각 113초·3390프레임·30fps·지정 해상도, 두 최종 MP4 전체 디코딩 통과. 마지막 1초 정지 프레임 차이 검사 통과.
