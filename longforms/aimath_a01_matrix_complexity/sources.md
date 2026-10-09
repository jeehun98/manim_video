# 출처·검수 기록

확인일: 2026-10-09 (Asia/Seoul).

- S1: [OpenAI 공식 발표](https://openai.com/index/sharing-ai-progress-in-mathematics/) — 공개 배경.
- S2: [결과 목록 family 107](https://github.com/openai/math/blob/main/CONTENTS.md) — 복소수 위 ω≤9/4 및 Oε(n^(9/4+ε)) 공개 주장.
- S3: [형식화 범위](https://github.com/openai/math/blob/main/lean/docs/107.md) — 해당 상한의 형식화 보고. division-free 산술 모델이며 비트 복잡도·실용적인 교차 크기를 다루지 않는다고 설명한다. 직접 빌드하지 않았다.
- S4: [AlphaTensor 원 논문](https://www.nature.com/articles/s41586-022-05172-4) — Strassen 2×2의 7곱과 재귀적 행렬곱 배경. 2022년 논문의 당시 최신 지수를 현재 기록으로 쓰지 않는다. AlphaTensor의 탐색 방식과 이번 OpenAI 연구 방식을 동일시하지 않는다.
- S5: [저장소 수정 이력](https://github.com/openai/math/blob/main/history.md) — 출고 전 버전 재확인.

## 조사 한계와 보완할 사항

새 9/4 원고 PDF·TeX 접근이 실패했다. 새 증명의 핵심 기법, 보조정리 의존 관계, 독립 전문가 검토, 실용적 GPU 구현·성능은 미확인이다. 현재 초안은 확립된 예제를 통해 문제와 공개 상한의 의미를 설명한다. 새 접근의 고유한 직관은 원문 조사 후 별도 씬으로 보강한다.

형식화 문서는 주된 9/4 원고와 다른 동반 원고 제목을 연결하면서 더 강한 상한의 형식화를 설명한다. 따라서 특정 PDF 전체가 직접 검사됐다고 말하지 않는다. Lean 문서·코드·실제 빌드 결과를 추가 검토해야 한다.

## Strassen 공식 — 화면 제작 기준

A=[[a,b],[c,d]], B=[[e,f],[g,h]].

M1=(a+d)(e+h)
M2=(c+d)e
M3=a(f−h)
M4=d(g−e)
M5=(a+b)h
M6=(c−a)(e+f)
M7=(b−d)(g+h)

C11=M1+M4−M5+M7=ae+bg
C12=M3+M5=af+bh
C21=M2+M4=ce+dg
C22=M1−M2+M3+M6=cf+dh

C11 전개: ae+ah+de+dh+dg−de−ah−bh+bg+bh−dg−dh=ae+bg.

블록에서도 곱셈 순서를 유지한다. 공식 일곱 개를 한꺼번에 읽히려 하지 않는다. C11의 항 소거를 중심으로 보여준다.

## 복잡도 조건

- n은 정사각 행렬의 한 변. 표준 방법은 n³ 곱셈과 n²(n−1) 덧셈.
- Strassen: T(n)=7T(n/2)+O(n²), Θ(n^(log₂7)). 크기 2의 거듭제곱으로 설명. 일반 크기는 패딩 등으로 같은 점근 지수 유지.
- ω는 해당 체와 산술 모델에서 가능한 지수의 infimum. 엄밀한 정의는 화면 제작 전 재검수한다. ω≤9/4를 일률적인 O(n^2.25) 보장으로 읽지 않는다.
- 명시적인 n²개 출력을 생성하는 일반 산술 회로 모델에서 ω≥2. 단순 출력 읽기 비용으로 산술 하한을 증명했다고 설명하지 않는다.
- 곱셈 절약이 전체 연산 수 절약을 곧바로 뜻하지 않는다. 재귀 비용에는 덧셈·뺄셈을 포함한다.
- 정확한 산술 항등식과 부동소수점 오차·비트 복잡도는 별개다.

