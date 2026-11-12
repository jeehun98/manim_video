# EP.05 · 프랑크–헤르츠 실험

사용자 확정 24문장·122초, 전체 문장 자막·무음. 9:16 1080×1920와 16:9 1920×1080, 30fps, 각 3660프레임. 음원 미제공.

## 제작과 실행

`script.json`은 대본·문장 종료 시각의 원본이다. 대본·brief·씬별spec을 먼저 확정했다. 6개 씬 길이는6 + 18 + 18 + 25 + 24 + 31초. 공통 `shared/build.py`는 자막·씬 렌더·프레임 검사·조립·디코딩·검수시트, `shared/chapter_scene.py`는 시간·자막 처리를 담당한다. 편별 `direction.py`는 연출,`layouts.py`는 배치,`apparatus.py`는 도형,`experiment_model.py`는 계산이다. EP.04의 BohrAtom을 재사용하며 수은과 수소를 구분한다.

```powershell
.venv/Scripts/python.exe quantum_series/episodes/ep05_franck_hertz/build.py --preview --stills
.venv/Scripts/python.exe scripts/render.py quantum05 --preview
.venv/Scripts/python.exe quantum_series/episodes/ep05_franck_hertz/build.py --preview --inspect
.venv/Scripts/python.exe quantum_series/episodes/ep05_franck_hertz/build.py --inspect
```

단일 씬: `--scene 04_collision --layout shorts` (같은 품질·종료 모드 나머지 MP4가 있어야 조립 가능). 기본 쇼츠 standalone / 가로 join. 두 모드 모두122초를 유지하고121–122초 정지한다. 별도 복습·예고·엔드카드 없음. `--stills`는 씬 끝 대표 프레임만 생성하므로 최초 레이아웃 검수에 사용한다. 이후 동작 중 주요 시각은 전체 미리보기의 작은contact sheet로 확인한다.

출력: `exports/quantum05_shorts.mp4`,`exports/quantum05_longform.mp4`,각 `_ending.png`;미리보기는`_preview.mp4`. 중간 클립과 로그·검수 이미지는`media/quantum05/`.

## 물리적 조건과 한계

- 전위차U(V),전자 운동에너지K(eV),수은의 대표 들뜸 차이ΔE≈4.9eV를 독립적으로 관리한다. 전자 한 개의 가속 에너지 증가ΔK=eΔU,표시 단위eV에서는수치상ΔK=ΔU. 충돌은K≥4.9eV일 때가능하며K가4.9eV감소한다. 문턱을 넘은 모든 전자가 반드시 충돌한다는 뜻이 아니다.
- 예시K=5.2→0.3eV,속도비sqrt(0.3/5.2)≈0.24. 낮은 에너지에서도 탄성 충돌과 방향 변화는 가능하다. 원자 기호는 공간에 고정하고 내부 상태만높인다. 원자·전자 크기와경로는실제축척이 아니다.
- 감속 전위차 예시0.8V는 실측값이 아니다. K=0.3eV인 전자가 이를넘지못하고격자–검출부사이에서반전한다. 감속 구간은금속벽이아니다. 재가속은음극–격자에서만발생한다. 여러전자중일부는도달해전류가0이되지않는다. 대표경로·점개수는실제충돌확률·전류를수치모사하지않는다.
- 전류곡선은관측된형태를설명하는부드러운개념도이며실측이나수송시뮬레이션자료가아니다. 상대전류단위와임의절대전압오프셋을사용한다. 최솟값6.0/10.9/15.8V의간격만4.9V로설계하며첫최소를정확히4.9V라고주장하지않는다. 실제곡선은접촉전위·밀도·충돌단면적·방출조건·감속전압에의존한다.
- 이온화에너지와4.9eV의대표들뜸을구분한다. 수은에는다른준위와준안정상태도있으며그전체구조를두선으로축약한것이아니다. 전자는계속존재하고원자를들뜨게할때운동에너지를잃는다.
- UV253.7nm와그에대응하는hc/λ≈4.887eV는약4.9eV로연결된다. 4.9라는반올림값으로253.7nm를정밀하게역산했다고표현하지않는다. 보라색파동은비가시자외선의식별용이며UV라벨을함께표시한다.
- 설명은현대물리학의해석이다. 1914년최초발표때부터보어가정을의도적으로검증한것처럼연출하지않는다. 사진은사용하지않는다. 흡수는전자충돌에의한내부에너지전달이며빛흡수실험과동일시하지않는다.

자료: [유타대학교 실험 안내](https://web.physics.utah.edu/~detar/phys6720/handouts/fh/franck_hertz.html),[프랑크 노벨 강연](https://www.nobelprize.org/uploads/2018/06/franck-lecture.pdf),[헤르츠 노벨 강연](https://www.nobelprize.org/uploads/2018/06/hertz-lecture.pdf).
