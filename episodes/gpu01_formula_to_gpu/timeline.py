"""GPU 01 대본과 화면 타이밍. 시작/끝은 초 단위이며 직접 수정합니다."""

FPS = 30
DURATION = 145.0

# 각 action은 scene.py의 anim_<action> 메서드에 대응합니다.
CUES = [
    {'id': '01', 'section': '수식', 'action': 'formula', 'text': '각 원소에 1을 더합니다.', 'start': 0.133333333, 'end': 2.266666667},
    {'id': '02', 'section': '수식', 'action': 'formula_focus', 'text': '수학적으로는 이 한 줄이면 충분합니다.', 'start': 2.5, 'end': 6.2},
    {'id': '03', 'section': '수식', 'action': 'question', 'text': '그런데 이 계산은 GPU에서 어떻게 실행될까요?', 'start': 6.433333333, 'end': 10.966666667},
    {'id': '04', 'section': '데이터와 Kernel', 'action': 'data', 'text': '먼저 데이터를 펼쳐 보겠습니다.', 'start': 11.3, 'end': 14.3},
    {'id': '05', 'section': '데이터와 Kernel', 'action': 'elements', 'text': '사각형 하나가 원소 하나입니다.', 'start': 14.533333333, 'end': 17.4},
    {'id': '06', 'section': '데이터와 Kernel', 'action': 'kernel', 'text': '이 데이터를 읽고, 계산하고, 결과를 쓰는 GPU 함수를 Kernel이라고 합니다.', 'start': 17.633333333, 'end': 25.6},
    {'id': '07', 'section': 'Thread 배치', 'action': 'threads', 'text': '여기서는 Thread 하나가 원소 하나를 맡습니다.', 'start': 25.933333333, 'end': 30.166666667},
    {'id': '08', 'section': 'Thread 배치', 'action': 'assignments', 'text': '같은 Kernel을 실행하지만 담당 위치는 서로 다릅니다.', 'start': 30.4, 'end': 35.1},
    {'id': '09', 'section': '병렬 계산', 'action': 'first_results', 'text': '3은 4가 되고, 7은 8이 됩니다.', 'start': 35.433333333, 'end': 39.166666667},
    {'id': '10', 'section': '병렬 계산', 'action': 'other_results', 'text': '다른 Thread도 같은 계산을 수행합니다.', 'start': 39.4, 'end': 42.866666667},
    {'id': '11', 'section': '병렬 계산', 'action': 'independent', 'text': '하나의 연산이 독립적인 여러 작업으로 나뉜 것입니다.', 'start': 43.1, 'end': 47.9},
    {'id': '12', 'section': 'Block', 'action': 'block', 'text': 'Thread가 많아지면 여러 Thread를 하나의 Block으로 묶습니다.', 'start': 48.233333333, 'end': 53.3},
    {'id': '13', 'section': 'Block', 'action': 'zoom', 'text': '시야를 넓혀 보면 여러 Block이 있고,', 'start': 53.533333333, 'end': 56.7},
    {'id': '14', 'section': 'Block', 'action': 'block_contents', 'text': '각 Block 안에 다시 여러 Thread가 있습니다.', 'start': 56.933333333, 'end': 60.566666667},
    {'id': '15', 'section': 'Grid', 'action': 'grid', 'text': '한 번의 Kernel 실행에서 이 Block 전체를 Grid라고 합니다.', 'start': 60.9, 'end': 65.966666667},
    {'id': '16', 'section': 'Grid', 'action': 'hierarchy', 'text': 'Thread, Block, Grid는 작업을 조직하는 계층 구조입니다.', 'start': 66.2, 'end': 72.566666667},
    {'id': '17', 'section': 'Grid', 'action': 'scheduling', 'text': '모든 Block이 반드시 동시에 실행되는 것은 아닙니다.', 'start': 72.8, 'end': 77.466666667},
    {'id': '18', 'section': 'Memory 구조', 'action': 'memory', 'text': '계산 구조 옆에는 데이터를 저장하는 구조도 있습니다.', 'start': 77.8, 'end': 82.433333333},
    {'id': '19', 'section': 'Memory 구조', 'action': 'global_memory', 'text': '입력과 출력은 Global Memory에 있고,', 'start': 82.666666667, 'end': 86.2},
    {'id': '20', 'section': 'Memory 구조', 'action': 'registers', 'text': 'Thread는 계산할 값을 Register에서 사용합니다.', 'start': 86.433333333, 'end': 90.8},
    {'id': '21', 'section': '입력 읽기', 'action': 'follow_thread', 'text': 'Thread 하나를 따라가 보겠습니다.', 'start': 91.133333333, 'end': 93.933333333},
    {'id': '22', 'section': '입력 읽기', 'action': 'load', 'text': '입력값 3을 읽어 Register로 가져옵니다.', 'start': 94.166666667, 'end': 97.966666667},
    {'id': '23', 'section': 'Register 계산', 'action': 'compute', 'text': '여기에 1을 더하면 4가 됩니다.', 'start': 98.3, 'end': 101.033333333},
    {'id': '24', 'section': '결과 쓰기', 'action': 'store', 'text': '계산된 4를 출력 위치에 씁니다.', 'start': 101.366666667, 'end': 104.466666667},
    {'id': '25', 'section': '결과 쓰기', 'action': 'finish_results', 'text': '다른 Thread도 같은 과정을 거쳐 결과를 완성합니다.', 'start': 104.7, 'end': 109.366666667},
    {'id': '26', 'section': 'Shared Memory', 'action': 'shared', 'text': 'Block 안에는 Thread들이 함께 사용하는 Shared Memory도 있습니다.', 'start': 109.7, 'end': 115.233333333},
    {'id': '27', 'section': 'Shared Memory', 'action': 'shared_optional', 'text': '하지만 이 단순한 계산에서는 필요하지 않습니다.', 'start': 115.466666667, 'end': 119.866666667},
    {'id': '28', 'section': '전체 흐름', 'action': 'return_formula', 'text': '다시 처음 수식으로 돌아가 봅시다.', 'start': 120.2, 'end': 123.3},
    {'id': '29', 'section': '전체 흐름', 'action': 'summary_kernel', 'text': '계산을 Kernel로 표현하고,', 'start': 123.533333333, 'end': 125.8},
    {'id': '30', 'section': '전체 흐름', 'action': 'summary_hierarchy', 'text': 'Thread, Block, Grid로 나눈 뒤', 'start': 126.033333333, 'end': 130.033333333},
    {'id': '31', 'section': '전체 흐름', 'action': 'summary_memory', 'text': '데이터를 읽고 계산해 결과를 씁니다.', 'start': 130.266666667, 'end': 133.566666667},
    {'id': '32', 'section': '결론', 'action': 'conclusion_work', 'text': '같은 수식도 작업을 어떻게 나누고', 'start': 133.9, 'end': 137.266666667},
    {'id': '33', 'section': '결론', 'action': 'conclusion_data', 'text': '데이터를 어떻게 배치하느냐에 따라', 'start': 137.5, 'end': 140.533333333},
    {'id': '34', 'section': '결론', 'action': 'conclusion_performance', 'text': 'GPU의 실행 방식과 성능은 달라집니다.', 'start': 140.766666667, 'end': 144.766666667},
]
