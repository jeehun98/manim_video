# 원주율의 중요성에 관한 질문

사용자 확정: 378–388초, 10초.

3840×2160, 30fps. 음원 미제공으로 무음. 본문 y≥−2.8, 자막 −4.2≤y≤−3.1.



**06:18\~06:28 · 10초**

> 어쩌면 원주율과 같은 수학적 상수의 중요성은, 이처럼 서로 다른 수학적 개념들을 연결하고 새로운 관계를 발견할 수 있게 해 준다는 점에서도 찾아볼 수 있지 않을까요?

### **마지막 카메라 시퀀스**

**378\~381초**

지금까지 생성한 관계도의 연결선을 따라 카메라가 천천히 이동합니다.

개별 수식이나 수학적 객체보다 연결선이 강조되도록 배경 객체의 밝기를 조절합니다.

**381\~384초**

카메라가 전체 관계망을 바라보는 방향으로 이동합니다.

지금까지의 1장과 2장의 수학적 구조들이 한 화면에 들어옵니다.

**384\~386초**

화면 중앙에 원주율을 배치하고 관계도 전체의 연결선들이 서서히 밝아집니다.

**386\~388초**

나레이션의 질문과 함께 다음 문구를 화면에 표시합니다.

**수학적 대상을 이해하는 것에서, 수학적 관계를 이해하는 것으로.**

이 문구는 나레이션에 추가하지 않고 시각적인 마무리 문장으로 사용합니다.

완전한 암전보다는 관계도가 낮은 밝기로 유지된 상태에서 2장을 종료합니다. 이후 3장의 새로운 표현과 계산 방법에 관한 내용을 시작할 때 동일한 관계도의 미탐구 영역을 사용할 수 있습니다.

# **Manim 구현 설계**

이번 장은 62개의 세부 장면으로 구성되지만, 실제 구현에서는 수학적 객체와 카메라의 연속성을 유지할 수 있도록 주요 Scene 단위로 묶는 것을 추천합니다.

## **1. Scene 클래스 구성**

| 클래스명                          | 담당 구간    | 시간       | 유형 |
| ----------------------------- | -------- | -------- | -- |
| `Chapter02Intro`              | 0\~19    | 19초      | 2D |
| `EulerSeriesScene`            | 19\~38   | 19초      | 2D |
| `ComplexRotationHelixScene`   | 38\~60   | 22초      | 3D |
| `FourierDecompositionScene`   | 60\~85   | 25초      | 2D |
| `FourierAverageScene`         | 85\~112  | 27초      | 2D |
| `BaselProblemIntroScene`      | 112\~139 | 27초      | 2D |
| `SawtoothFourierScene`        | 139\~153 | 14초      | 2D |
| `ParsevalBaselScene`          | 153\~190 | 37초      | 2D |
| `GaussianNormalizationScene`  | 190\~212 | 22초      | 2D |
| `GaussianSurfaceScene`        | 212\~240 | 28초      | 3D |
| `GaussianPolarIntegralScene`  | 240\~264 | 24초      | 3D |
| `GaussianResultScene`         | 264\~277 | 13초      | 2D |
| `Chapter0102SummaryScene`     | 277\~347 | 70초      | 2D |
| `MathematicalRelationsEnding` | 347\~388 | 41초      | 2D |
| **합계**                        |          | **388초** |    |

3차원 연출은 크게 두 구간에 집중합니다.

- 복소평면에서 회전과 파동의 관계를 보여주는 38\~60초.
- 가우스 함수의 공간적 구조와 회전 불변성을 보여주는 212\~264초.

모든 장면을 3D로 구현하기보다는 공간적 구조가 실제로 새로운 정보를 제공하는 부분에서 3D를 활용합니다.

## **2. 렌더링 설정**

```
from manim import *import numpy as npimport mathconfig.pixel_width = 3840config.pixel_height = 2160config.frame_width = 16config.frame_height = 9config.frame_rate = 60config.background_color = "#0B1019"COLORS = {    "background": "#0B1019",    "foreground": "#E8EDF4",    "pi": "#F4D58D",    "geometry": "#60A5FA",    "complex": "#A78BFA",    "fourier": "#A78BFA",    "gaussian": "#4ADE80",    "rotation": "#FB923C",    "negative": "#F87171",    "secondary": "#94A3B8",}
```

기존 0장과 1장에서 사용한 설정을 그대로 유지합니다.

