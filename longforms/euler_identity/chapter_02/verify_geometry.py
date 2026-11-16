"""Check the geometry actually used by the animation, including signed quadrants."""
import json
from pathlib import Path
import numpy as np
from visuals import UnitCircleVisual,RadianCircleVisual,CircleRatioVisual
R=Path(__file__).resolve().parent
u=UnitCircleVisual(0,components=True)
scale_x=np.linalg.norm(u.axes.c2p(1,0)-u.origin)
scale_y=np.linalg.norm(u.axes.c2p(0,1)-u.origin)
assert abs(scale_x-scale_y)<1e-10
samples=[]
for t in np.linspace(0,2*np.pi,17):
    u.theta.set_value(t);u.update(0)
    p=u.point();x,y=np.cos(t),np.sin(t)
    assert abs(np.linalg.norm(p-u.origin)-1.6)<1e-9
    assert np.allclose(u.axes.p2c(p),[x,y])
    assert np.allclose(u.components[0].get_end(),u.axes.c2p(x+1e-8,0))
    assert np.allclose(u.components[1].get_start(),u.axes.c2p(x,0))
    samples.append(dict(theta=float(t),x=float(x),y=float(y)))
v=RadianCircleVisual(1);v.update(0)
ratio=v.arc.get_arc_length()/v.radius
assert abs(ratio-1)<.001,ratio
ratios=[c.circle.get_arc_length()/c.diameter.get_length() for c in [CircleRatioVisual(.85),CircleRatioVisual(1.7)]]
assert abs(ratios[0]-ratios[1])<1e-8
assert abs(ratios[0]-np.pi)<.001
report=dict(passed=True,equal_axis_scales=[scale_x,scale_y],one_radian_arc_over_radius=float(ratio),circumference_over_diameter=ratios,samples=samples)
(R/'geometry_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Equal axes, exact 1-radian angle, scale-invariant C/d and signed coordinate components verified.')
