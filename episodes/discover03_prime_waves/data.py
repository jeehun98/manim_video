"""Exact prime-power weights and a symmetric truncation of the explicit formula."""
import numpy as np

# First 30 positive ordinates, Odlyzko zeros1 table (9 decimal places).
# https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1
GAMMAS = np.array([
    14.134725142,21.022039639,25.010857580,30.424876126,32.935061588,
    37.586178159,40.918719012,43.327073281,48.005150881,49.773832478,
    52.970321478,56.446247697,59.347044003,60.831778525,65.112544048,
    67.079810529,69.546401711,72.067157674,75.704690699,77.144840069,
    79.337375020,82.910380854,84.735492981,87.425274613,88.809111208,
    92.491899271,94.651344041,95.870634228,98.831194218,101.317851006])


def prime_weights(n=120):
    prime = np.ones(n+1,dtype=bool)
    prime[:2] = False
    for p in range(2,int(n**.5)+1):
        if prime[p]:
            prime[p*p::p] = False
    weights = np.zeros(n+1)
    for p in np.flatnonzero(prime):
        power = int(p)
        while power <= n:
            weights[power] = np.log(p)
            power *= int(p)
    return np.flatnonzero(prime), weights, np.cumsum(weights)


def pair_wave(x, gamma, beta=.5):
    x = np.asarray(x)
    rho = beta + 1j*gamma
    return -2*np.real(np.exp(rho*np.log(x))/rho)


def correction(x):
    x = np.asarray(x)
    return -np.log(2*np.pi)-.5*np.log1p(-x**-2)


def explicit_approx(x, pairs=30):
    x = np.asarray(x)
    return x+correction(x)+sum(pair_wave(x,g) for g in GAMMAS[:pairs])


def psi_midpoint(x):
    x = np.asarray(x)
    _,w,psi = prime_weights(int(np.ceil(np.max(x))))
    k = np.floor(x).astype(int)
    return psi[k] - .5*w[k]*np.isclose(x,k,rtol=0,atol=1e-10)
