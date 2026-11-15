# New periodic orbits of the planar Newtonian three-body problem

**Domain:** theoretical astrophysics / celestial mechanics. **Status:** open. There is no classification of the
periodic solutions of the three-body problem; new families keep being found numerically.

This is a lab problem of Phoenixastar, not an EinsteinArena problem. There is no public leaderboard: the
"record" is the literature catalog in `catalog.json`, and the score counts verified orbits outside it.

## Background

Three point masses attract each other with Newtonian gravity. Poincare showed the system is not integrable; periodic
orbits are the skeleton of its dynamics. For 300 years only three families were known (Euler-Lagrange, Broucke-Henon-
Hadjidemetriou, and the figure-eight of Moore 1993 / Chenciner-Montgomery 2000). Then:

- Suvakov & Dmitrasinovic, *Phys. Rev. Lett.* 110, 114301 (2013): 13 new families (butterfly, moth, bumblebee,
  dragonfly, goggles, yarn, yin-yang ...), found by scanning initial velocities and minimising a return distance.
- Li & Liao, *Sci. China-Phys. Mech. Astron.* 60, 129511 (2017): 695 families for equal masses.
- Li, Jing & Liao, *PASJ* 70, 64 (2018): 1349 families for m1 = m2 = 1, m3 in {0.5, 0.75, 2, 4, 5, 8, 10}.
- Later catalogs (Hristov et al. 2021-2024; Li, Li & Liao 2021) list more than 10,000 orbits.

## Setup (the standard one of these papers)

Planar motion, G = 1, masses m1 = m2 = 1 and m3 (m3 = 1 is the equal-mass problem; m3 != 1 is the unequal-mass
variant). Isosceles collinear start with zero total momentum and zero angular momentum:

    r1 = (-1, 0),  r2 = (1, 0),  r3 = (0, 0)
    v1 = v2 = (vx, vy),  v3 = -2 (vx, vy) / m3

A periodic orbit is a triple (vx, vy, T) (plus m3) with x(T) = x(0), v(T) = v(0). Energy E = (vx^2+vy^2)(1+2/m3)
- (1/2 + 2 m3) must be negative. The scale-invariant period is T* = T |E|^(3/2).

## Topological family

The shape of the triangle (up to translation, rotation, scale) is a point on the shape sphere. Collinear
configurations (syzygies) form its equator; the three two-body collisions are three points on the equator, cutting
it into three arcs labelled by the body in the middle. A collisionless periodic orbit is a closed curve on the
sphere minus three points, whose fundamental group is the free group on two letters. Its conjugacy class (the "free-
group word" of Suvakov-Dmitrasinovic) is equivalent to the cyclic sequence of syzygies after cancelling equal
neighbours (Montgomery 1998). `verifier.py` computes that sequence, reduces it and canonicalises it over the start
point, time reversal and relabelling of the bodies (e.g. the figure-eight is `123123`, i.e. `aBAb` ~ abAB).

An orbit whose word is a power w^k (k > 1) of a shorter closed word is a "topological-power satellite" of the family
w (Suvakov 2014: satellites of the figure-eight). The verifier reduces every word to its primitive root, and a
satellite of a catalog family is a known family, not a new one.

## Solution format and score

    {"orbits": [{"vx": 0.3471168881, "vy": 0.5327249454, "T": 6.3259139829, "m3": 1.0}, ...]}

`verifier.evaluate(solution)` integrates every orbit in float64 (adaptive Dormand-Prince 8(5,3), rtol 1e-13 and
1e-11), requires return error |r(T)-r(0)| + |v(T)-v(0)| < 1e-8 with agreement between the two step-size levels,
requires T to be the minimal period, computes the topological word, and compares with `catalog.json`
(2060 entries: Suvakov-Dmitrasinovic 2013, Li-Liao 2017, Li-Jing-Liao 2018).

**Score (maximize) = number of distinct verified families that are not in the catalog.** An orbit is counted as new
only if its canonical word matches no catalog entry (at any mass) and no catalog entry has the same m3, T* and
initial velocity. Otherwise it is a rediscovery. Baseline: 0.

## Honesty rules

- A positive score means "candidate new family relative to `catalog.json`". The catalogs listed under
  `not_included` in `catalog.json` were not checked; a claim of novelty needs those checks and a multi-precision
  confirmation.
- Same word at a different mass is treated as a known family (mass continuation), not as new.
- Orbits too unstable to close to 1e-8 in float64 are rejected.
