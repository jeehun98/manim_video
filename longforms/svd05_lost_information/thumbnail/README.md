# SVD 미니멀 썸네일

사용자 요청에 따라 이미지 생성 모델 대신 좌표·벡터·수식·글자를 코드로 배치했다. 기존의 좌측 제목과 우측 U | Σ | Vᵀ 구성을 유지한다.

```powershell
python longforms/svd05_lost_information/thumbnail/thumbnail_minimal.py
```

출력: exports/svd_thumbnail_minimal.png 및 exports/svd_thumbnail_minimal.svg. 1920×1080. SVG에는 실제 편집 가능한 text, polyline, polygon 요소가 들어 있다. 설치된 Malgun Gothic Regular와 Georgia를 사용한다. 다른 컴퓨터에서 SVG를 열 때 해당 폰트가 필요하며, PNG는 폰트 설치와 무관하게 동일하게 표시된다. Python 소스에서 모든 문구·좌표·색·크기를 변경할 수 있다.

PNG는 SVG와 같은 좌표와 폰트로 그린 뒤 3배 슈퍼샘플링을 적용한다. 새 이미지를 생성하거나 기존 생성 이미지를 덧칠하지 않았다. 입력·출력 기저는 서로 다른 회전행렬로 계산하며 각각 QᵀQ=I를 검사한다. 두 기저 벡터의 표시 길이는 모두127px. Σ의 막대는 특잇값(1.6,0.8)에 비례하여144px와72px로 그린다. 각도 수치·세로 구분선·작은 원/타원 아이콘·하단 장식 문구는 생략한다.

검수: 1920px 원본 및 preview_480.png에서 제목·여백·정렬과 가독성을 확인했다. 수치 검증과 텍스트 경계는 geometry_check.json에 기록한다.

## 추가 수정 v2

`python longforms/svd05_lost_information/thumbnail/thumbnail_minimal_v2.py`

기존 파일은 보존하고 exports/svd_thumbnail_minimal_v2.png 및 .svg를 만든다. SVD 라벨을34px에서56px로 확대했다. 우측 하단의 원과 타원은 동일한56px 단위 척도이며, 위의 U·Σ·V와 동일한 A=UΣVᵀ를 단위원의 각 점에 적용해 계산했다. 타원의 반축은89.6px와44.8px, 장축 방향은30도다. 원본 크기와 preview_v2_480.png를 검수했으며 geometry_check_v2.json에 계산을 기록한다.

## 벡터 연결 v3

`python longforms/svd05_lost_information/thumbnail/thumbnail_minimal_v3.py`

exports/svd_thumbnail_minimal_v3.png 및 .svg. 상단의 A 뒤와 우변 Vᵀ 뒤에 같은 cyan의 작은44px x를 붙여 등식 Ax=UΣVᵀx를 정확하게 유지했다. Vᵀ 구성요소 옆에도34px x를 덧붙였다. 주된 행렬 기호는 기존 크기를 유지하고, 설명을 결과 방향 / 반응 크기 / 기준 방향과 사용자 제공 보조 문장으로 변경했다. 원본과480px 축소 상태에서 검수했으며 이전 버전은 보존했다.
