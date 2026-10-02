"""Concrete compute-copy-uncompute example and exact gate verification."""
import itertools
import numpy as np

def toffoli(state):
    a,b,t,r=state
    return a,b,t^(a&b),r

def copy_result(state):
    a,b,t,r=state
    return a,b,t,r^t

def uncompute(state):
    return toffoli(copy_result(toffoli(state)))

START=(1,1,0,0)
TRACE=[START,toffoli(START),copy_result(toffoli(START)),uncompute(START)]
STATES=list(itertools.product((0,1),repeat=4))
PERMUTATION=np.zeros((16,16))
for j,state in enumerate(STATES):PERMUTATION[STATES.index(uncompute(state)),j]=1
INITIAL=np.zeros(16);INITIAL[0]=INITIAL[12]=1/np.sqrt(2)
QUANTUM_FINAL=PERMUTATION@INITIAL

DISPLAY=[
 'AND의 결과가 0입니다. 입력은 00, 01, 10 중 무엇이었을까요?',
 '입력을 버리면 삭제 비용과 연결됩니다. 이번에는 입력을 남기고 계산해보죠.',
 '입력 1과 1은 그대로 둡니다. 작업 칸만 0에서 결과 1로 바꿉니다.',
 '거꾸로 실행하면 작업 칸은 0으로 돌아갑니다. 하지만 결과도 없어집니다.',
 '긴 계산의 중간값은 계속 쌓입니다. 그냥 지우면 다시 비가역적입니다.',
 '먼저 결과를 별도 칸에 보존합니다. 작업 칸의 1로, 결과 칸의 0을 1로 바꿉니다.',
 '작업 계산만 되감습니다. 작업 칸은 0으로, 별도 결과는 1로 남습니다.',
 '이것이 uncomputation입니다. 0으로 덮는 대신, 입력을 이용해 원래 상태를 복원합니다.',
 '토폴리 게이트는 입력을 보존합니다. 같은 게이트를 다시 적용하면 되돌아옵니다.',
 '같은 회로가 양자 계산에도 쓰입니다. 이상적 게이트는 역순으로 역연산하면 되돌릴 수 있습니다.',
 '중첩된 입력에서도 보조 큐빗을 0으로 되돌립니다. 입력과 보존한 결과는 남습니다.',
 '측정과 리셋은 다릅니다. 측정한 상태는 같은 역회로만으로 복원할 수 없습니다.',
 '가역적이어도 실제 소비가 영은 아닙니다. 작업 공간과 계산 단계도 더 필요합니다.',
 '결과는 남기고, 중간 계산은 되감습니다. 계산은 정보를 지우지 않고도 구성할 수 있습니다.',
]
READINGS=[('AND','앤드'),('uncomputation','언컴퓨테이션'),('00','영 영'),('01','영 일'),('10','일 영'),('1','일'),('0','영')]
SPOKEN=[]
for value in DISPLAY:
    for a,b in READINGS:value=value.replace(a,b)
    SPOKEN.append(value)
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    duration=max(3.5,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1:duration+=.5
    count=round(duration*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken));frames+=count
DURATION=frames/30
