"""Generate frontend fixture JSON (dev-only, VITE_FIXTURES=1) matching SPEC section 4 exactly.
Uses real leaderboard records from ROOT/problems and real search snapshots read from the box."""
import json, math, os, random, datetime as dt
import numpy as np

import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = ROOT + '/web/src/fixtures'
SCR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT + '/problems', exist_ok=True)
random.seed(7)

NOW = dt.datetime(2026, 11, 15, 14, 40, 0, tzinfo=dt.timezone.utc)
def iso(t):
    return t.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def ago(**kw):
    return NOW - dt.timedelta(**kw)

def best(slug):
    return json.load(open(f'{ROOT}/problems/{slug}/best_solutions.json'))
def desc(slug):
    return open(f'{ROOT}/problems/{slug}/description.md').read()
def meta(slug):
    return json.load(open(f'{ROOT}/problems/{slug}/meta.json'))

PROBLEMS = ['no-three-in-line-75', 'spencer-discrepancy', 'hadamard-det-51', 'sidon-45-set',
            'two-deletion-code-16', 'snake-in-the-box-13', 'ring-loading-15']

def leaderboard(slug):
    rows = best(slug)
    sc = meta(slug)['scoring']
    rows = sorted(rows, key=lambda r: r['score'], reverse=(sc == 'maximize'))
    return [{'rank': i + 1, 'agent': r['agentName'], 'score': r['score']} for i, r in enumerate(rows)]

# ---- artifacts ----
nothree = json.load(open(SCR + '/box/nothree_latest.json'))
grid_art = {'kind': 'grid', 'n': 75, 'points': nothree['points'], 'violated_lines': nothree['violated_lines'],
            'count': nothree['count'], 'sym': nothree['sym'], 'round': nothree['round']}

sp_line = open(SCR + '/box/spencer.txt').read().strip().splitlines()[-1]
sp = json.loads(sp_line)
n = 20
M = np.array([[(-1 if (r >> j) & 1 else 1) for j in range(n)] for r in sp['rows']], dtype=np.int32)
# bad vectors: x in {-1,1}^n (x0 = +1, sign symmetry) with ||Ax||_inf < D
D = 8
idx = np.arange(2 ** (n - 1), dtype=np.int64)
X = np.ones((idx.size, n), dtype=np.int32)
for j in range(1, n):
    X[:, j] = 1 - 2 * ((idx >> (j - 1)) & 1)
prod = np.abs(X @ M.T).max(axis=1)
bad = int((prod < D).sum())
print('spencer bad computed', bad, 'log says', sp['bad'])
spencer_art = {'kind': 'sign_matrix', 'n': n, 'D': D, 'matrix': M.tolist(), 'bad_vectors': bad,
               'total_vectors': int(2 ** (n - 1))}

H = best('hadamard-det-51')[0]['data']['matrix']
hadamard_art = {'kind': 'sign_matrix', 'n': 51, 'matrix': H, 'log10_det': best('hadamard-det-51')[0]['score']}

sid = best('sidon-45-set')[0]
sidon_art = {'kind': 'integer_set', 'elements': sid['data']['elements'], 'h': 8, 'score': sid['score']}

tw = best('two-deletion-code-16')[0]
code_art = {'kind': 'code', 'words': tw['data']['words'][:220], 'count': 220}

# ---- strategies ----
def strat(id_, template, params, resource, started_min, adopted, metric):
    return {'id': id_, 'template': template, 'params': params, 'resource': resource,
            'started_at': iso(ago(minutes=started_min)) if started_min is not None else None,
            'adopted': adopted, 'metric_value': metric}

nothree_strats = []
for sym, seeds, base in [('rot180-150', 6, 131), ('mirror-149', 5, 178), ('diag-149', 3, 206)]:
    for s in range(seeds):
        nothree_strats.append(strat(f'adopt-nothree-{sym}-s{s}', 'nothree_sat',
                                    {'sym': sym, 'seed': s, 'solver': 'cadical195', 'presolve-slopes': 2},
                                    'cpu', 210 - s * 3, True, base + s * 7))
nothree_strats.append(strat('nt-c6-none150-s0', 'nothree_sat', {'sym': 'none-150', 'seed': 0, 'solver': 'maplechrono', 'presolve-slopes': 3}, 'cpu', 34, False, None))
spencer_strats = [strat(f'adopt-spencer-n20-s{s}', 'spencer_gpu', {'n': 20, 'D': 8, 'seed': s, 'init': 'paley', 'tenure': 24, 'restart': 50000}, 'gpu', 190 - s * 5, True, 2592) for s in range(3)]
spencer_strats.append(strat('sp-c5-n18-s5', 'spencer_gpu', {'n': 18, 'D': 8, 'seed': 5, 'init': 'random', 'tenure': 16, 'restart': 30000}, 'gpu', 48, False, 3314))
hadamard_strats = [strat(f'adopt-hadamard-s{s}', 'hadamard_gpu', {'seed': s, 'chains': 512, 'perturb': 4, 'tenure': 32, 'restart': 20000, 'target': 43.34}, 'gpu', 200 - s * 4, True, 43.33745596194) for s in (6, 7, 24, 25)]
twodel_strats = [strat(f'td-c4-ils-s{s}', 'twodel_ils', {'seed': s, 'iters': 2000000, 'kick': 6}, 'cpu', 70 - s, False, 220 - (s % 3)) for s in range(8)]
sidon_strats = [strat('adopt-sidon-extend', 'sidon_extend', {}, 'cpu', 240, True, 0.5714285714285714)]

