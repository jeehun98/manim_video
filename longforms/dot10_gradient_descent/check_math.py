"""Verify local derivatives separately from exact finite loss changes."""
import json
import numpy as np
from visuals import P,THETA,GRAD,NORM,loss
assert np.allclose(GRAD,[2*THETA[0],8*THETA[1]]) and loss(THETA)==8
eps=1e-6;fd=np.array([(loss(THETA+eps*np.eye(2)[i])-loss(THETA-eps*np.eye(2)[i]))/(2*eps) for i in range(2)])
assert np.allclose(fd,GRAD,atol=1e-8)
max_norm_error=0.;max_taylor_error=0.;minimum=1e9
for angle in np.linspace(0,2*np.pi,721):
    u=np.array([np.cos(angle),np.sin(angle)]);d=float(GRAD@u);minimum=min(minimum,d);max_norm_error=max(max_norm_error,abs(np.linalg.norm(u)-1))
    for e in [.001,.02,.1]:
        delta=e*u;exact=loss(THETA+delta)-loss(THETA);first=float(GRAD@delta);remainder=delta[0]**2+4*delta[1]**2
        max_taylor_error=max(max_taylor_error,abs(exact-first-remainder))
assert max_taylor_error<1e-12 and max_norm_error<1e-12
u=-GRAD/NORM;assert np.allclose(u,[-1/np.sqrt(5),-2/np.sqrt(5)]) and abs(GRAD@u+NORM)<1e-12
assert minimum>=-NORM-1e-12 and np.isclose(GRAD@[1,0],4) and np.isclose(GRAD@[-1,0],-4)
updates=[]
for eta,expected,expected_loss in [(.1,[1.6,.2],2.72),(.4,[.4,-2.2],19.52)]:
    new=THETA-eta*GRAD;actual=loss(new);assert np.allclose(new,expected) and abs(actual-expected_loss)<1e-12
    updates.append(dict(learning_rate=eta,new_point=new.tolist(),loss=actual,exact_change=actual-8,first_order_change=float(-eta*(GRAD@GRAD))))
contour_error=0.
for level in [1,2.72,4,8,12,19.52,24]:
    for angle in np.linspace(0,2*np.pi,101):
        point=[np.sqrt(level)*np.cos(angle),np.sqrt(level)/2*np.sin(angle)];contour_error=max(contour_error,abs(loss(point)-level))
assert contour_error<1e-12
# Tangent lift preserves the directional derivative, not the true finite height.
delta=-.06*GRAD;tangent_z=8+float(GRAD@delta);surface_z=loss(THETA+delta);assert abs(surface_z-tangent_z-(delta[0]**2+4*delta[1]**2))<1e-12
report=dict(loss='theta1**2+4*theta2**2',current=THETA.tolist(),gradient=GRAD.tolist(),finite_difference=fd.tolist(),gradient_norm=NORM,minimum_unit_direction=u.tolist(),minimum_directional_derivative=float(GRAD@u),max_unit_norm_error=max_norm_error,max_taylor_remainder_error=max_taylor_error,max_contour_error=contour_error,updates=updates,gradient_display_scale=.18,surface_height_display_scale=.15,tangent_plane='z=8+4*(x-2)+8*(y-1)',local_condition='Euclidean fixed-length first-order change; not arbitrary finite steps')
(P/'qa_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
