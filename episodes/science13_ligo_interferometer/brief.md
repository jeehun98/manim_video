# 제작 기준 — LIGO는 시공간의 흔들림을 어떻게 측정했을까

- 목표: 중력파의 존재 자체보다 `팔 길이 변화 → 빛의 위상 차이 → 간섭광 변화`라는 LIGO의 측정 변환 구조를 움직임으로 이해시킨다.
- 14장면, 106초, 세로 1080×1920 / 30fps / 무음. 사용자가 제공한 TTS 누적 시각을 장면 경계로 사용한다.
- 단순화한 Michelson 간섭계 도식을 사용한다. 실제 LIGO의 Fabry–Pérot 공동, 다중 반사, power/signal recycling, 제어계와 두 관측소의 coincidence 분석은 생략한다.
- 두 팔은 각각 4 km다. 그림의 팔 길이와 변형량은 화면 가독성을 위해 실제 비율과 다르며, stretch/squeeze는 극단적으로 과장한다.
- 중력파가 거울에 일반적인 기계적 힘을 가해 미는 그림이 아니라, 자유낙하하는 시험질량 사이의 시공간 간격이 변하는 그림으로 표현한다.
- 기본 도식에서는 같은 광원에서 나뉜 두 빛이 왕복 후 재결합한다. 평상시 출력 포트는 destructive interference에 가깝고, 차동 팔 길이 변화가 위상차와 광신호를 만든다.
- strain은 `h = ΔL/L`로 정의한다. GW150914급 신호의 대표 규모를 `h ~ 10^-21`로 표시하며, 4 km에 대응하는 길이 변화가 양성자 폭보다 훨씬 작다는 비교만 사용한다.
- 2015년 9월 14일 최초 직접 관측, 두 블랙홀의 inspiral–merger–ringdown과 주파수·진폭이 증가하는 chirp를 연결한다.
- LIGO는 전자기파를 보는 망원경이 아니다. 시공간의 파동을 측정해 중력파 천문학이라는 새로운 관측 채널을 열었다는 결론으로 끝낸다.

## 근거

- LIGO Lab, What is an Interferometer?: https://www.ligo.caltech.edu/LA/page/what-is-interferometer
- LIGO Lab, LIGO — A Gravitational-Wave Observatory: https://www.ligo.caltech.edu/page/ligo-gw-interferometer
- LIGO Lab, First detection announcement: https://www.ligo.caltech.edu/MIT/news/ligo20160211
- LIGO Lab, LIGO Fact Sheet: https://www.ligo.caltech.edu/system/media_files/binaries/300/original/LIGO_Fact_Sheet_DHS_update_2022.pdf
- Nobel Prize, Physics 2017 press release: https://www.nobelprize.org/prizes/physics/2017/press-release/

## 검증

- 미리보기에서 간섭 전후의 밝기 변화, stretch/squeeze 방향, 파형의 chirp, 한글과 세로 안전영역을 확인했다.
- 장면 경계: 0, 9, 17, 25, 31, 39, 46, 52, 58, 66, 73, 80, 87, 94, 106초.
- 최종본 `exports/science13.mp4`: 1080×1920, 30fps, 3,180프레임, 105.997982초, 비디오 스트림 1개·오디오 스트림 없음.