TEMPLATES = {
    'no-three-in-line-75': [{'name': 'nothree_sat', 'resource': 'cpu', 'params': {
        'sym': {'type': 'enum', 'values': ['mirror-149', 'rot180-150', 'diag-149', 'diag-150', 'none-149', 'none-150'], 'default': 'rot180-150'},
        'seed': {'type': 'int', 'min': 0, 'max': 9999, 'default': 0},
        'solver': {'type': 'enum', 'values': ['cadical195', 'glucose4', 'maplechrono'], 'default': 'cadical195'},
        'presolve_slopes': {'type': 'int', 'min': 0, 'max': 12, 'default': 4}}}],
    'spencer-discrepancy': [{'name': 'spencer_gpu', 'resource': 'gpu', 'params': {
        'n': {'type': 'int', 'min': 2, 'max': 20, 'default': 20},
        'D': {'type': 'int', 'min': 1, 'max': 20, 'default': 8},
        'seed': {'type': 'int', 'min': 0, 'max': 9999, 'default': 0},
        'init': {'type': 'enum', 'values': ['random', 'paley'], 'default': 'paley'},
        'tenure': {'type': 'int', 'min': 1, 'max': 400, 'default': 24},
        'restart': {'type': 'int', 'min': 1000, 'max': 1000000, 'default': 50000}}}],
    'hadamard-det-51': [{'name': 'hadamard_gpu', 'resource': 'gpu', 'params': {
        'seed': {'type': 'int', 'min': 0, 'max': 9999, 'default': 0},
        'chains': {'type': 'int', 'min': 1, 'max': 4096, 'default': 512},
        'perturb': {'type': 'int', 'min': 1, 'max': 64, 'default': 4},
        'tenure': {'type': 'int', 'min': 1, 'max': 400, 'default': 32},
        'restart': {'type': 'int', 'min': 1000, 'max': 1000000, 'default': 20000},
        'target': {'type': 'float', 'min': 40, 'max': 50, 'default': 43.34}}}],
    'sidon-45-set': [{'name': 'sidon_extend', 'resource': 'cpu', 'params': {}},
                     {'name': 'sidon_sa', 'resource': 'cpu', 'params': {
                         'size': {'type': 'int', 'min': 4, 'max': 18, 'default': 15},
                         'span': {'type': 'int', 'min': 100, 'max': 100000, 'default': 4000},
                         'seed': {'type': 'int', 'min': 0, 'max': 9999, 'default': 0},
                         'temp': {'type': 'float', 'min': 0.01, 'max': 10, 'default': 0.5}}}],
    'two-deletion-code-16': [{'name': 'twodel_ils', 'resource': 'cpu', 'params': {
        'seed': {'type': 'int', 'min': 0, 'max': 9999, 'default': 0},
        'iters': {'type': 'int', 'min': 1000, 'max': 100000000, 'default': 2000000},
        'kick': {'type': 'int', 'min': 1, 'max': 32, 'default': 6}}}],
    'snake-in-the-box-13': [],
    'ring-loading-15': [],
}

def summary(slug, title, record, holder, ours, metric, status, gpus, cpu, strategies):
    sc = meta(slug)['scoring']
    beats = False
    if ours:
        beats = ours['score'] > record if sc == 'maximize' else ours['score'] < record
    return {'slug': slug, 'title': title, 'scoring': sc, 'record': {'score': record, 'holder': holder},
            'ours': ours, 'beats_record': beats, 'metric': metric, 'status': status,
            'compute': {'gpus': gpus, 'cpu_procs': cpu, 'share': 0.0}, 'strategies': strategies}

def ours(score, mins, sid):
    return {'score': score, 'verified': True, 'at': iso(ago(minutes=mins)), 'strategy_id': sid}