## **3. 3D 복소지수함수와 나선**

SCENE 10의 핵심 구현에 사용할 수 있는 컴포넌트입니다.

```
class ComplexRotationHelixScene(ThreeDScene):    def construct(self):        axes = ThreeDAxes(            x_range=[0, 4 * PI, PI],            y_range=[-1.5, 1.5, 0.5],            z_range=[-1.5, 1.5, 0.5],            x_length=10,            y_length=3,            z_length=3,        )        helix = ParametricFunction(            lambda t: axes.c2p(                t,                np.cos(t),                np.sin(t)            ),            t_range=[0, 4 * PI],            color=COLORS["complex"],            stroke_width=4,        )        self.set_camera_orientation(            phi=70 * DEGREES,            theta=-50 * DEGREES,
```

### **나선과 파동의 투영 관계**

\\[ \gamma(t)=(t,\cos t,\sin t) \\]

| 바라보는 평면    | 나타나는 형태 |
| ---------- | ------- |
| 실수부–허수부 평면 | 단위원     |
| 입력값–실수부 평면 | 코사인파    |
| 입력값–허수부 평면 | 사인파     |
| 전체 3차원 공간  | 나선      |

카메라 이동만으로 투영 관계가 정확하게 드러나지 않는 경우에는 명시적인 투영 곡선을 별도로 생성하고 카메라 방향과 함께 나타내는 방식이 안정적입니다.

위 예시는 핵심 객체와 카메라 이동을 구성하기 위한 코드이며, 전체 22초 장면에 맞추어 완성된 것은 아닙니다.

## **4. 푸리에 계수의 회전 평균 컴포넌트**

```
def rotating_function(t, n, func):    value = func(t) * np.exp(-1j * n * t)    return np.array([        value.real,        value.imag,        0.0,    ])
```

예시 함수:

```
def example_function(t):    return np.cos(t) + 0.5 * np.cos(2*t)
```

회전하는 벡터의 평균을 계산합니다.

```
def fourier_average(func, n, samples=4096):    ts = np.linspace(        0,        2 * np.pi,        samples,        endpoint=False    )    values = func(ts) * np.exp(-1j*n*ts)    return np.mean(values)
```

이 예시의 이론적인 계수는 다음과 같습니다.

\\[ a_1=\frac12,\qquad a_2=\frac14,\qquad a_3=0 \\]

### **Manim 객체 구성**

```
tracker = ValueTracker(0)vector = always_redraw(    lambda: Arrow(        complex_axes.c2p(0, 0),        complex_axes.c2p(            *rotating_function(                tracker.get_value(),                n,                example_function            )[:2]        ),        color=COLORS["rotation"],        buff=0,    ))
```

화면에 생성되는 각각의 표본 벡터와 최종 평균 벡터는 별도의 객체로 관리합니다.

특히 평균 벡터를 실시간으로 계산할 때 아직 한 주기를 돌지 않았다면 중간 평균값으로 표시하고, 한 주기의 회전이 완료되었을 때 푸리에 계수라는 이름을 부여합니다.

## **5. 톱니파의 실제 푸리에 부분합**

SCENE 26에서는 임의로 형태를 변환하는 것이 아니라 실제 부분합을 계산하여 그래프를 생성합니다.

```
def sawtooth_partial_sum(x, n_terms):    result = 0.0    for n in range(1, n_terms + 1):        coefficient = (            2 * (-1)**(n + 1) / n        )        result += coefficient * np.sin(n*x)    return result
```

```
axes = Axes(    x_range=[-3*PI, 3*PI, PI],    y_range=[-4, 4, 1],    x_length=12,    y_length=5,)graph = axes.plot(    lambda x: sawtooth_partial_sum(x, 1),    color=COLORS["fourier"],)self.play(Create(graph))for n in [2, 3, 5, 10, 20, 50]:    next_graph = axes.plot(        lambda x, n=n: sawtooth_partial_sum(x, n),        color=COLORS["fourier"],    )    self.play(        Transform(graph, next_graph),        run_time=0.6,    )
```

낮은 차수의 부분합부터 높은 차수까지 빠르게 변환되도록 구현합니다.

깁스 현상을 실제로 유지하고 불연속점에서의 극한값이 좌우 극한의 평균으로 수렴한다는 특성을 훼손하지 않도록 합니다.

## **6. 3D 가우스 함수의 곡면 생성**

