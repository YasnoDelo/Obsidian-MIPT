#!/usr/bin/env python3
"""Two finite FCFS nodes and a common finite retrial orbit.
Python >=3.10; dependencies: numpy, scipy.
Run: python two_phase_orbit.py --reps 24 --duration 50000 --warmup 5000
Prints readable tables; saves results.md and results.json in --output directory.
Time unit is arbitrary.
Analytical tagged chain and ID-based simulation are separate implementations.
"""
from __future__ import annotations
import argparse
from collections import deque
from dataclasses import dataclass, asdict
from itertools import product
import json
from pathlib import Path
import random
import platform
import numpy as np
import scipy
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.stats import t as student_t

@dataclass(frozen=True)
class Params:
    lam: float
    mu1: float
    mu2: float
    nu: float
    c1: int
    c2: int
    k: int
    def validate(self):
        assert min(self.lam, self.mu1, self.mu2, self.nu) > 0
        assert self.c1 >= 1 and self.c2 >= 1 and self.k >= 0
        assert all(isinstance(x, int) for x in (self.c1, self.c2, self.k))


def aggregate(p):
    """Occupancy generator: no tagged job, no artificial self transitions."""
    states = list(product(range(p.c1+1), range(p.c2+1), range(p.k+1)))
    idx = {s: n for n, s in enumerate(states)}
    q = np.zeros((len(states), len(states)))
    for a, (i, j, r) in enumerate(states):
        transitions = []
        if i < p.c1:
            transitions.append(((i+1, j, r), p.lam))
            if r: transitions.append(((i+1, j, r-1), r*p.nu))
        elif r < p.k:
            transitions.append(((i, j, r+1), p.lam))
        if i:
            if j < p.c2: dst = (i-1, j+1, r)
            elif r < p.k: dst = (i-1, j, r+1)
            else: dst = (i-1, j, r)
            transitions.append((dst, p.mu1))
        if j: transitions.append(((i, j-1, r), p.mu2))
        for dst, rate in transitions: q[a, idx[dst]] += rate
        q[a, a] = -q[a].sum()
    a = q.T.copy()
    a[-1] = 1
    b = np.zeros(len(states)); b[-1] = 1
    pi = np.linalg.solve(a, b)
    assert pi.min() > -1e-12
    assert np.max(np.abs(pi @ q)) < 1e-10
    return states, pi, q


def tagged_events(s, p):
    """s=(queue1,queue2,ordinary_orbit,tag_in_orbit); 1 is tagged, 0 ordinary.
    Destinations 'S','L' absorb the tag. Ordinary losses leave the tag alive.
    Self events are returned and subsequently omitted from the generator.
    """
    a, b, r, o = s
    def state(aa=a, bb=b, rr=r, oo=o): return (aa, bb, rr, oo)
    def to_orbit(job, aa, bb):
        if r+o < p.k:
            return state(aa, bb, r+(job == 0), o+(job == 1))
        return 'L' if job else state(aa, bb)
    if len(a) < p.c1: dst = state(a+(0,))
    else: dst = to_orbit(0, a, b)
    yield dst, p.lam
    if a:
        job, aa = a[0], a[1:]
        if len(b) < p.c2: dst = state(aa, b+(job,))
        else: dst = to_orbit(job, aa, b)
        yield dst, p.mu1
    if b:
        yield ('S' if b[0] else state(bb=b[1:])), p.mu2
    if r:
        yield (state(a+(0,), rr=r-1) if len(a)<p.c1 else s), r*p.nu
    if o:
        yield (state(a+(1,), oo=0) if len(a)<p.c1 else s), p.nu


