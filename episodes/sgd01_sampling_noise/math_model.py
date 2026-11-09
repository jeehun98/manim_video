"""Deterministic numerical inputs for the animation; no hand-shrunk clouds."""
import numpy as np

SEED=20261108
MEAN=np.array([.6,.8])
v=np.array([[1.4,.10],[1.1,-.08],[.8,.12],[.45,-.04],[1.25,.06],[.95,-.10],[.6,.08],[.3,-.06]])
OFFSETS=np.concatenate([v,-v])
WIDE=MEAN+OFFSETS
NARROW=MEAN+OFFSETS*.13
GROUPS=[np.array([0,2,4,6]),np.array([8,10,12,14]),np.array([0,8,3,11])]

def means(batch_size,repeats=192):
    rng=np.random.default_rng(SEED+batch_size)
    return WIDE[rng.integers(0,len(WIDE),size=(repeats,batch_size))].mean(axis=1)

def covariance(batch_size=1):
    return np.cov(WIDE.T,bias=True)/batch_size

def loss(p):
    x,y=np.asarray(p).T
    return (x*x-1)**2/4+y*y/2

def full_gradient(p):
    x,y=p
    return np.array([x*(x*x-1),y])

def trajectory(seed=None,steps=110,eta=.075):
    """Mean loss plus four balanced linear sample perturbations ±.8x ±.18y."""
    rng=np.random.default_rng(seed);p=np.array([0.,1.15]);points=[p.copy()]
    for _ in range(steps):
        g=full_gradient(p)
        if seed is not None:g=g+rng.choice([-1.,1.],size=2)*np.array([.8,.18])
        p=p-eta*g;points.append(p.copy())
    return np.array(points)

def validate():
    np.testing.assert_allclose(WIDE.mean(axis=0),MEAN)
    np.testing.assert_allclose(NARROW.mean(axis=0),MEAN)
    assert (5-5)/2==0
    first=0-.1*5
    second_grad=first*(first*first-1)-5
    second=first-.1*second_grad
    np.testing.assert_allclose([first,second_grad,second],[-.5,-4.625,-.0375])
    # Exact iid batch covariance; empirical cloud is a finite reproducible sample.
    for b in [1,4,16]:np.testing.assert_allclose(covariance(b),covariance()/b)
    variances=[np.var(means(b),axis=0).sum() for b in [1,4,16]]
    assert variances[0]>variances[1]>variances[2]
    for seed in [4,9,14]:
        pts=trajectory(seed)
        for a,b in zip(pts,pts[1:]):
            residual=(a-b)/.075-full_gradient(a)
            np.testing.assert_allclose(np.abs(residual),[.8,.18],atol=1e-12)
    return dict(seed=SEED,cloud_samples=192,batches=[1,4,16],empirical_total_variances=variances,cancellation=[5,-5],eta=.1,first_step=first,second_gradient=second_grad,second_step=second)

if __name__=='__main__':print(validate())