problems = [
    summary('no-three-in-line-75', meta('no-three-in-line-75')['title'], 148, 'Thomas-Prellberg', None,
            {'name': 'min_violated_lines', 'value': 131, 'target': 0, 'lower_is_better': True}, 'searching', 0, 109, nothree_strats),
    summary('spencer-discrepancy', meta('spencer-discrepancy')['title'], 1.697749375254331, 'Youhua-Li',
            ours(1.697749375254331, 170, 'adopt-spencer-n20-s0'),
            {'name': 'bad_vectors', 'value': bad, 'target': 0, 'lower_is_better': True}, 'searching', 4, 0, spencer_strats),
    summary('hadamard-det-51', meta('hadamard-det-51')['title'], 43.33745596194037, 'kgrey',
            ours(43.33745596194037, 150, 'adopt-hadamard-s6'),
            {'name': 'best_log10', 'value': 43.33745596194, 'target': 43.33745596194037, 'lower_is_better': False}, 'stalled', 4, 0, hadamard_strats),
    summary('sidon-45-set', meta('sidon-45-set')['title'], 0.5714285714285714, 'Ma-Tang',
            ours(0.5714285714285714, 230, 'adopt-sidon-extend'),
            {'name': 'best_score', 'value': 0.5714285714285714, 'target': 0.5714285714285714, 'lower_is_better': True}, 'proved-negative', 0, 1, sidon_strats),
    summary('two-deletion-code-16', meta('two-deletion-code-16')['title'], 226, 'kgrey', ours(220, 12, 'td-c4-ils-s0'),
            {'name': 'best_size', 'value': 220, 'target': 227, 'lower_is_better': False}, 'searching', 0, 8, twodel_strats),
    summary('snake-in-the-box-13', meta('snake-in-the-box-13')['title'], 2950, 'kgrey', None,
            {'name': 'best_length', 'value': None, 'target': 2951, 'lower_is_better': False}, 'idle', 0, 0, []),
    summary('ring-loading-15', meta('ring-loading-15')['title'], 1.125, 'JSAgent-Ring15', None,
            {'name': 'best_score', 'value': None, 'target': 1.125, 'lower_is_better': False}, 'idle', 0, 0, []),
]
total_units = sum(p['compute']['gpus'] * 8 + p['compute']['cpu_procs'] for p in problems)
for p in problems:
    p['compute']['share'] = round((p['compute']['gpus'] * 8 + p['compute']['cpu_procs']) / total_units, 4)

gpu_owner = ['spencer-discrepancy'] * 4 + ['hadamard-det-51'] * 4
gpu_strat = ['adopt-spencer-n20-s0', 'adopt-spencer-n20-s1', 'adopt-spencer-n20-s2', 'sp-c5-n18-s5',
             'adopt-hadamard-s6', 'adopt-hadamard-s7', 'adopt-hadamard-s24', 'adopt-hadamard-s25']
real_gpu = [(93, 805), (93, 725), (96, 805), (95, 805), (98, 1269), (99, 1271), (95, 1355), (98, 1355)]
compute = {'gpus': [{'idx': i, 'util': u, 'mem_mb': m, 'problem': gpu_owner[i], 'strategy_id': gpu_strat[i]} for i, (u, m) in enumerate(real_gpu)],
           'cpus': 124, 'load1': 119.97, 'cpu_procs': {'no-three-in-line-75': 109, 'two-deletion-code-16': 8, 'sidon-45-set': 1}, 'box': 'online'}

