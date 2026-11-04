# EP.01 · 뜨거운 물체의 빛은 어떻게 계산할까?

사용자 확정 대본·16개 문장 종료 시각 기준 **86초**, 30fps, 무음·전체 문장 자막.
9:16은 1080×1920, 16:9는 1920×1080으로 각각 배치하여 렌더한다.

## 소스와 제작 단계

`longforms/_template/`의 대본·씬 인덱스·씬 spec 규격을 바탕으로 사용자 요청의 `quantum_series/` 구조에 배치했다. `script.json`이 대본·타이밍의 원본이며, `direction.py`의 4개 클래스는 동일한 애니메이션을 공유하는 두 화면비를 지원한다. `scenes/`에는 주장별 spec과 TTS 원문이 있다. 각 클래스는 독립 MP4로 렌더·교체하고 최종 concat한다.

화면 제작 전 확정된 길이: 01=24초, 02=25초, 03=23초, 04=14초. 모든 길이는 사용자 문장 종료 시각으로 확정했으며 추정하지 않았다. 음원은 미제공이다.

## 실행

```powershell
python quantum_series/episodes/ep01_planck/build.py --preview
python quantum_series/episodes/ep01_planck/build.py
python quantum_series/episodes/ep01_planck/build.py --layout shorts
python quantum_series/episodes/ep01_planck/build.py --layout longform
```

두 화면비의 기본 종료 모드는 shorts=standalone, longform=join이다. `--ending standalone` / `--ending join`으로 바꿀 수 있다. 두 모드 모두 86초 대본을 전부 유지하며 별도 엔드카드는 없다. standalone은 마지막 빛을 조금 낮추고 1초간 정지한다. join은 빛의 밝기와 프레임을 유지한다.

한 씬만 수정할 때는 동일 layout·ending·품질의 나머지 씬들이 존재하는 상태에서 다음처럼 실행한다.

```powershell
python quantum_series/episodes/ep01_planck/build.py --layout shorts --scene 03_energy
```

중간 MP4와 로그는 `media/quantum01/<layout>/<ending>/<quality>/`에 있다. 최종 파일은 `exports/quantum01_shorts.mp4`, `exports/quantum01_longform.mp4`. 각 씬의 프레임 수와 최종 2580프레임·86초·해상도·30fps를 빌드에서 검사한다.

## 물리 표현

- 그래프는 파장 λ(μm)에 따른 흑체 스펙트럼 복사휘도 Bλ를 최대값으로 정규화한 상대값이다. T=1500 K, 고정 온도·고정 정규화. 가로축을 진동수로 바꾸지 않는다.
- 빈 법칙: `2hc² / λ⁵ × exp(-hc/(λkT))`; 플랑크 법칙: `2hc² / λ⁵ / expm1(hc/(λkT))`. 5–12 μm 확대에서는 세로축을 확대하고 수치 눈금을 명시한다.
- 실측 점을 사용하지 않는다. 청록색 곡선·점은 모두 플랑크 법칙으로 계산한 이론적 기준 분포이며 화면에 이를 표시한다. 관측 분포에 대한 역사적 설명과 그래프의 데이터 출처를 구분한다.
- 실제 쇠의 방사율을 측정한 자료가 아니므로 그래프에 ‘흑체 근사’를 표시한다.
- 황금색 블록은 동일한 진동수의 진동자에 분배하는 에너지량의 계산 기호이며 전자·광자·공간의 분절을 뜻하지 않는다. 6개 블록을 `[3,2,1,0] → [2,2,1,1] → [0,1,3,2]`로 재분배하며 총량을 보존한다.
- 플랑크의 1900년 계산과 1905년 광양자 가설을 구분한다. 과거의 계산상의 단위를 현대 광자로 확정하여 그리지 않는다.

출처: [플랑크 노벨 강연](https://www.nobelprize.org/prizes/physics/1918/planck/lecture/), [NIST 스펙트럼 복사휘도 교정](https://www.nist.gov/system/files/documents/pml/div685/pub/sp250-1.pdf).
