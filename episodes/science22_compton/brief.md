# 과학 한조각 · 콤프턴 효과

- 사용자 대본 확정본과 문장 종료 시각을 그대로 사용. 136초, 9:16 쇼츠만 제작. 음원 미제공으로 무음.
- 질문: 정지질량이 없는 빛이 물체를 밀 수 있는가? 결론: 운동량을 전달하며, 광자 모델은 각도별 파장 이동을 정량적으로 설명한다.
- 실험 → 파장·에너지 → 고전 예측의 한계 → 광자·충돌 → 보존 법칙·정량적 검증 → 파동과 입자의 성질.
- 고전파도 에너지와 운동량을 전달한다. 한계는 정지 자유전자 톰슨 근사의 파장 이동 예측이다.
- 이동하지 않은 성분과 이동한 성분을 함께 제시. 스펙트럼은 개념도. 예측곡선 점은 이론식 표본이며 실측 자료가 아니다.
- 광자 파장 증가를 진폭 감소로 표현하지 않는다. 충돌 도형은 λ=71 pm, θ=60°의 상대론적 운동량 방향을 반영하며 길이·속력은 도식이다.
- 당구공은 전달의 비유다. 파동/입자는 서로 다른 성질의 표현이며 두 물체의 합성이 아니다.
- 11개 독립 Scene, 공유 테마와 wave 재사용. 발화와 종료시간 유지, 별도 엔드카드·다음 편 예고 없음.

실행: `python episodes/science22_compton/build.py --preview`, `python episodes/science22_compton/build.py`.
변경 구간 확인: `--scene shift energy prediction`.

근거:
- https://journals.aps.org/pr/abstract/10.1103/PhysRev.21.483
- https://journals.aps.org/pr/abstract/10.1103/PhysRev.22.409
- https://openstax.org/books/university-physics-volume-3/pages/6-3-the-compton-effect

자막 전환 수정: Scene updater에서 자막을 제거·추가하던 방식을 폐기하고, 지속되는 VGroup의 mobject updater로 매 프레임 갱신한다. Cairo 정적 배경에 이전 자막이 남지 않게 한다. `verify_captions.py`는 문장 경계 전후의 자막 픽셀을 깨끗한 기준 이미지와 비교한다.