# ---- literature ----
LIT = [
    ('no-three-in-line-75', 'no-three-in-line problem large n constructions symmetry', 'No-three-in-line problem', 'https://en.wikipedia.org/wiki/No-three-in-line_problem', None,
     'Solutions with 2n points are known for every n up to 46; it is conjectured that for large n fewer than 2n points are possible. Most known solutions have some symmetry of the square.'),
    ('no-three-in-line-75', 'no-three-in-line 2n point counts table Flammenkamp', 'Achim Flammenkamp: The No-Three-in-Line Problem', 'https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html', '1998-01-01',
     'Configurations with 2n points restricted to symmetry classes (rotation by 180 degrees, reflections) were found by exhaustive branch and bound, which reduces the search space drastically.'),
    ('no-three-in-line-75', 'OEIS no-3-in-line 2n points sequence', 'A000769: No-3-in-line problem on n X n grid', 'https://oeis.org/A000769', None,
     'Number of inequivalent ways of placing 2n points on an n X n grid so that no 3 are in a line.'),
    ('no-three-in-line-75', 'incremental SAT lazy clause generation geometry', 'CaDiCaL SAT solver', 'https://github.com/arminbiere/cadical', None,
     'CaDiCaL is a simplified satisfiability solver with incremental solving support: clauses can be added between calls without restarting.'),
    ('spencer-discrepancy', 'Spencer six standard deviations discrepancy sign matrix', 'Discrepancy theory', 'https://en.wikipedia.org/wiki/Discrepancy_theory', None,
     'Spencer showed that for n sets on n points there is a colouring with discrepancy at most 6 sqrt(n), improving the random bound by a log factor.'),
    ('spencer-discrepancy', 'Paley construction conference matrix order 18 20', 'Paley construction', 'https://en.wikipedia.org/wiki/Paley_construction', None,
     'Paley constructions give Hadamard and conference matrices from quadratic residues in finite fields; they are natural high-discrepancy starting points.'),
    ('hadamard-det-51', 'maximal determinant +-1 matrix order 51 records', 'Hadamard\'s maximal determinant problem', 'https://en.wikipedia.org/wiki/Hadamard%27s_maximal_determinant_problem', None,
     'For n = 3 mod 4 the best known upper bound is due to Ehlich; record matrices for many orders come from block constructions and local search.'),
    ('hadamard-det-51', 'large determinant sign matrices table Orrick Solomon', 'Large-determinant sign matrices of order 4k+3', 'http://www.indiana.edu/~maxdet/', None,
     'Tables of the largest known determinants of +-1 matrices by order, with constructions and references.'),
    ('sidon-45-set', 'Sidon subsets of (4,5)-sets Erdos problem', 'Sidon sequence', 'https://en.wikipedia.org/wiki/Sidon_sequence', None,
     'A Sidon set has all pairwise sums distinct. Erdos asked how large a Sidon subset must exist inside sets with few repeated differences.'),
    ('two-deletion-code-16', 'two deletion correcting codes length 16 largest known', 'Deletion channel', 'https://en.wikipedia.org/wiki/Deletion_channel', None,
     'Codes correcting s deletions; Varshamov-Tenengolts codes are optimal-ish for one deletion, while for two deletions the best sizes are found by clique search.'),
    ('two-deletion-code-16', 'iterated local search maximum independent set conflict graph', 'Tabu search', 'https://en.wikipedia.org/wiki/Tabu_search', None,
     'Tabu search forbids recently visited moves for a tenure, letting a local search escape local optima; widely used for max-independent-set heuristics.'),
    ('snake-in-the-box-13', 'snake in the box dimension 13 longest known', 'Snake-in-the-box', 'https://en.wikipedia.org/wiki/Snake-in-the-box', None,
     'The longest known snakes for dimensions 9 and above come from stochastic beam search and priming constructions.'),
]
literature = []
for i, (prob, q, title, url, pub, hl) in enumerate(LIT):
    literature.append({'id': i + 1, 'problem': prob, 'query': q, 'title': title, 'url': url, 'published': pub, 'highlight': hl, 'cited_by': []})

def src(i):
    l = literature[i - 1]
    return {'id': l['id'], 'title': l['title'], 'url': l['url'], 'published': l['published']}

# ---- memory facts ----
F = [
    ('f_001', 'agent:no-three-in-line-75', 'no-three-in-line-75', 'rot180-150 class converges fastest: median 44 rounds, min violated lines 151 after 3h; mirror-149 plateaus near 178.', 200, ['planner', 'proposer']),
    ('f_002', 'critic', 'no-three-in-line-75', 'Prediction refuted: diag-149 was expected to reach <150 violated lines within 60 min; observed 206. Diagonal symmetry adds too many forced collinear triples.', 150, ['proposer', 'agent:no-three-in-line-75']),
    ('f_003', 'agent:spencer-discrepancy', 'spencer-discrepancy', 'n=20 D=8 tabu from Paley init stalls at 2592 bad vectors on all 3 seeds; identical plateau suggests a structural barrier, not bad luck.', 120, ['planner', 'proposer', 'critic']),
    ('f_004', 'agent:hadamard-det-51', 'hadamard-det-51', 'All 6 hadamard chains seeded from the kgrey record matrix return to 43.33745596194 within 100 steps; neighbourhood of the record looks locally optimal under 1-4 flips.', 110, ['planner', 'proposer']),
    ('f_005', 'agent:sidon-45-set', 'sidon-45-set', 'Exact search: the Ma-Tang 14-element set has no 1-point extension and no 2-point extension inside [-3000, 4000]. Status: proved-negative for small extensions.', 230, ['planner', 'critic', 'proposer']),
    ('f_006', 'planner', None, 'GPU budget split 4/4 spencer/hadamard; 109 CPU cores on no-three SAT. Free resources: 3 cores.', 90, ['proposer']),
    ('f_007', 'proposer', 'two-deletion-code-16', 'Launched twodel_ils x8 with kick=6: conflict-graph ILS reached 220 words in 12 min (record 226).', 12, ['planner', 'agent:two-deletion-code-16']),
    ('f_008', 'critic', 'spencer-discrepancy', 'Verified with official verifier: our n=17 Paley-derived matrix scores 1.697749375254331, equal to the record (no improvement, minImprovement 1e-6).', 170, ['proposer', 'agent:spencer-discrepancy']),
    ('f_009', 'agent:two-deletion-code-16', 'two-deletion-code-16', 'Words with long runs (>=6 equal bits) are rarely in large codes; seeding ILS from the record minus run-heavy words speeds convergence.', 8, ['proposer']),
    ('f_010', 'proposer', 'no-three-in-line-75', 'Exa: Flammenkamp found 2n-point solutions for large n mainly in rotation-symmetric classes; supports shifting more seeds to rot180-150.', 60, ['planner', 'agent:no-three-in-line-75']),
    ('f_011', 'critic', 'hadamard-det-51', 'Prediction confirmed: hadamard stays at record after 90 min (expected no gain). Recommend reallocating 2 GPUs.', 40, ['planner']),
    ('f_012', 'planner', 'spencer-discrepancy', 'Priority drop: spencer gap closed per GPU-hour = 0 for 4 cycles; keep 2 GPUs as exploration, release 2.', 30, ['proposer', 'critic']),
    ('f_013', 'agent:no-three-in-line-75', 'no-three-in-line-75', 'Round-55 rot180-150 s0 model: 150 points, 131 violated lines, 12475 lazy line clauses. Violations concentrate on slopes 1/2, 2, -1/3.', 5, ['proposer', 'planner']),
]
facts = [{'id': fid, 'agent': ag, 'problem': pr, 'text': tx, 'time': iso(ago(minutes=m)), 'read_by': rb} for fid, ag, pr, tx, m, rb in F]
links = []
for f in facts:
    for r in f['read_by']:
        links.append({'from_agent': f['agent'], 'to_agent': r, 'fact_id': f['id']})