def analytical(p):
    p.validate()
    states, pi, q = aggregate(p)
    out = p.mu2*sum(v for (i,j,r),v in zip(states,pi) if j)
    ext_loss = p.lam*sum(v for (i,j,r),v in zip(states,pi) if i==p.c1 and r==p.k)
    int_loss = p.mu1*sum(v for (i,j,r),v in zip(states,pi) if i and j==p.c2 and r==p.k)
    ploss = (ext_loss+int_loss)/p.lam
    mean_n = sum((i+j+r)*v for (i,j,r),v in zip(states,pi))
    # PASTA initial distribution after insertion of an external tagged arrival.
    initial = {}
    immediate = 0.
    for (i,j,r),v in zip(states,pi):
        if i < p.c1: s = ((0,)*i+(1,), (0,)*j, r, 0)
        elif r < p.k: s = ((0,)*i, (0,)*j, r, 1)
        else:
            immediate += v
            continue
        initial[s] = initial.get(s,0.)+v
    tagged = list(initial); index = {s:i for i,s in enumerate(tagged)}
    rows, cols, data, success, loss = [], [], [], [], []
    n = 0
    while n < len(tagged):
        s = tagged[n]; rate_sum = 0.; bs = bl = 0.
        for dst, rate in tagged_events(s,p):
            if dst == s: continue
            rate_sum += rate
            if dst == 'S': bs += rate
            elif dst == 'L': bl += rate
            else:
                if dst not in index:
                    index[dst] = len(tagged); tagged.append(dst)
                rows.append(n); cols.append(index[dst]); data.append(rate)
        rows.append(n); cols.append(n); data.append(-rate_sum)
        success.append(bs); loss.append(bl); n += 1
    t = coo_matrix((data,(rows,cols)),shape=(n,n)).tocsc()
    alpha = np.zeros(n)
    for s,v in initial.items(): alpha[index[s]] += v
    bs, bl = np.array(success), np.array(loss)
    h = spsolve(-t, bs)
    g = spsolve(-t, h)
    u = spsolve(-t, np.ones(n))
    ell = spsolve(-t, bl)
    ps = float(alpha@h)
    w = float(alpha@g/ps)
    unconditional = float(alpha@u)
    assert np.max(np.abs(t@h+bs))/(1+np.max(bs)) < 1e-10
    assert np.max(np.abs(t@g+h))/(1+np.max(np.abs(t.data))*np.max(np.abs(g))) < 1e-10
    assert np.max(np.abs(h+ell-1)) < 1e-10
    assert abs(ploss-(immediate+alpha@ell)) < 1e-10
    assert abs(ps+ploss-1) < 1e-10
    assert abs(out-p.lam*ps) < 1e-10
    assert abs(unconditional-mean_n/p.lam) < 1e-9
    return dict(loss=ploss, delay_success=w, throughput=out,
                mean_n=mean_n, time_until_exit=unconditional,
                external_loss_rate=ext_loss, internal_loss_rate=int_loss,
                immediate_loss=immediate, states=len(states), tagged_states=n,
                balance_residual=float(abs(p.lam-out-ext_loss-int_loss)),
                stationary_residual=float(np.max(np.abs(pi@q))))


def simulate(p, seed, warmup, duration):
    """Physical event simulation; each customer keeps its original arrival time.
    Failed retries are actual events. Uniform orbit selection realizes r*nu.
    Keep external input on while completing the observation-window cohort.
    """
    rng = random.Random(seed)
    q1, q2, orbit = deque(), deque(), []
    now = 0.; end = warmup+duration
    next_id = 0; arrivals = successes = losses = pending = 0
    total_delay = total_exit = 0.; occupation = departures = 0.
    # Job is (unique ID, original arrival time, cohort membership).
    def finish(job, success):
        nonlocal pending, successes, losses, total_delay, total_exit
        if job[2]:
            pending -= 1
            total_exit += now-job[1]
            if success:
                successes += 1; total_delay += now-job[1]
            else: losses += 1
    while now < end or pending:
        r0 = p.lam
        r1 = p.mu1 if q1 else 0.
        r2 = p.mu2 if q2 else 0.
        rr = p.nu*len(orbit)
        rate = r0+r1+r2+rr
        future = now+rng.expovariate(rate)
        occupation += max(0.,min(future,end)-max(now,warmup))*(len(q1)+len(q2)+len(orbit))
        # Do not execute an event beyond the end if no cohort job remains.
        if future >= end and pending == 0:
            now = end; break
        now = future; choice = rng.random()*rate
        if choice < r0:
            tracked = warmup <= now < end
            job = (next_id,now,tracked); next_id += 1
            if tracked: arrivals += 1; pending += 1
            if len(q1) < p.c1: q1.append(job)
            elif len(orbit) < p.k: orbit.append(job)
            else: finish(job,False)
        elif choice < r0+r1:
            job = q1.popleft()
            if len(q2) < p.c2: q2.append(job)
            elif len(orbit) < p.k: orbit.append(job)
            else: finish(job,False)
        elif choice < r0+r1+r2:
            job = q2.popleft()
            if warmup <= now < end: departures += 1
            finish(job,True)
        else:
            pos = rng.randrange(len(orbit))
            if len(q1) < p.c1:
                job = orbit[pos]; orbit[pos] = orbit[-1]; orbit.pop()
                q1.append(job)
        assert len(q1)<=p.c1 and len(q2)<=p.c2 and len(orbit)<=p.k
    assert arrivals == successes+losses and pending == 0
    assert successes > 0 and arrivals > 0
    return dict(loss=losses/arrivals, delay_success=total_delay/successes,
                throughput=departures/duration,mean_n=occupation/duration,
                time_until_exit=total_exit/arrivals,
                arrivals=arrivals, successes=successes, losses=losses,
                seed=seed, cohort_followup=max(0.,now-end))


