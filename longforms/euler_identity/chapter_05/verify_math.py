"""Verify the exact data used for Euler steps, limit, tangents and radians."""
from pathlib import Path
import json,numpy as np
from visuals import complex_exp_steps,FiniteVisual,OrbitVisual
R=Path(__file__).resolve().parent
reports=[]
for theta in [-5,-np.pi,-1,0,.5,1,np.pi,5]:
    radii=[];angles=[];errors=[]
    for n in [4,10,100,1000]:
        z=complex_exp_steps(theta,n);d=np.diff(z)
        assert np.allclose(z[0],1)
        assert np.allclose(d,1j*theta/n*z[:-1])
        assert np.allclose(np.real(np.conj(z[:-1])*d),0,atol=1e-10)
        modulus=(1+(theta/n)**2)**(n/2)
        angle=n*np.arctan(theta/n)
        assert np.isclose(abs(z[-1]),modulus)
        assert np.allclose(z[-1],modulus*np.exp(1j*angle))
        if theta:assert np.all(np.abs(z[1:])>np.abs(z[:-1]))
        radii.append(float(modulus));angles.append(float(angle));errors.append(float(abs(z[-1]-np.exp(1j*theta))))
    assert all(a>=b-1e-12 for a,b in zip(errors,errors[1:])),(theta,errors)
    assert all(a>=b-1e-12 for a,b in zip(radii,radii[1:]))
    assert all(a>=b-1e-12 for a,b in zip([abs(v-theta) for v in angles],[abs(v-theta) for v in angles][1:]))
    reports.append(dict(theta=theta,radii=radii,unwrapped_angles=angles,errors=errors))
v=FiniteVisual(np.pi,4,4,wide=True)
scale_x=np.linalg.norm(v.axes.c2p(1,0)-v.o);scale_y=np.linalg.norm(v.axes.c2p(0,1)-v.o)
assert np.isclose(scale_x,scale_y)
assert np.allclose(v.axes.p2c(v.dot.get_center()),[v.values[-1].real,v.values[-1].imag])
assert abs(v.values[-1])>2.6
u=OrbitVisual(0,velocity=True)
for theta in np.linspace(-2*np.pi,2*np.pi,41):
    u.theta.set_value(theta);p=u.point();velocity=u.velocity_end()-p;radius=p-u.o
    assert abs(np.dot(radius,velocity))<1e-10
    assert np.isclose(np.linalg.norm(radius),u.unit)
    assert np.isclose(np.linalg.norm(velocity),u.unit)
    assert radius[0]*velocity[1]-radius[1]*velocity[0]>0
    assert abs(2*np.real(np.conj(np.exp(1j*theta))*1j*np.exp(1j*theta)))<1e-12
    assert np.allclose(u.axes.p2c(p),[np.cos(theta),np.sin(theta)])
u.theta.set_value(1);u.update(0);arc_over_radius=u.arc.get_arc_length()/u.unit
assert abs(arc_over_radius-1)<.001
report=dict(passed=True,ns=[4,10,100,1000],fixed_theta_pi_radii=[float(abs(complex_exp_steps(np.pi,n)[-1])) for n in [4,10,100,1000]],same_axis_scale=[scale_x,scale_y],no_finite_normalization=True,perpendicular_velocity=True,constant_radius_and_unit_speed=True,one_radian_arc_over_radius=float(arc_over_radius),euler_formula=True,convergence=reports)
(R/'math_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Finite vector sums, amplitude and angle convergence, equal axes, unit-speed tangents, one radian and Euler coordinates verified.')