agents = ['planner', 'proposer', 'critic'] + [f'agent:{s}' for s in PROBLEMS[:5]]
memory = {'facts': facts, 'agents': agents, 'links': links,
          'benchmark': {'systems': [
              {'name': 'past.dev', 'accuracy': 0.88, 'latency_ms': 412.0, 'cost_usd': 0.0009, 'n': 40},
              {'name': 'markdown', 'accuracy': 0.73, 'latency_ms': 2870.0, 'cost_usd': 0.0187, 'n': 40},
              {'name': 'rag', 'accuracy': 0.80, 'latency_ms': 655.0, 'cost_usd': 0.0014, 'n': 40}],
              'time': iso(ago(minutes=25))}}

# ---- decisions ----
decisions = []
did = [0]
def D_(cycle, mins, agent, problem, action, rationale, params=None, prediction=None, outcome=None, sources=(), reads=(), writes=(), model=None, tokens=None, latency=None):
    did[0] += 1
    d = {'id': did[0], 'cycle': cycle, 'time': iso(ago(minutes=mins)), 'agent': agent, 'problem': problem, 'action': action,
         'params': params or {}, 'rationale': rationale, 'prediction': prediction, 'outcome': outcome,
         'sources': [src(s) for s in sources], 'memory_reads': list(reads), 'memory_writes': list(writes),
         'model': model, 'tokens': tokens, 'latency_ms': latency}
    for s in sources:
        literature[s - 1]['cited_by'].append(d['id'])
    decisions.append(d)
    return d

P = 'gpt-6-astra'
FAST = 'gpt-5.4-mini'
cyc = 1
for c, base in [(1, 240), (2, 200), (3, 150), (4, 100), (5, 55), (6, 18)]:
    D_(c, base, 'system', None, 'cycle_start', f'Cycle {c} started: telemetry pulled from 8 GPUs and 124 cores.', params={'interval_s': 300})
    D_(c, base - 0.5, 'planner', None, 'priorities', 'UCB priority over gap-closed-per-compute-hour and staleness: no-three 0.81, two-deletion 0.64, spencer 0.38, hadamard 0.21, sidon 0.05.',
       params={'free_gpus': 0, 'free_cores': 3}, reads=['f_006'], model=None)

D_(1, 239, 'executor', 'no-three-in-line-75', 'adopt', 'Adopted 109 running nothree_sat processes found via pgrep (5 symmetry classes); not restarted.', params={'count': 109})
D_(1, 238, 'executor', 'spencer-discrepancy', 'adopt', 'Adopted 6 spencer_gpu processes on GPUs 0-3.', params={'count': 6})
D_(1, 238, 'executor', 'hadamard-det-51', 'adopt', 'Adopted 6 hadamard_gpu processes on GPUs 4-7.', params={'count': 6})
D_(1, 236, 'literature', 'no-three-in-line-75', 'search', 'Exa search for prior 2n-point constructions under symmetry to decide which classes to favour.', params={'query': LIT[1][1], 'results': 3}, sources=[1, 2, 3])
D_(1, 234, 'proposer', 'no-three-in-line-75', 'keep', 'Keep all five symmetry classes running for one more cycle to measure convergence rates before reallocating cores.',
   prediction={'metric': 'min_violated_lines', 'expected': 170, 'horizon_min': 60},
   outcome={'observed': 178, 'verdict': 'refuted', 'note': 'min violated 178 after 60 min (mirror-149); rot180 not yet converged'},
   sources=[2], reads=['f_006'], writes=['f_010'], model=P, tokens=6120, latency=8400)
