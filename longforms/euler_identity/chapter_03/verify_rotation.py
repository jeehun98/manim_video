"""Verify the animation's rotation formula on all quadrants and at the origin."""
from pathlib import Path
from types import SimpleNamespace
import json,numpy as np
from manim import ValueTracker
from visuals import GeneralVisual,wide_axes
R=Path(__file__).resolve().parent
axes=wide_axes(False);origin=axes.c2p(0,0)
sx=np.linalg.norm(axes.c2p(1,0)-origin);sy=np.linalg.norm(axes.c2p(0,1)-origin)
assert abs(sx-sy)<1e-10
results=[]
for a,b in [(2,3),(-3,2),(-2,-3),(3,-2),(0,0),(0,1),(1,0)]:
    fake=SimpleNamespace(theta=ValueTracker(np.pi/2),original=np.array([a,b]),axes=axes)
    point=GeneralVisual.point(fake);xy=axes.p2c(point)
    assert np.allclose(xy,[-b,a])
    assert np.allclose(xy,[complex(a,b).__mul__(1j).real,complex(a,b).__mul__(1j).imag])
    assert abs(np.linalg.norm(xy)-np.linalg.norm([a,b]))<1e-9
    assert abs(np.dot([a,b],xy))<1e-9
    if a or b:assert a*xy[1]-b*xy[0]>0
    fake.theta.set_value(np.pi);assert np.allclose(axes.p2c(GeneralVisual.point(fake)),[-a,-b])
    fake.theta.set_value(2*np.pi);assert np.allclose(axes.p2c(GeneralVisual.point(fake)),[a,b])
    results.append(dict(original=[a,b],quarter_turn=xy.tolist()))
cycle=[complex(np.cos(k*np.pi/2),np.sin(k*np.pi/2)) for k in range(5)]
assert np.allclose(cycle,[1,1j,-1,-1j,1])
report=dict(passed=True,equal_axis_scales=[sx,sy],quarter_turn_is_counterclockwise=True,zero_fixed=True,half_turn_is_negation=True,full_turn_is_identity=True,samples=results)
(R/'rotation_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('All-quadrant coordinates, preserved length, counterclockwise quarter turn, negation, full turn and zero verified.')