```
class GaussianSurfaceScene(ThreeDScene):    def construct(self):        axes = ThreeDAxes(            x_range=[-3, 3, 1],            y_range=[-3, 3, 1],            z_range=[0, 1.2, 0.2],            x_length=7,            y_length=7,            z_length=4,        )        def gaussian(x, y):            return np.exp(                -(x*x + y*y) / 2            )        surface = Surface(            lambda u, v: axes.c2p(                u,                v,                gaussian(u, v)            ),            u_range=[-3, 3],            v_range=[-3, 3],            resolution=(48, 48),            checkerboard_colors=[
```

### **곡면 위의 회전 궤적**

```
def gaussian_level_curve(axes, r):    height = np.exp(-r*r / 2)    return ParametricFunction(        lambda t: axes.c2p(            r * np.cos(t),            r * np.sin(t),            height,        ),        t_range=[0, TAU],        color=COLORS["pi"],        stroke_width=3,    )
```

```
level_curves = VGroup(*[    gaussian_level_curve(axes, r)    for r in [0.5, 1.0, 1.5, 2.0, 2.5]])
```

이렇게 하면 가우스 곡면 위에 실제 높이가 일정한 원형 등고선을 생성할 수 있습니다.

카메라가 위쪽으로 이동할 때 곡면의 형태가 원형 등고선 구조로 자연스럽게 바뀌어 보이도록 구성합니다.

2차원 가우스 함수의 회전 불변성을 보여주는 구간에서 \\(x\\)축과 \\(y\\)축의 실제 화면 스케일은 반드시 동일하게 유지해야 합니다. 그렇지 않으면 원이 타원처럼 표현될 수 있습니다.

## **7. 극좌표 미소 면적**

SCENE 45에서 사용하는 미소 부채꼴 영역은 다음과 같이 구현할 수 있습니다.

```
def polar_area_element(    r,    dr,    theta,    dtheta,    center=ORIGIN,):    return AnnularSector(        inner_radius=r,        outer_radius=r + dr,        angle=dtheta,        start_angle=theta,        fill_color=COLORS["gaussian"],        fill_opacity=0.5,        stroke_color=COLORS["pi"],        stroke_width=2,        arc_center=center,    )
```

미소 부채꼴의 정확한 넓이는

\\[ \frac12\left((r+dr)^2-r^2\right)d\theta \\]

이며, 이를 전개하면

\\[ r\\,dr\\,d\theta +\frac12(dr)^2d\theta \\]

입니다.

미소 변화량의 극한에서는 면적 요소가 다음과 같이 표현됩니다.

\\[ dA=r\\,dr\\,d\theta \\]

영상에서는 이 관계를 보여주는 정도면 충분합니다. 야코비안 행렬 전체를 설명하는 것은 원주율이 등장하는 이유에서 벗어나므로 생략합니다.

# **핵심 구현 과제 — 확장 가능한 지식 관계도**

이번 장의 마지막 111초를 별도의 독립적인 Scene들로 나누지 않고 구현하려면, 관계도를 단순 이미지가 아닌 실제 노드와 연결선을 관리하는 컴포넌트로 만드는 것이 좋습니다.

## **8. 관계도 데이터 구조**

```
GRAPH_NODES = {    "geometry": {        "chapter": 1,        "label": "기하학적 정의",        "equation": r"\pi=\frac{C}{d}",        "position": [-6, 2, 0],        "color": COLORS["geometry"],    },    "power_series": {        "chapter": 1,        "label": "멱급수",        "equation": (            r"\sum_{n=0}^{\infty}"            r"\frac{x^n}{n!}"        ),        "position": [-2, 2, 0],        "color": COLORS["complex"],    },    "euler": {        "chapter": 2,        "label": "오일러 공식",        "equation": (            r"e^{ix}=\cos x+i\sin x"        ),        "position": [2, 2, 0],        "color": COLORS["complex"],
```

이것은 일부 노드의 데이터 구조 예시입니다. 모든 노드를 독립적으로 관리하면 위치와 연결 관계를 나중에 변경하기 쉽습니다.

### **연결선의 종류도 구분**