D_(1, 233, 'critic', 'sidon-45-set', 'verify', 'Re-ran official verifier on the record 14-element set: 0.5714285714285714 (h=8). Our best equals the record; no record declared.', params={'score': 0.5714285714285714}, writes=['f_005'])
D_(2, 198, 'critic', 'spencer-discrepancy', 'verify', 'Official verifier on our n=17 matrix: 1.697749375254331 = 7/sqrt(17), equal to the record. minImprovement 1e-6 not met.', writes=['f_008'])
D_(2, 196, 'proposer', 'hadamard-det-51', 'keep', 'Hadamard chains are at the record value; keep for one cycle since GPU tabu needs ~2h to escape the basin according to step rates.',
   prediction={'metric': 'best_log10', 'expected': 43.33745596194, 'horizon_min': 90},
   outcome={'observed': 43.33745596194, 'verdict': 'confirmed', 'note': 'no gain, as predicted'}, reads=['f_004'], model=P, tokens=5410, latency=7300)
D_(2, 195, 'literature', 'hadamard-det-51', 'search', 'Exa search for record tables of order 4k+3 max-det matrices.', params={'query': LIT[7][1], 'results': 2}, sources=[7, 8])
D_(3, 148, 'proposer', 'spencer-discrepancy', 'note', 'All n=20 D=8 seeds share the 2592 plateau; propose testing n=18 D=8 (target ratio 8/sqrt(18)=1.8856) on one GPU.',
   prediction={'metric': 'bad_vectors', 'expected': 2000, 'horizon_min': 60},
   outcome={'observed': 3314, 'verdict': 'refuted', 'note': 'n=18 plateau 3314'}, sources=[5, 6], reads=['f_003'], model=P, tokens=7020, latency=9100)
D_(3, 147, 'planner', 'spencer-discrepancy', 'launch', 'Validated spencer_gpu params against schema; GPU 3 freed by stopping seed 3 (identical plateau).',
   params={'template': 'spencer_gpu', 'n': 18, 'D': 8, 'seed': 5, 'init': 'random', 'tenure': 16, 'restart': 30000, 'gpu': 3})
D_(3, 146, 'executor', 'spencer-discrepancy', 'launch', 'Launched sp-c5-n18-s5 on GPU 3 (CUDA_VISIBLE_DEVICES=3).', params={'strategy_id': 'sp-c5-n18-s5', 'pid': 412233})
D_(3, 145, 'critic', 'no-three-in-line-75', 'score_prediction', 'Prediction from cycle 1 refuted (expected 170, observed 178). Lesson written to memory.', writes=['f_002'])
D_(4, 98, 'literature', 'two-deletion-code-16', 'search', 'New problem in portfolio: searched for two-deletion code constructions and local search methods.', params={'query': LIT[9][1], 'results': 2}, sources=[10, 11])
D_(4, 96, 'proposer', 'two-deletion-code-16', 'launch', 'No strategy yet for two-deletion-code-16. Conflict-graph iterated local search with random kicks is cheap on CPU; use the 8 cores freed by stopping diag-150 seeds.',
   params={'template': 'twodel_ils', 'seeds': 8, 'kick': 6},
   prediction={'metric': 'best_size', 'expected': 222, 'horizon_min': 30},
   outcome={'observed': 220, 'verdict': 'refuted', 'note': 'reached 220 after 30 min'}, sources=[10, 11], reads=['f_006'], writes=['f_007'], model=P, tokens=8830, latency=11200)
D_(4, 95, 'executor', 'two-deletion-code-16', 'launch', 'Launched td-c4-ils-s0..s7 (8 CPU cores).', params={'count': 8})
D_(4, 94, 'executor', 'no-three-in-line-75', 'stop', 'Stopped 8 diag-150 seeds (no model after 2h, lowest priority class).', params={'count': 8})
D_(5, 54, 'proposer', 'no-three-in-line-75', 'research', 'rot180-150 has the steepest violated-lines decline; Flammenkamp reports most large 2n solutions are rotation-symmetric. Ask literature agent for slope-presolve tricks.',
   sources=[2, 4], reads=['f_001', 'f_010'], model=P, tokens=6650, latency=8800)
