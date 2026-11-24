# Knowledge Atlas

기존 Manim 저장소 안에서 독립적으로 실행하는 개인 지식 탐구 프로토타입. 개념 사이의 **주장, 성립 조건, 근거, 출처, 미확인 사항**을 읽고 탐색한다. 영상 제작 설정이나 Python 환경은 사용하지 않는다.

## 실행

Node.js 22.8 이상(검증 환경: 24.14.0), npm이 필요하다. PowerShell에서:

```powershell
cd C:\Users\as042\OneDrive\Desktop\manim_video\knowledge_atlas
npm ci
npm run dev
```

터미널에 표시되는 로컬 주소를 연다. 기본 주소는 http://127.0.0.1:5173 이며, 포트를 쓰고 있으면 다음 포트를 사용한다. 종료는 Ctrl+C.

```powershell
npm run validate
npm test
npm run build
npm run preview
```

`build`는 데이터 검증 → TypeScript 검사 → 정적 빌드를 실행한다. `preview`는 빌드된 앱을 로컬에서 확인한다. 빌드 결과는 `dist/`, 의존성은 `node_modules/`에 생성되며 Git에서 제외한다. `index.html`을 파일로 직접 열지 않는다.

## 탐색 방법

- 왼쪽 개념 검색은 이름·영문 ID·태그로 개념 인덱스를 좁힌다. 검색 결과를 누르면 해당 노트와 연결이 강조된다. 검색어 자체는 그래프를 잘라내지 않는다.
- 노드를 누르고 **선택 개념 중심**을 선택하면 주변을 1–3단계로 확장한다. 주변 탐색은 관계 방향과 무관하게 양 끝점을 따라가며, 선행 학습 경로 계산과는 다르다.
- 학문·학습 상태는 노드를, 관계 유형·검증 상태는 관계를 필터링한다. 여러 필터는 AND 조건이다. 관계 필터를 적용하면 해당 관계에 참여한 노드만 남긴다.
- 노드를 끌어 배치하고 빈 공간을 끌어 이동한다. 휠 또는 +/−로 확대·축소한다. **맞춤**으로 현재 그래프를 화면에 맞춘다.
- 연결선 또는 오른쪽의 관련 관계를 누르면 방향·주장·조건·근거·한계·출처를 읽을 수 있다. 점선은 탐구 후보이며, 연결 자체가 동치를 의미하지 않는다.
- 선택한 노트가 필터 밖에 있어도 상세 기록은 유지한다. 오른쪽 관련 관계 목록은 현재 필터와 관계없이 해당 개념의 모든 관계를 보여준다.
- **대본 열기**는 새 탭에서 실제 로컬 텍스트를 표시한다. dev/preview 서버는 sources/contents에 명시된 저장소 파일만 읽는다.

## 파일 구조

```text
knowledge_atlas/
  data/
    concepts.json       # 개념·구조·정리·방법·아이디어·현상·문제
    relations.json      # 독립적인 관계 기록
    sources.json        # 대본·외부 문헌 출처
    contents.json       # 개념과 제작 자료의 연결
    schema.json         # 전체 데이터의 JSON Schema
  src/
    main.tsx            # Graph View와 상세 노트
    model.ts            # 타입·표시 이름·색상
    graph.mjs           # 공유 탐색 질의
    validation.mjs      # 스키마·ID·참조·경로 검사
    style.css
  scripts/
    validate.mjs        # 저장소 파일 존재·수식까지 검사
    graph.test.mjs      # 탐색·검증 회귀 검사
  vite.config.mjs       # 개발·미리보기용 제한된 대본 읽기
```

## 데이터 추가·수정

UI 코드를 바꾸지 않고 `data/` JSON을 수정한다. 개발 서버에서는 변경이 반영되며, 빌드 결과에는 재빌드가 필요하다. 파일은 UTF-8로 저장한다.