```
GRAPH_EDGES = [    {        "source": "power_series",        "target": "euler",        "relation": "representation",        "style": "solid",        "reveal_at": 296,    },    {        "source": "euler",        "target": "periodicity",        "relation": "property",        "style": "solid",        "reveal_at": 304,    },    {        "source": "fourier",        "target": "parseval",        "relation": "theorem",        "style": "solid",        "reveal_at": 315,    },    {        "source": "periodicity",        "target": "rotational_invariance",        "relation": "shared_structure",
```

관계의 유형에 따라 다른 애니메이션을 사용합니다.

| 관계 유형         | 표현 방법         |
| ------------- | ------------- |
| 동일한 대상의 표현    | 양방향 연결선 또는 등호 |
| 수학적 유도        | 방향이 있는 실선     |
| 성질의 활용        | 강조된 실선        |
| 공통된 구조        | 점선 연결         |
| 아직 탐구하지 않은 관계 | 낮은 밝기의 점선     |

이를 구분하면 관계도가 단순한 연관 키워드의 모음이 아니라 실제 수학적 관계를 나타내는 구조로 발전할 수 있습니다.

## **9. 관계도 Scene 인터페이스**

```
class MathematicalKnowledgeGraph(VGroup):    def __init__(self, **kwargs):        super().__init__(**kwargs)        self.nodes = {}        self.edges = {}    def register_node(self, node_id, data):        # 노드의 도형, 수식, 제목 생성        pass    def reveal_node(self, node_id):        # 노드 등장 애니메이션 반환        pass    def connect_nodes(        self,        source,        target,        relation="derivation",    ):        # 관계 유형에 맞는 연결선 생성        pass    def highlight_path(self, node_ids):        # 특정 수학적 경로 강조        pass    def get_node(self, node_id):        return self.nodes[node_id]
```

이 인터페이스를 0장, 1장, 2장뿐 아니라 이후의 모든 챕터에서 공통적으로 사용합니다.

### **카메라 이동 방식**

```
class Chapter0102SummaryScene(    MovingCameraScene):    def focus_node(        self,        graph,        node_id,        scale_factor=1.8,        duration=1.5,    ):        node = graph.get_node(node_id)        self.play(            self.camera.frame.animate                .move_to(node.get_center())                .set_width(                    node.width * scale_factor                ),            run_time=duration,        )
```

이렇게 하면 관계도 내에서 특정 수학적 개념으로 확대하고, 개별 노드에 관한 설명을 마친 후 전체 관계도로 돌아오는 연출을 반복적으로 구현할 수 있습니다.

## **10. 1·2장 통합 정리용 타임라인**

마무리 Scene의 제어를 명확하게 하기 위해 시간별 이벤트를 정의하는 방식도 좋겠습니다.

| 절대 시간 | 관계도 이벤트            |
| ----- | ------------------ |
| 277초  | 전체 관계도 공간 진입       |
| 281초  | 기하학적 정의 활성화        |
| 283초  | 함수와 방정식 노드 생성      |
| 285초  | 곡선 길이와 넓이 가지 분기    |
| 289초  | 해석학적 정의 영역으로 이동    |
| 292초  | 멱급수에서 삼각함수 생성      |
| 295초  | 원주율 노드와 연결         |
| 296초  | 멱급수에서 오일러 공식으로 확장  |
| 304초  | 복소평면의 회전 노드 생성     |
| 308초  | 함수의 주기성 노드 연결      |
| 310초  | 푸리에 해석 가지 생성       |
| 315초  | 파르세발 항등식 노드 추가     |
| 320초  | 바젤 문제 결과 표시        |
| 322초  | 가우스 함수 가지 생성       |
| 326초  | 이차원 가우스 함수와 연결     |
| 328초  | 회전 불변성 노드 생성       |
| 330초  | 극좌표 변환 노드 생성       |
| 332초  | 정규분포 노드 완성         |
| 333초  | 기하학적 정의로 카메라 복귀    |
| 336초  | 1장의 관계도 순회         |
| 339초  | 푸리에 해석 가지 순회       |
| 342초  | 정규분포 가지 순회         |
| 345초  | 전체 관계도 공개          |
| 347초  | 아직 탐구하지 않은 영역 표시   |
| 353초  | 공통된 상수와 구조 강조      |
| 362초  | 수학적 대상에서 관계로 초점 이동 |
| 369초  | 수학적 방법의 재사용 강조     |
| 378초  | 완성된 관계망 조망         |
| 388초  | CHAPTER 02 종료      |

이벤트 시간을 기준으로 각 메서드를 구현하면 나레이션이 수정되었을 때 전체 애니메이션을 일일이 수정해야 하는 문제도 줄일 수 있습니다.

