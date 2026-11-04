CASES={
 'L1 Hit':dict(l1=True,l2=True,request=['Warp','L1'],response=['L1','Register'],status=['Hit','미접근','미접근'],source='L1'),
 'L2 Hit':dict(l1=False,l2=True,request=['Warp','L1','L2'],response=['L2','L1','Register'],status=['Miss','Hit','미접근'],source='L2'),
 'DRAM':dict(l1=False,l2=False,request=['Warp','L1','L2','DRAM'],response=['DRAM','L2','L1','Register'],status=['Miss','Miss','접근'],source='DRAM'),
 'L1 Bypass':dict(l1=None,l2=True,request=['Warp','L2'],response=['L2','Register'],status=['미사용','Hit','미접근'],source='L2')
}
