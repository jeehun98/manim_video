"""Code costs, lossless example, and speech-estimated frame-aligned cues."""
import math

PROBABILITIES = dict(zip("ABCD", (.7, .1, .1, .1)))
FIXED = dict(zip("ABCD", ("00", "01", "10", "11")))
VARIABLE = dict(zip("ABCD", ("0", "10", "110", "111")))
MESSAGE = "".join({3: "B", 7: "C", 11: "D", 15: "B", 17: "C", 19: "D"}.get(i, "A") for i in range(20))
FIXED_BITS = "".join(FIXED[s] for s in MESSAGE)
VARIABLE_BITS = "".join(VARIABLE[s] for s in MESSAGE)
MEAN_LENGTH = sum(PROBABILITIES[s] * len(VARIABLE[s]) for s in "ABCD")
ENTROPY = -sum(p * math.log2(p) for p in PROBABILITIES.values())

def decode(bits, codes):
    reverse = {code: symbol for symbol, code in codes.items()}
    result, pending = [], ""
    for bit in bits:
        pending += bit
        if pending in reverse:
            result.append(reverse[pending])
            pending = ""
    if pending:
        raise ValueError("Incomplete codeword")
    return "".join(result)

TEXT = [
    "압축하면 무엇이 사라질까요? 비트의 지출을 바꿔봅시다.",
    "20개 중 A는 14번. 모두 2 bits씩 쓰면 40 bits입니다.",
    "가장 자주 쓸 이름이, 가장 싸다면 어떨까요?",
    "질문 트리의 경로를 코드로 씁니다. A는 1 bit, B는 2, C와 D는 3입니다.",
    "어느 코드도 다른 코드의 시작이 아닙니다. 이어 붙여도 원문을 복원할 수 있습니다.",
    "같은 20개가 30 bits가 됐습니다. 줄어든 것은 기호 수가 아니라 표현 비용입니다.",
    "드문 C와 D는 오히려 길어졌습니다. 자주 나오는 A에서의 절약이 이를 상쇄합니다.",
    "압축은 예상 가능한 것을 싸게 표현하는 설계입니다.",
    "반복만은 아닙니다. 반복 없는 규칙도, 모형이 알고 있다면 예측할 수 있습니다.",
    "실제 코드 길이는 정수입니다. 엔트로피는 평균 길이의 하한이고, 여러 기호를 묶으면 가까워집니다.",
    "예측이 좋을수록 평균 비트 비용을 줄일 여지가 생깁니다.",
    "그런데 예상한 확률이 틀렸다면? 잘못 배분한 비트의 비용은 얼마나 클까요?",
]

REPLACEMENTS = [
    ("40 bits", "사십 비트"), ("30 bits", "삼십 비트"), ("2 bits", "이 비트"),
    ("1 bit", "일 비트"), ("20", "스무"), ("14", "열네"),
    ("A", "에이"), ("B", "비"), ("C", "씨"), ("D", "디"), ("2", "이"), ("3", "삼"),
]
SPOKEN = []
for display in TEXT:
    spoken = display
    for old, new in REPLACEMENTS:
        spoken = spoken.replace(old, new)
    SPOKEN.append(spoken)

CUES = []
frames = 0
for i, (display, spoken) in enumerate(zip(TEXT, SPOKEN)):
    seconds = max(2.6, len("".join(spoken.split())) / 7.0 + .18 * (spoken.count(".") + spoken.count("?")))
    if i == len(TEXT) - 1:
        seconds += .5
    count = round(seconds * 30)
    CUES.append((frames / 30, (frames + count) / 30, display, spoken))
    frames += count
DURATION = frames / 30