# **제작 우선순위**

**1. 복소평면 → 3D 나선 → 사인파**

52\~60초 · 회전과 주기성의 직접적인 연결

**2. 회전하는 벡터의 평균**

85\~103초 · 푸리에 계수에 2π가 등장하는 이유

**3. 톱니파 → 파르세발 항등식 → 바젤 문제**

139\~176초 · 수학적 관계를 실제 문제 해결에 활용

**4. 일차원 가우스 함수 → 3차원 곡면**

212\~240초 · 공간을 확장하면서 발견하는 새로운 대칭성

**5. 극좌표 변환과 각도 적분**

240\~264초 · 정규분포에서 원주율이 등장하는 직접적인 이유

**6. 1장과 2장의 통합 지식 관계도**

277\~388초 · 영상 전체의 메시지를 시각적으로 완성

## **제작 시 주의할 사항**

이번 콘티는 제공한 388초 분량의 나레이션을 그대로 기준으로 설계했습니다. 다만 수학적으로 더 정확한 전달을 위해 다음 부분은 자막과 수식 연출에서 보완했습니다.

| 기존 나레이션 표현           | 화면에서의 보완                               |
| -------------------- | -------------------------------------- |
| 단위원의 둘레를 나타냈던 원주율    | 단위원의 둘레는 정확히 \\(2\pi\\)                |
| 푸리에 계수의 표현에 등장하는 원주율 | \\(2\pi\\) 주기로 정규화된 각도 변수라는 조건 표시      |
| 진동 성분의 계수            | 실수 사인 계수 \\(b_n\\)와 복소 계수 \\(a_n\\) 구분 |
| 파르세발 항등식             | 사용하는 푸리에 급수의 정규화 방식 명시                 |
| 자연수의 역수를 더하는 문제      | 정확하게는 자연수의 제곱에 대한 역수합                  |
| 극좌표계로의 변환            | 면적 요소 \\(r\\,dr\\,d\theta\\) 포함        |
| 가우스 적분에서의 회전 불변성     | 일차원 함수 자체가 아닌 이차원으로 확장된 함수의 성질         |
| 수학적 관계의 연결           | 실제 유도 관계와 공통 구조를 구분                    |

제시한 2D·3D 시연은 화면 설계용 개념적 시각화이며, Manim 코드 역시 핵심 구현 예시입니다. 전체 렌더링과 실제 음성 싱크 검증은 수행하지 않았습니다. 3D 카메라 각도와 일부 수식의 표시 시간은 저해상도 테스트 렌더링에서 조정할 필요가 있습니다.

# **이번 장의 전체 서사**

결국 이번 장에서 가장 중요하게 전달하고자 하는 흐름은 다음과 같습니다.

CHAPTER 01

## **표현의 확장**

원을 함수로 표현하고, 함수와 적분, 무한급수를 통해 동일한 원주율에 도달한다.

**기존 표현의 활용**\
멱급수라는 표현을 복소지수함수에도 적용한다.

\\[ e^{ix}=\cos x+i\sin x \\]

**수학적 구조의 발견**\
원의 회전이 함수의 주기성으로 나타난다.

**푸리에 해석**

주기성과 진동 성분

**파르세발 항등식**

**바젤 문제**

\\[ \frac{\pi^2}{6} \\]

**가우스 적분**

별도의 문제에서 출발

**회전 불변성과 극좌표**

**정규분포**

\\[ \sqrt{2\pi} \\]

CHAPTER 02

## **관계의 확장**

서로 다른 수학적 문제에서 공통된 구조를 발견하고 새로운 문제 해결 방법을 얻는다.

0장에서는 원주율을 중심으로 다양한 수학적 개념이 등장하는 모습을 보여주었고, 1장에서는 그 개념들로부터 동일한 원주율에 도달하는 과정을 살펴보았습니다.

2장에서는 한 단계 더 나아가 수학적 개념들이 서로 직접적인 관계를 형성하게 됩니다.

**0장 — 관계에 대한 질문.**

**1장 — 동일한 대상에 도달하는 여러 표현.**

**2장 — 서로 다른 표현에서 발견되는 수학적 구조와 그 활용.**

이러한 변화가 실제 영상의 관계망에도 그대로 반영되도록 만드는 것이 이번 콘티의 핵심입니다.