def summarize(runs, exact, family_size):
    ans = {}
    for metric in ('loss','delay_success','throughput','mean_n','time_until_exit'):
        values = np.array([r[metric] for r in runs]); m = len(values)
        mean = float(values.mean()); se = float(values.std(ddof=1)/np.sqrt(m))
        half = float(student_t.ppf(.975,m-1)*se)
        simultaneous = float(student_t.ppf(1-.05/(2*family_size),m-1)*se)
        ans[metric] = dict(exact=exact[metric], estimate=mean, se=se,
                           ci95=[mean-half,mean+half],
                           family_ci95=[mean-simultaneous,mean+simultaneous],
                           covered95=bool(abs(mean-exact[metric])<=half),
                           covered_family=bool(abs(mean-exact[metric])<=simultaneous),
                           relative_error_percent=100*(mean-exact[metric])/exact[metric])
    return ans


SCENARIO_LABELS = {
    'light': 'Малая нагрузка',
    'busy': 'Повышенная нагрузка',
    'slow_retrial': 'Редкие повторные попытки',
}
METRIC_LABELS = {
    'loss': 'Вероятность потери',
    'delay_success': 'Задержка успешных заявок',
    'throughput': 'Пропускная способность',
    'mean_n': 'Среднее число заявок',
    'time_until_exit': 'Время до любого исхода',
}


def scenario_table(name, data):
    """Aligned Markdown also reads as a plain-text table in a terminal."""
    p = data['params']
    headers = ['Показатель', 'Аналитика', 'Имитация', '95% ДИ', 'Ошибка, %', 'В ДИ']
    rows = []
    for metric, label in METRIC_LABELS.items():
        value = data['summary'][metric]
        low, high = value['ci95']
        rows.append([
            label, f"{value['exact']:.6f}", f"{value['estimate']:.6f}",
            f'[{low:.6f}; {high:.6f}]',
            f"{value['relative_error_percent']:+.3f}",
            'Да' if value['covered95'] else 'Нет',
        ])
    widths = [max(len(row[i]) for row in [headers]+rows) for i in range(len(headers))]

    def line(row):
        return '| ' + ' | '.join(
            cell.ljust(widths[i]) if i == 0 else cell.rjust(widths[i])
            for i, cell in enumerate(row)
        ) + ' |'

    title = SCENARIO_LABELS.get(name, name)
    text = [f'## {title}', '',
            f"λ={p['lam']:g}; μ₁={p['mu1']:g}; μ₂={p['mu2']:g}; "
            f"ν={p['nu']:g}; C₁={p['c1']}; C₂={p['c2']}; K={p['k']}", '',
            line(headers),
            '| ' + ' | '.join('-'*w for w in widths) + ' |']
    text.extend(line(row) for row in rows)
    runs = data['runs']
    text += ['',
             f"Заявок: {sum(r['arrivals'] for r in runs):,}; "
             f"успешных: {sum(r['successes'] for r in runs):,}; "
             f"потерянных: {sum(r['losses'] for r in runs):,}.".replace(',', ' ')]
    return '\n'.join(text)