1. 기존 이름·ID·설명을 검색해 중복 개념을 먼저 확인한다.
2. `sources.json`에 출처를 추가한다. 저장소 자료는 `kind: "repository"`, 저장소 루트 기준 `path`, 확인한 구간인 `locator`를 넣는다. 외부 문헌은 `kind: "external"`, `url`(http/https), 장·절 등 `locator`를 넣는다. 읽지 않은 문헌을 확인한 근거로 표시하지 않는다.
3. `concepts.json`의 기존 레코드 형식으로 개념을 추가한다. ID는 안정적으로 유지한다. `type`, `domain`, `tags`, `description`, `sourceIds`, `questions`, `learningStatus`를 기록한다. `formula`는 선택 사항이며 JSON 안에서는 TeX의 `\`를 `\\`로 이스케이프한다.
4. `relations.json`에 출발·도착 ID, 유형, 방향성, 설명, 조건, 근거, 출처, 구간, 한계, 질문을 기록한다. `directed: true`이면 유형을 **source에서 target으로** 읽는다. 예: `내적 공간 → 힐베르트 공간`은 `specialization`이다. `prerequisite`는 선행 개념에서 학습 대상으로 향한다.
5. 관계는 먼저 `verificationStatus: "proposed"`로 저장한다. AI 제안의 `provenance`는 `ai_suggestion`. 문헌을 실제 검토했다면 그에 맞게 `literature_review`로 바꾼다. 자동으로 `verified`로 올리지 않는다.
6. 제작 자료가 존재하면 `contents.json`에 실제 경로와 연결 개념 ID를 넣는다. `script_present`는 대본 존재만 의미한다. 영상 완료는 실제 확인 후 `completed`로 기록한다.
7. `npm run validate`와 `npm test`를 실행하고 Git diff에서 주장·조건·출처를 검토한다.

새로운 관계 유형/노드 유형/상태 자체를 추가할 때는 스키마와 `model.ts`도 확장한다. 새 학문 분야와 태그는 자유 문자열이므로 코드 변경이 필요 없다. 알 수 없는 분야는 기본 색상으로 표시된다.

### 독립적인 두 상태

| 구분 | 값 |
| --- | --- |
| 자신의 이해 | `unassessed`, `learning`, `explainable`, `understood` |
| 관계의 근거 | `proposed`, `investigating`, `verified`, `rejected` |

`verified`는 출처가 있는 검토 기록에만 허용한다. 검증기는 AI 유래인 채로 검증 완료 처리하거나, 없는 출처·노드 참조, 중복 ID, 잘못된 상태, 허용하지 않은 경로가 있으면 실패한다. 설명의 수학적 참·거짓을 자동 판정하는 기능은 아니다.

## 초기 데이터의 범위와 검증

실제 읽은 대본 4개를 바탕으로 16개 개념·16개 관계를 구성했다.

- `episodes/basis01_fourier_heat/narration.md`: 푸리에 **급수**, 사인·코사인, 열방정식, 표현·분해 전략
- `longforms/hilbert/structure_short/narration.md`: 벡터 공간, 내적 공간, 내적, 직교성, 완비성, 힐베르트 공간
- `longforms/dot05_gram_schmidt_qr/narration.md`: 정사영, 그람–슈미트 과정
- `longforms/minimal04_sufficiency/narration.md`: 충분통계량, 우도, 목적에 따른 정보 축약

푸리에 급수를 푸리에 변환과 합치지 않았다. 관계는 조사 중 13개·탐구 후보 3개이며, 외부 문헌으로 검증 완료한 관계는 없다. 개인의 이해 상태는 추정하지 않아 모두 미평가다. 콘텐츠도 대본 파일 존재만 표시한다. 후보 목록의 나머지 개념은 실제 근거를 검토한 뒤 추가한다.

검증 결과: 데이터·참조 파일·수식 검사, TypeScript 및 프로덕션 빌드 통과. 자동 테스트 4개 통과. 브라우저에서 검색, 주변 탐색 깊이 변경, 관계 상세의 조건·출처 표시를 확인했다.

## 현재 한계와 다음 단계

- Graph View만 구현했다. Roadmap·Idea·Research는 동일 JSON과 공유 질의를 재사용하는 후속 범위이며 현재 구현된 메뉴로 표시하지 않는다.
- 화면 내 편집·저장, AI API, 인증, 데이터베이스, 클라우드는 없다. JSON을 직접 수정하거나 Codex에 수정 작업을 요청한다. Git으로 변경 이력을 관리한다.
- 드래그한 위치는 새로고침/필터 변경 시 유지되지 않는다. 검색은 키워드 검색이다.
- 외부 정적 호스팅에 `dist/`만 올리면 `/repository/` 링크는 동작하지 않는다. 로컬 dev/preview 서버를 사용하는 프로토타입이다.
- 초기 데이터는 저장소 전체를 자동 추출한 목록이 아니다. 대본의 존재는 출판·렌더 완료나 외부 수학적 검증을 뜻하지 않는다.
- 다음 단계는 실제 사용한 탐구 기록을 추가하고, 선행 관계만 따라가는 Roadmap 또는 미확인 관계를 모으는 Research View 중 필요가 큰 기능을 선택한다.

구현 참고: [Cytoscape API](https://js.cytoscape.org/), [Vite](https://vite.dev/guide/), [KaTeX API](https://katex.org/docs/api).
