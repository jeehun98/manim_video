"""Single source for narration and estimated speech timing."""
TEXT = [
    "모른다는 건, 여러 가능성을 아직 버리지 못했다는 뜻입니다.",
    "결과를 보기 전에는 A도, B도 가능한 세계로 남아 있습니다.",
    "결과가 A라면, B는 제외됩니다. 정보를 얻으며 가능성이 줄었습니다.",
    "그런데 같은 A를 봐도, 얻는 정보는 같을까요?",
    "A와 B가 모두 가능했다면, A를 보고 B를 버립니다.",
    "처음부터 A가 확실했다면? 확인해도 새롭게 버릴 가능성이 없습니다.",
    "데이터는 같은 A입니다. 하지만 정보량은 관측 전의 확률에 달려 있습니다.",
    "A의 확률이 0.9라면, 예상한 A보다 드문 B가 더 많은 정보를 줍니다.",
    "정보는 가능성을 좁힙니다. 단, 지운 개수만으로 정보량을 정할 수는 없습니다.",
    "가능성마다 무게가 다르니까요. 다음 편에서 확률로 정보의 크기를 재봅니다.",
]
SPOKEN = [s.replace('A','에이').replace('B','비').replace('0.9','영 점 구') for s in TEXT]
CUES=[]
elapsed=0.0
for i,(display,spoken) in enumerate(zip(TEXT,SPOKEN)):
    length=round(len(''.join(spoken.split()))/7.0 + .18*(spoken.count('.')+spoken.count('?')),1)
    length=max(3.0,length)+(.6 if i==len(TEXT)-1 else 0)
    end=round(elapsed+length,1)
    CUES.append((elapsed,end,display,spoken))
    elapsed=end
DURATION=elapsed