D_(5, 53, 'memory', None, 'recall', 'Recalled 6 facts for proposer from past.dev shared space ltd-lab (level high).', params={'k': 6, 'latency_ms': 388}, reads=['f_001', 'f_002', 'f_003', 'f_004', 'f_006', 'f_010'])
D_(5, 50, 'sandbox', 'sidon-45-set', 'sandbox', 'Proposer wrote 8 Sidon search programs; ran 8 Modal sandboxes in parallel (120 s each). Best valid score 0.6 (9/15), worse than record.', params={'n': 8, 'ok': 6, 'invalid': 1, 'timeout': 1})
D_(5, 48, 'critic', 'hadamard-det-51', 'score_prediction', 'Prediction confirmed: no gain on hadamard over 90 min.', writes=['f_011'])
D_(6, 17, 'planner', 'spencer-discrepancy', 'reallocate', 'Spencer gap closed per GPU-hour is 0 for 4 cycles. Keep 2 GPUs exploring, mark 2 for release next cycle.', writes=['f_012'])
D_(6, 15, 'proposer', 'no-three-in-line-75', 'launch', 'Add one unsymmetric none-150 seed with maplechrono and 6 presolved slopes as a control for the symmetry hypothesis.',
   params={'template': 'nothree_sat', 'sym': 'none-150', 'seed': 0, 'solver': 'maplechrono', 'presolve-slopes': 3},
   prediction={'metric': 'min_violated_lines', 'expected': 125, 'horizon_min': 45},
   outcome={'observed': None, 'verdict': 'pending', 'note': ''}, sources=[1, 4], reads=['f_001', 'f_013'], model=P, tokens=7310, latency=9600)
D_(6, 12, 'learning', 'sidon-45-set', 'train_step', 'Tinker GRPO step 40: reward mean 0.61, best 0.83, valid rate 0.91.', params={'step': 40})
D_(6, 8, 'critic', 'two-deletion-code-16', 'verify', 'Official verifier on td-c4-ils-s0 best code: 220 words, valid. Record 226 not beaten.', params={'score': 220}, writes=['f_009'])
D_(6, 5, 'memory', 'no-three-in-line-75', 'write', 'Wrote round-55 model summary for agent:no-three-in-line-75 to past.dev.', writes=['f_013'])
D_(6, 3, 'proposer', 'two-deletion-code-16', 'keep', 'ILS still improving (218 -> 220 in 10 min); keep all 8 seeds.',
   prediction={'metric': 'best_size', 'expected': 223, 'horizon_min': 40}, outcome={'observed': None, 'verdict': 'pending', 'note': ''},
   reads=['f_007', 'f_009'], model=FAST, tokens=2110, latency=1900)
decisions.sort(key=lambda d: d['id'], reverse=True)

# ---- metric history ----
def hist(points):
    return [[iso(ago(minutes=m)), v] for m, v in points]
mh = {
    'no-three-in-line-75': hist([(240 - i * 6, round(262 - 131 * (1 - math.exp(-i / 14)) + random.uniform(-3, 3))) for i in range(40)] + [(0, 131)]),
    'spencer-discrepancy': hist([(240 - i * 8, int(2592 + 9000 * math.exp(-i / 3))) for i in range(30)]),
    'hadamard-det-51': hist([(240 - i * 8, 43.33745596194) for i in range(30)]),
    'sidon-45-set': hist([(240 - i * 20, 0.5714285714285714) for i in range(12)]),
    'two-deletion-code-16': hist([(96 - i * 3, 180 + int(40 * (1 - math.exp(-i / 9)))) for i in range(32)]),
    'snake-in-the-box-13': [],
    'ring-loading-15': [],
}
arts = {'no-three-in-line-75': grid_art, 'spencer-discrepancy': spencer_art, 'hadamard-det-51': hadamard_art,
        'sidon-45-set': sidon_art, 'two-deletion-code-16': code_art, 'snake-in-the-box-13': None, 'ring-loading-15': None}

# align with the strategies builder's registry where it exists
try:
    import re
    raw = open(ROOT + '/search/TEMPLATES.json').read()
    reg = json.loads(raw)
    for name, t in reg.items():
        prob = t.get('problem')
        if prob in TEMPLATES:
            entry = {'name': name, 'resource': t.get('resource', 'cpu'), 'params': t.get('params', {})}
            TEMPLATES[prob] = [entry] + [x for x in TEMPLATES[prob] if x['name'] != name]
except Exception as e:
    print('templates registry not used:', e)

for p in problems:
    detail = dict(p)
    detail.update({'description_md': desc(p['slug']), 'leaderboard': leaderboard(p['slug']), 'metric_history': mh[p['slug']],
                   'artifact': arts[p['slug']], 'templates': TEMPLATES[p['slug']]})
    json.dump(detail, open(f"{OUT}/problems/{p['slug']}.json", 'w'), separators=(',', ':'))

state = {'now': iso(NOW),
         'loop': {'status': 'running', 'cycle': 6, 'phase': 'idle', 'next_cycle_at': iso(NOW + dt.timedelta(seconds=140)), 'interval_s': 300,
                  'proposer_model': P, 'started_at': iso(ago(minutes=242))},
         'compute': compute, 'problems': problems,
         'totals': {'decisions': len(decisions), 'cycles': 6, 'experiments_run': 31, 'sandboxes_run': 8, 'facts': len(facts), 'sources': len(literature), 'records': 0}}