def report_header(settings):
    return (
        '# Сравнение аналитики и имитации\n\n'
        f"Прогонов на сценарий: {settings['reps']}; "
        f"прогрев: {settings['warmup']:g}; "
        f"окно наблюдения: {settings['duration']:g}.\n\n"
        'ДИ — индивидуальный приближённый доверительный интервал. '
        '«В ДИ» показывает, попало ли аналитическое значение в интервал.\n\n'
        'Ошибка, % = 100 × (имитация − аналитика) / аналитика. '
        'Потери указаны как вероятность от 0 до 1; время — в условных единицах. '
        'Числа округлены для отображения; проверки используют полную точность.\n\n'
        'Выход за ДИ сам по себе не доказывает ошибку программы.'
    )


def self_tests():
    # K=0: direct tandem without orbit; exact closed form at all rates=1.
    p = Params(1.,1.,1.,1.,1,1,0)
    a = analytical(p)
    # pi=(2,2,3,1)/8 in ordering (0,0),(0,1),(1,0),(1,1).
    assert abs(a['loss']-5/8)<1e-12
    assert abs(a['delay_success']-13/6)<1e-12
    assert abs(a['time_until_exit']-7/8)<1e-12
    # Fast second node approaches the M/M/1/1 blocking probability 1/2.
    a = analytical(Params(1.,1.,1e6,1.,1,1,0))
    assert abs(a['loss']-.5)<1e-6
    # Low load: empty queues, no losses, delay tends to 1/mu1+1/mu2.
    a = analytical(Params(1e-7,2.,3.,1.,2,2,2))
    assert abs(a['delay_success']-(1/2+1/3))<1e-6


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reps',type=int,default=24)
    parser.add_argument('--duration',type=float,default=50000.)
    parser.add_argument('--warmup',type=float,default=5000.)
    parser.add_argument('--seed',type=int,default=20261025)
    parser.add_argument('--output',type=Path,default=Path('.'))
    args = parser.parse_args()
    if args.reps<2 or args.duration<=0 or args.warmup<0: parser.error('invalid run length/reps')
    self_tests()
    scenarios = {
        'light': Params(.6,1.5,1.2,.8,2,2,3),
        'busy': Params(1.4,1.5,1.2,.8,2,2,3),
        'slow_retrial': Params(1.4,1.5,1.2,.15,2,2,3),
    }
    results = dict(settings=vars(args)|{'output':str(args.output)},
                   versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
                   self_tests='passed',scenarios={})
    sections = [report_header(results['settings'])]
    print(sections[0], flush=True)
    for j,(name,p) in enumerate(scenarios.items()):
        exact = analytical(p)
        runs = [simulate(p,args.seed+100000*j+i,args.warmup,args.duration)
                for i in range(args.reps)]
        summary = summarize(runs,exact,5*len(scenarios))
        results['scenarios'][name] = dict(params=asdict(p),analytical=exact,runs=runs,summary=summary)
        table = scenario_table(name, results['scenarios'][name])
        sections.append(table)
        print('\n'+table, flush=True)
    covered = sum(v['covered_family'] for s in results['scenarios'].values()
                  for v in s['summary'].values())
    total = sum(len(s['summary']) for s in results['scenarios'].values())
    footer = (f'Покрытие интервалами с поправкой Бонферрони: {covered}/{total}.\n\n'
              'Встроенные проверки и матричные тождества: выполнены.')
    sections.append(footer)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(
        json.dumps(results,indent=2,ensure_ascii=False)+'\n', encoding='utf-8')
    (args.output/'results.md').write_text('\n\n'.join(sections)+'\n', encoding='utf-8')
    print('\n'+footer)
    print('\nТаблицы:',args.output/'results.md')
    print('Подробные данные:',args.output/'results.json')

if __name__ == '__main__': main()