json.dump(state, open(OUT + '/state.json', 'w'), indent=1)
json.dump(decisions, open(OUT + '/decisions.json', 'w'), indent=1)
json.dump(memory, open(OUT + '/memory.json', 'w'), indent=1)
json.dump(literature, open(OUT + '/literature.json', 'w'), indent=1)

# ---- learning ----
steps = []
for s in range(41):
    rm = 0.08 + 0.53 * (1 - math.exp(-s / 13)) + random.uniform(-0.025, 0.025)
    rb = min(1.0, rm + 0.15 + random.uniform(0, 0.08))
    vr = 0.22 + 0.69 * (1 - math.exp(-s / 10)) + random.uniform(-0.03, 0.03)
    steps.append({'step': s, 'reward_mean': round(rm, 4), 'reward_best': round(rb, 4), 'valid_rate': round(min(vr, 1), 4), 'time': iso(ago(minutes=120 - s * 2.6))})
learning = {'status': 'running', 'base_model': 'Qwen/Qwen3-8B', 'problem': 'sidon-45-set', 'steps': steps,
            'eval': {'gen0': {'score': 0.31, 'valid_rate': 0.19}, 'genN': {'score': 0.58, 'valid_rate': 0.83}, 'heldout': 'spencer-discrepancy n<=8'},
            'best': {'solution': {'elements': [0, 1, 3, 7, 12, 20, 30, 44, 65, 80, 96, 122, 147, 181, 203]}, 'score': 0.6}}
json.dump(learning, open(OUT + '/learning.json', 'w'), indent=1)

# ---- sandboxes ----
CODE_SIDON = '''import itertools, json, random

def sidon_size(A):
    best = 0
    for r in range(len(A), 0, -1):
        for S in itertools.combinations(A, r):
            sums = [x + y for i, x in enumerate(S) for y in S[i:]]
            if len(sums) == len(set(sums)):
                return r
    return best

def is_45(A):
    for Q in itertools.combinations(A, 4):
        if len({abs(a - b) for a, b in itertools.combinations(Q, 2)}) < 5:
            return False
    return True

random.seed(%d)
best, best_A = 1.0, None
for it in range(%d):
    A = sorted(random.sample(range(0, %d), 15))
    if not is_45(A):
        continue
    s = sidon_size(A) / len(A)
    if s < best:
        best, best_A = s, A
print(json.dumps({"elements": best_A}))
'''
CODE_SPENCER = '''import json, numpy as np
rng = np.random.default_rng(%d)
n = %d
A = rng.choice([-1, 1], size=(n, n))
X = np.array([[1 - 2 * ((i >> j) & 1) for j in range(n)] for i in range(2 ** (n - 1))])
def disc(A):
    return np.abs(X @ A.T).max(axis=1).min()
best = disc(A)
for step in range(%d):
    i, j = rng.integers(n), rng.integers(n)
    A[i, j] *= -1
    d = disc(A)
    if d >= best:
        best = d
    else:
        A[i, j] *= -1
print(json.dumps({"matrix": A.tolist()}))
'''
sandboxes = []
rows = [('sidon-45-set', 'ok', 0.6, 64.2), ('sidon-45-set', 'ok', 0.6667, 71.9), ('sidon-45-set', 'invalid', None, 12.4),
        ('sidon-45-set', 'ok', 0.6, 88.0), ('sidon-45-set', 'timeout', None, 120.0), ('sidon-45-set', 'ok', 0.6429, 59.3),
        ('sidon-45-set', 'ok', 0.6667, 101.7), ('sidon-45-set', 'error', None, 2.1),
        ('spencer-discrepancy', 'ok', 1.5, 43.0), ('spencer-discrepancy', 'ok', 1.6330, 77.5)]
sid_dec = next(d['id'] for d in decisions if d['agent'] == 'sandbox')
for i, (prob, st, scv, secs) in enumerate(rows):
    code = CODE_SIDON % (i, 20000 + i * 5000, 2000 + i * 300) if prob == 'sidon-45-set' else CODE_SPENCER % (i, 6 + i % 3 * 2, 3000)
    sandboxes.append({'id': 100 + i, 'problem': prob, 'time': iso(ago(minutes=50 - i * 0.3)), 'code': code, 'status': st,
                      'score': scv, 'seconds': secs, 'decision_id': sid_dec})
sandboxes.sort(key=lambda s: s['id'], reverse=True)
json.dump(sandboxes, open(OUT + '/sandboxes.json', 'w'), indent=1)
json.dump([], open(OUT + '/gallery.json', 'w'))
print('ok', len(decisions), 'decisions', len(facts), 'facts')
