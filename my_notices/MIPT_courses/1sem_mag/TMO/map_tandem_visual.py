#!/usr/bin/env python3
"""MAP/M/1/K1 -> M/1/K2 with a shared finite orbit.

Two independent methods:
  1) CTMC + tagged customer (matrix formulas, no randomness);
  2) event-driven Monte Carlo simulation (random arrivals/services/retrials).

Exports PNG figures, CSVs and JSON.  All times are in model time units.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve
from scipy.sparse.linalg import expm_multiply
from scipy.stats import t as student_t


@dataclass(frozen=True)
class Parameters:
    D0: np.ndarray
    D1: np.ndarray
    K1: int = 2
    K2: int = 2
    R: int = 2
    mu1: float = 1.8
    mu2: float = 1.35
    nu: float = 0.9

    def __post_init__(self):
        m = self.D0.shape[0]
        if self.D0.shape != (m, m) or self.D1.shape != (m, m):
            raise ValueError("D0 and D1 must be square matrices of equal size")
        if np.max(np.abs((self.D0 + self.D1).sum(axis=1))) > 1e-10:
            raise ValueError("Rows of D0 + D1 must sum to zero")
        if np.min(self.D1) < -1e-12 or np.min(self.D0 - np.diag(np.diag(self.D0))) < -1e-12:
            raise ValueError("MAP transition intensities must be nonnegative")
        if min(self.K1, self.K2) < 1 or self.R < 0:
            raise ValueError("K1,K2 >= 1 and R >= 0 required")
        if min(self.mu1, self.mu2, self.nu) <= 0:
            raise ValueError("All rates must be positive")


def stationary(G):
    M = G.T.copy()
    M[-1, :] = 1.0
    rhs = np.zeros(G.shape[0]); rhs[-1] = 1.0
    x = solve(M, rhs, assume_a="gen")
    if max(abs(x @ G)) > 1e-8 or min(x) < -1e-9:
        raise ArithmeticError("Invalid stationary distribution")
    return np.clip(x, 0, None) / x.sum()


class AnalyticalModel:
    def __init__(self, p: Parameters):
        self.p = p
        self.m = p.D0.shape[0]
        self.zstates = [(a,b,r) for a in range(p.K1+1)
                        for b in range(p.K2+1) for r in range(p.R+1)]
        self.N = len(self.zstates)
        self.zidx = {z:i for i,z in enumerate(self.zstates)}
        self.states = [(v,a,b,r) for v in range(self.m) for a,b,r in self.zstates]
        self.n = len(self.states)
        self.index = {s:i for i,s in enumerate(self.states)}
        self._build()

    def _build(self):
        p, N, m = self.p, self.N, self.m
        PA = np.zeros((N,N))
        B = np.zeros((N,N))
        H1 = np.zeros((self.n,self.n))
        H2 = np.zeros_like(H1)
        self.loss0_vec = np.zeros(self.n)
        self.loss12_vec = np.zeros(self.n)
        def add_B(z, dst, rate):
            i,j = self.zidx[z],self.zidx[dst]
            if i!=j:
                B[i,j] += rate
                B[i,i] -= rate
        for z in self.zstates:
            a,b,r=z
            target=(a+1,b,r) if a<p.K1 else ((a,b,r+1) if r<p.R else z)
            PA[self.zidx[z],self.zidx[target]]=1
            if a>0:
                dst=(a-1,b+1,r) if b<p.K2 else ((a-1,b,r+1) if r<p.R else (a-1,b,r))
                add_B(z,dst,p.mu1)
                for v in range(m):
                    H1[v*N+self.zidx[z],v*N+self.zidx[dst]]=p.mu1
            if b>0:
                dst=(a,b-1,r)
                add_B(z,dst,p.mu2)
                for v in range(m):
                    H2[v*N+self.zidx[z],v*N+self.zidx[dst]]=p.mu2
            if r>0 and a<p.K1:
                add_B(z,(a+1,b,r-1),r*p.nu)
        self.PA,self.B,self.H1,self.H2=PA,B,H1,H2
        self.Q=np.kron(p.D0,np.eye(N))+np.kron(p.D1,PA)+np.kron(np.eye(m),B)
        if np.max(abs(self.Q.sum(axis=1)))>1e-9:
            raise ArithmeticError("Q rows do not sum to zero")
        if np.min(self.Q - np.diag(np.diag(self.Q))) < -1e-9:
            raise ArithmeticError("Q has negative off-diagonal rates")
        for i,(v,a,b,r) in enumerate(self.states):
            if a==p.K1 and r==p.R:
                self.loss0_vec[i]=p.D1[v,:].sum()
            if a>0 and b==p.K2 and r==p.R:
                self.loss12_vec[i]=p.mu1
        self.pi=stationary(self.Q)
        theta=stationary(p.D0+p.D1)
        self.lam=float(theta @ p.D1 @ np.ones(m))
        self.lam1=float(self.pi @ H1 @ np.ones(self.n))
        self.lam2=float(self.pi @ H2 @ np.ones(self.n))
        self.loss0=float(self.pi @ self.loss0_vec)
        self.loss12=float(self.pi @ self.loss12_vec)
        self.p_loss0=self.loss0/self.lam
        self.p_loss12=self.loss12/self.lam
        self.p_loss=self.p_loss0+self.p_loss12
        self.p_success=self.lam2/self.lam
        self.L=float(sum(self.pi[i]*(a+b+r) for i,(_,a,b,r) in enumerate(self.states)))
        self.mean_all=self.L/self.lam
        assert abs(self.lam-self.lam2-self.loss0-self.loss12)<1e-8
        self.marginals={k:np.array([sum(self.pi[i] for i,s in enumerate(self.states) if s[pos]==j)
                                  for j in range(cap+1)])
                        for k,pos,cap in [('Узел 1',1,p.K1),('Узел 2',2,p.K2),('Орбита',3,p.R)]}

    def tagged_delay(self):
        p,m=self.p,self.m
        tagged=[]
        for v,a,b,r in self.states:
            tagged.extend((v,a,b,r,1,pos) for pos in range(1,a+1))
            tagged.extend((v,a,b,r,2,pos) for pos in range(1,b+1))
            if r>0: tagged.append((v,a,b,r,3,0))
        tidx={s:i for i,s in enumerate(tagged)}
        nt=len(tagged)
        A=np.zeros((nt,nt)); g=np.zeros(nt); lost=np.zeros(nt)
        def jump(i,s,rate):
            j=tidx[s]
            if i!=j and rate>0: A[i,j]+=rate
        for i,(v,a,b,r,side,pos) in enumerate(tagged):
            for w in range(m):
                if w!=v and p.D0[v,w]>0:
                    jump(i,(w,a,b,r,side,pos),p.D0[v,w])
                rate=p.D1[v,w]
                if rate<=0: continue
                dest=(w,a+1,b,r,side,pos) if a<p.K1 else (
                    (w,a,b,r+1,side,pos) if r<p.R else (w,a,b,r,side,pos))
                jump(i,dest,rate)
            if a>0:
                if side==1 and pos==1:
                    if b<p.K2: dst=(v,a-1,b+1,r,2,b+1)
                    elif r<p.R: dst=(v,a-1,b,r+1,3,0)
                    else: dst=None; lost[i]+=p.mu1
                else:
                    newpos=pos-int(side==1)
                    if b<p.K2: dst=(v,a-1,b+1,r,side,newpos)
                    elif r<p.R: dst=(v,a-1,b,r+1,side,newpos)
                    else: dst=(v,a-1,b,r,side,newpos)
                if dst is not None: jump(i,dst,p.mu1)
            if b>0:
                if side==2 and pos==1: g[i]+=p.mu2
                else: jump(i,(v,a,b-1,r,side,pos-int(side==2)),p.mu2)
            if r>0 and a<p.K1:
                if side==3:
                    jump(i,(v,a+1,b,r-1,1,a+1),p.nu)
                    if r>1: jump(i,(v,a+1,b,r-1,3,0),(r-1)*p.nu)
                else:
                    jump(i,(v,a+1,b,r-1,side,pos),r*p.nu)
        for i in range(nt): A[i,i]=-A[i,:].sum()-g[i]-lost[i]
        assert np.max(abs(A.sum(axis=1)+g+lost))<1e-9
        gamma=np.zeros(nt)
        for i,(v,a,b,r) in enumerate(self.states):
            for w in range(m):
                weight=self.pi[i]*p.D1[v,w]/self.lam
                if weight==0: continue
                if a<p.K1: target=(w,a+1,b,r,1,a+1)
                elif r<p.R: target=(w,a,b,r+1,3,0)
                else: continue  # immediate loss: zero sojourn time
                gamma[tidx[target]]+=weight
        h=solve(-A,g)
        u=solve(-A,h)
        self.tag_count=nt
        self.mean_success=float((gamma@u)/(gamma@h))
        self.tag_success=float(gamma@h)
        self.tag_all=float(gamma@solve(-A,np.ones(nt)))
        assert abs(self.tag_success-self.p_success)<1e-8
        assert abs(self.tag_all-self.mean_all)<1e-8
        return self.mean_success

    def inter_departures(self,time_grid):
        H1,Q=self.H1,self.Q
        alpha=self.pi@H1/self.lam1
        Z=H1-Q
        one=np.ones(self.n)
        vec=solve(Z,one)
        self.mean_delta=float(alpha@vec)
        second=float(2*alpha@solve(Z,vec))
        cross=float(alpha@solve(Z,solve(Z,H1@vec)))
        self.corr_delta=float((cross-self.mean_delta**2)/(second-self.mean_delta**2))
        assert abs(self.mean_delta-1/self.lam1)<1e-8
        # expm_multiply for row vector alpha exp((Q-H1)t), via transpose.
        evolved=expm_multiply((Q-H1).T,alpha,start=float(time_grid[0]),stop=float(time_grid[-1]),num=len(time_grid),endpoint=True)
        cdf=1-evolved.sum(axis=1)
        self.cdf=np.clip(cdf,0,1)
        return self.cdf


def simulate(p:Parameters,warmup:int,arrivals:int,seed:int,trajectory_window:float=24.0):
    """Independent event-driven simulation; MAP events include arrivals with same phase."""
    rng=np.random.default_rng(seed)
    m=p.D0.shape[0]
    phase=0
    q1,q2=deque(),deque()
    orbit=[]
    # event tuples: (code, new phase, intensity), where 0=phase-only and 1=arrival.
    phase_events=[]
    for v in range(m):
        row=[]
        row.extend((0,w,float(p.D0[v,w])) for w in range(m) if w!=v and p.D0[v,w]>0)
        row.extend((1,w,float(p.D1[v,w])) for w in range(m) if p.D1[v,w]>0)
        phase_events.append(row)
    phase_rates=[sum(e[2] for e in row) for row in phase_events]

    t=0.0; n_arrived=0; resolved=0; next_id=0
    start=None; end=None
    births={}
    succ_delays=[]; all_delays=[]
    loss0=0; loss12=0; successes=0
    q1_exit=[]; last_q1_exit=None
    durations=np.zeros((m,p.K1+1,p.K2+1,p.R+1),dtype=float)
    trace_t=[0.0]; trace_counts=[(0,0,0)]
    event_log=[]

    def finish(cid,kind,now):
        nonlocal resolved,loss0,loss12,successes
        if cid not in births: return
        sojourn=now-births.pop(cid)
        resolved+=1
        all_delays.append(sojourn)
        if kind=='success':
            successes+=1; succ_delays.append(sojourn)
        elif kind=='loss0': loss0+=1
        elif kind=='loss12': loss12+=1
        else: raise RuntimeError(kind)

    while end is None or resolved<arrivals:
        if phase_rates[phase]+(p.mu1 if q1 else 0)+(p.mu2 if q2 else 0)+len(orbit)*p.nu<=0:
            raise ArithmeticError("Absorbing simulator state")
        total=phase_rates[phase]+(p.mu1 if q1 else 0)+(p.mu2 if q2 else 0)+len(orbit)*p.nu
        dt=float(rng.exponential(1/total))
        if start is not None and end is None:
            durations[phase,len(q1),len(q2),len(orbit)]+=dt
        t+=dt
        x=float(rng.random()*total)
        kind=None; target=None
        for code,w,rate in phase_events[phase]:
            if x<rate:
                kind=code; target=w; break
            x-=rate
        if kind is None:
            r1=p.mu1 if q1 else 0
            r2=p.mu2 if q2 else 0
            if x<r1: kind=2
            elif x<r1+r2: kind=3
            else: kind=4

        before=(phase,len(q1),len(q2),len(orbit))
        if kind==0:
            phase=target
            event_name='MAP: смена фазы без заявки'
        elif kind==1:
            phase=target
            n_arrived+=1; next_id+=1
            cid=next_id
            if warmup<n_arrived<=warmup+arrivals:
                births[cid]=t
            if len(q1)<p.K1:
                q1.append(cid); event_name='Внешняя заявка -> узел 1'
            elif len(orbit)<p.R:
                orbit.append(cid); event_name='Внешняя заявка -> орбита'
            else:
                finish(cid,'loss0',t); event_name='Внешняя заявка -> потеря'
        elif kind==2:
            cid=q1.popleft()
            if start is not None and end is None:
                if last_q1_exit is not None: q1_exit.append(t-last_q1_exit)
                last_q1_exit=t
            if len(q2)<p.K2:
                q2.append(cid); event_name='Узел 1 -> узел 2'
            elif len(orbit)<p.R:
                orbit.append(cid); event_name='Узел 1 -> орбита'
            else:
                finish(cid,'loss12',t); event_name='Узел 1 -> потеря'
        elif kind==3:
            cid=q2.popleft(); finish(cid,'success',t)
            event_name='Узел 2 -> выход'
        elif kind==4:
            if len(q1)<p.K1:
                k=int(rng.integers(len(orbit)))
                cid=orbit.pop(k)
                q1.append(cid)
                event_name='Повторная попытка: успешно -> узел 1'
            else:
                event_name='Повторная попытка: неудачно'
            # unsuccessful attempt leaves orbit and first node unchanged
        else: raise RuntimeError(f"Unexpected kind {kind}")

        if start is None and n_arrived>=warmup:
            start=t
            trace_t=[0.0]
            trace_counts=[(len(q1),len(q2),len(orbit))]
        if start is not None and end is None:
            if len(event_log)<120:
                after=(phase,len(q1),len(q2),len(orbit))
                event_log.append((float(t-start),event_name,before[0]+1,after[0]+1,*before[1:],*after[1:]))
            if t-start<=trajectory_window:
                trace_t.append(t-start)
                trace_counts.append((len(q1),len(q2),len(orbit)))
            if n_arrived>=warmup+arrivals:
                end=t
    if resolved!=arrivals or births:
        raise ArithmeticError("Simulation cohort not fully resolved")
    duration=float(durations.sum())
    station=durations.reshape(-1)/duration
    marginals={k:durations.sum(axis=tuple(j for j in range(4) if j!=axis))/duration
               for k,axis in [('Узел 1',1),('Узел 2',2),('Орбита',3)]}
    intervals=np.asarray(q1_exit,dtype=float)
    mean_all=float(np.mean(all_delays)); mean_success=float(np.mean(succ_delays))
    n=len(intervals)
    corr=float(np.corrcoef(intervals[:-1],intervals[1:])[0,1]) if n>2 else float('nan')
    return {
        'loss0':loss0/arrivals,
        'loss12':loss12/arrivals,
        'p_loss':(loss0+loss12)/arrivals,
        'p_success':successes/arrivals,
        'mean_all':mean_all,
        'mean_success':mean_success,
        'mean_delta':float(np.mean(intervals)),
        'corr_delta':corr,
        'marginals':marginals,
        'station':station,
        'duration':duration,
        'intervals':intervals,
        'trace_t':np.array(trace_t),
        'trace_counts':np.array(trace_counts),
        'event_log':event_log,
        'events_observed':int(n),
        'arrivals_observed':int(arrivals),
        'lost_observed':int(loss0+loss12),
        'successes_observed':int(successes),
    }


def mean_ci(values):
    arr=np.asarray(values,dtype=float)
    av=float(np.mean(arr))
    if len(arr)<2: return av,float('nan'),float('nan')
    err=float(student_t.ppf(.975,len(arr)-1)*np.std(arr,ddof=1)/np.sqrt(len(arr)))
    return av,av-err,av+err


def save_csv(path,headers,rows):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f)
        w.writerow(headers); w.writerows(rows)


def create_figures(output,calc,sim_results,grid,cdf):
    figdir=output/'figures'; figdir.mkdir(exist_ok=True,parents=True)
    plt.rcParams.update({'font.size':10,'axes.titlesize':12,'figure.dpi':120,'savefig.dpi':155})
    # 1. Sample path of occupancies.
    f,ax=plt.subplots(figsize=(11,4))
    trace=sim_results[0]
    for i,label in enumerate(['Узел 1','Узел 2','Орбита']):
        ax.step(trace['trace_t'],trace['trace_counts'][:,i],where='post',label=label,linewidth=1.6)
    ax.set(xlabel='Время после прогрева',ylabel='Число заявок',title='Пример случайной траектории системы')
    ax.legend();ax.grid(alpha=.25);ax.set_ylim(bottom=-.15)
    f.tight_layout();f.savefig(figdir/'01_trajectory.png');plt.close(f)

    # 2. Marginal occupancy comparisons by components.
    f,axes=plt.subplots(1,3,figsize=(12,3.9),sharey=True)
    for ax,key in zip(axes,['Узел 1','Узел 2','Орбита']):
        formula=calc.marginals[key]
        empirical=np.mean([x['marginals'][key] for x in sim_results],axis=0)
        t=np.arange(len(formula)); width=.38
        ax.bar(t-width/2,formula,width,label='Формулы')
        ax.bar(t+width/2,empirical,width,label='Имитация')
        ax.set(title=key,xlabel='Количество заявок',xticks=t,ylim=(0,1))
        ax.grid(axis='y',alpha=.2)
    axes[0].set_ylabel('Стационарная вероятность')
    axes[-1].legend(loc='upper right',fontsize=9)
    f.suptitle('Заполнение системы: формулы и имитация')
    f.tight_layout();f.savefig(figdir/'02_occupancy.png');plt.close(f)

    # 3. Loss probabilities with 95% CI across replications.
    labels=['При входе','После узла 1','Всего']
    keys=['loss0','loss12','p_loss']
    exact=[calc.p_loss0,calc.p_loss12,calc.p_loss]
    avgs=[mean_ci([r[k] for r in sim_results]) for k in keys]
    f,ax=plt.subplots(figsize=(9,4))
    xx=np.arange(3);wd=.35
    ax.bar(xx-wd/2,exact,wd,label='Формулы')
    ax.bar(xx+wd/2,[a[0] for a in avgs],wd,label='Имитация')
    if len(sim_results)>1:
        ax.errorbar(xx+wd/2,[a[0] for a in avgs],
                    yerr=[a[2]-a[0] for a in avgs],fmt='none',capsize=4,color='black',label='95% ДИ (по прогонам)')
    ax.set_xticks(xx,labels);ax.set(ylabel='Доля внешних заявок',title='Вероятность окончательной потери')
    ax.legend();ax.grid(axis='y',alpha=.2)
    f.tight_layout();f.savefig(figdir/'03_losses.png');plt.close(f)

    # 4. Delay comparison.
    labels=['До любого исхода','До успеха']
    exact=[calc.mean_all,calc.mean_success]
    avgs=[mean_ci([r[k] for r in sim_results]) for k in ['mean_all','mean_success']]
    f,ax=plt.subplots(figsize=(9,4))
    xx=np.arange(2);wd=.35
    ax.bar(xx-wd/2,exact,wd,label='Формулы')
    ax.bar(xx+wd/2,[a[0] for a in avgs],wd,label='Имитация')
    if len(sim_results)>1:
        ax.errorbar(xx+wd/2,[a[0] for a in avgs],
                    yerr=[a[2]-a[0] for a in avgs],fmt='none',capsize=4,color='black')
    ax.set_xticks(xx,labels);ax.set(ylabel='Единицы времени',title='Средняя межконцевая задержка')
    ax.legend();ax.grid(axis='y',alpha=.2)
    f.tight_layout();f.savefig(figdir/'04_delays.png');plt.close(f)

    # 5. Inter-departure CDF: matrix formula, empirical, Poisson same rate.
    intervals=np.concatenate([r['intervals'] for r in sim_results])
    emp=np.searchsorted(np.sort(intervals),grid,side='right')/len(intervals)
    poisson=1-np.exp(-calc.lam1*grid)
    f,ax=plt.subplots(figsize=(10,4.4))
    ax.plot(grid,cdf,label='Матричная формула F(t)',linewidth=2)
    ax.plot(grid,emp,label='Имитация (эмпирическая F(t))',linestyle='--',linewidth=2)
    ax.plot(grid,poisson,label='Экспоненциальная F(t) при той же λвыход',linestyle=':',linewidth=1.8)
    ax.set(xlabel='Интервал t',ylabel='F(t)',title='Интервалы между выходами первого узла',ylim=(0,1.01))
    ax.legend();ax.grid(alpha=.25)
    f.tight_layout();f.savefig(figdir/'05_interdeparture_cdf.png');plt.close(f)

    # 5b. Zoom of deviations from a memoryless exponential reference.
    f,ax=plt.subplots(figsize=(10,4))
    ax.plot(grid,cdf-poisson,label='Матричная F(t) минус экспоненциальная',linewidth=2)
    ax.plot(grid,emp-poisson,label='Имитация F(t) минус экспоненциальная',linestyle='--',linewidth=1.8)
    ax.axhline(0,linewidth=1,alpha=.5,color='gray')
    ax.set(xlabel='Интервал t',ylabel='Разность функций распределения',
           title='Насколько распределение интервалов отличается от экспоненциального')
    ax.grid(alpha=.25);ax.legend()
    f.tight_layout();f.savefig(figdir/'05b_interdeparture_difference.png');plt.close(f)

    # 6. Q matrix structure; nonnegative rates only (diagonal omitted).
    Q=calc.Q
    plotted=np.where(np.eye(Q.shape[0],dtype=bool),0,np.maximum(Q,0))
    f,ax=plt.subplots(figsize=(7,6))
    display=np.ma.masked_where(plotted<=1e-13,plotted)
    im=ax.imshow(display,interpolation='nearest',cmap='viridis',aspect='auto')
    f.colorbar(im,ax=ax,label='Интенсивность перехода')
    ax.set(xlabel='Новое состояние j',ylabel='Исходное состояние i',title=f'Ненулевые переходы Q ({Q.shape[0]} состояний)')
    f.tight_layout();f.savefig(figdir/'06_Q_transitions.png');plt.close(f)
    return emp


def orbit_sweep(p,maximum,output):
    result=[]
    for R in range(maximum+1):
        params=Parameters(p.D0,p.D1,p.K1,p.K2,R,p.mu1,p.mu2,p.nu)
        a=AnalyticalModel(params)
        a.tagged_delay()
        result.append((R,a.p_loss,a.mean_success,a.p_success))
    save_csv(output/'orbit_sweep.csv',['R','P_loss_exact','E_delay_success_exact','P_success_exact'],result)
    rr=np.asarray(result)
    f,ax=plt.subplots(figsize=(9,4.2))
    ax.plot(rr[:,0],rr[:,1],marker='o',label='P(потери)')
    ax.set(xlabel='Вместимость орбиты R',ylabel='Вероятность потери',title='Эффект увеличения орбиты (точный расчёт)')
    ax.grid(alpha=.25)
    f.tight_layout();f.savefig(output/'figures'/'07_orbit_loss.png');plt.close(f)
    f,ax=plt.subplots(figsize=(9,4.2))
    ax.plot(rr[:,0],rr[:,2],marker='o',label='E[T | успех]')
    ax.set(xlabel='Вместимость орбиты R',ylabel='Средняя задержка',title='Орбита и задержка успешных заявок (точный расчёт)')
    ax.grid(alpha=.25)
    f.tight_layout();f.savefig(output/'figures'/'08_orbit_delay.png');plt.close(f)
    return result


def main():
    ap=argparse.ArgumentParser(description='Аналитический и имитационный расчёт двухузловой СМО с конечной орбитой')
    ap.add_argument('--arrivals',type=int,default=40000,help='внешних заявок в наблюдаемой когорте каждого прогона')
    ap.add_argument('--warmup',type=int,default=5000,help='внешних заявок прогрева перед измерениями')
    ap.add_argument('--replications',type=int,default=8,help='число независимых имитационных прогонов')
    ap.add_argument('--seed',type=int,default=20261118)
    ap.add_argument('--sweep-max',type=int,default=5,help='максимальная вместимость орбиты в аналитическом сравнении')
    ap.add_argument('--no-sweep',action='store_true',help='не строить графики зависимости от размера орбиты')
    ap.add_argument('--output',default='tmo_visual_results',help='каталог результатов')
    args=ap.parse_args()
    if args.arrivals<100 or args.warmup<0 or args.replications<1 or args.sweep_max<0:
        ap.error('Неверные значения параметров прогонов')
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    p=Parameters(np.array([[-.80,.35],[.55,-2.85]],float),
                 np.array([[.45,0],[0,2.30]],float),
                 K1=2,K2=2,R=2,mu1=1.8,mu2=1.35,nu=.9)
    print('1/4: Решение стационарной цепи Q и помеченной цепи A...',flush=True)
    a=AnalyticalModel(p)
    a.tagged_delay()
    grid=np.linspace(0,5,151)
    cdf=a.inter_departures(grid)
    print(f'  Q: {a.n} состояния; помеченная цепь A: {a.tag_count} состояния',flush=True)
    print('2/4: Имитация независимых траекторий...',flush=True)
    sims=[]
    for i in range(args.replications):
        r=simulate(p,args.warmup,args.arrivals,args.seed+i)
        sims.append(r)
        print(f"  прогон {i+1}/{args.replications}: потери={r['p_loss']:.5f}, "
              f"задержка={r['mean_success']:.5f}, выборка выходов={r['events_observed']}",flush=True)
    print('3/4: Графики и таблицы...',flush=True)
    emp=create_figures(out,a,sims,grid,cdf)
    formula={
        'loss0':a.p_loss0,'loss12':a.p_loss12,'p_loss':a.p_loss,
        'p_success':a.p_success,'mean_all':a.mean_all,'mean_success':a.mean_success,
        'mean_delta':a.mean_delta,'corr_delta':a.corr_delta,
    }
    labels={'loss0':'Потеря при внешнем поступлении',
            'loss12':'Потеря после узла 1',
            'p_loss':'Полная вероятность потери',
            'p_success':'Вероятность успеха',
            'mean_all':'E[T] все поступления',
            'mean_success':'E[T | успех]',
            'mean_delta':'E[Δ] выходов узла 1',
            'corr_delta':'Corr(Δn, Δn+1)'}
    comparison=[]
    for key,exact in formula.items():
        avg,lo,hi=mean_ci([s[key] for s in sims])
        comparison.append([labels[key],key,f'{exact:.8f}',f'{avg:.8f}',
                           f'{lo:.8f}',f'{hi:.8f}',f'{avg-exact:+.8f}'])
    save_csv(out/'comparison.csv',
             ['Характеристика','key','Формулы','Имитация','ДИ 95% нижняя','ДИ 95% верхняя','Ошибка (имитация-формула)'],comparison)
    save_csv(out/'cdf_interdeparture.csv',
             ['t','F_exact','F_simulation','F_exponential_reference'],
             zip(grid,cdf,emp,1-np.exp(-a.lam1*grid)))
    est_station=np.mean([s['station'] for s in sims],axis=0)
    save_csv(out/'stationary_states.csv',
             ['MAP phase 1-based','N1','N2','Orbit','pi_exact','pi_simulation'],
             [[v+1,n1,n2,r,f'{a.pi[i]:.9f}',f'{est_station[i]:.9f}']
              for i,(v,n1,n2,r) in enumerate(a.states)])
    sample=sims[0]
    save_csv(out/'events.csv',
             ['t','Событие','MAP до','MAP после','N1 до','N2 до','Орбита до','N1 после','N2 после','Орбита после'],
             sample['event_log'])
    save_csv(out/'sample_path.csv',['t','N1','N2','Orbit'],
             [[float(t),int(c[0]),int(c[1]),int(c[2])]
              for t,c in zip(sample['trace_t'],sample['trace_counts'])])
    sweep=None
    if not args.no_sweep:
        print('4/4: Аналитическое изменение размера орбиты...',flush=True)
        sweep=orbit_sweep(p,args.sweep_max,out)
    else:
        print('4/4: Готово (вариация орбиты отключена).',flush=True)
    report={
        'parameters':{'D0':p.D0.tolist(),'D1':p.D1.tolist(),
                      'K1':p.K1,'K2':p.K2,'R':p.R,'mu1':p.mu1,'mu2':p.mu2,'nu':p.nu},
        'simulation':{'seed':args.seed,'replications':args.replications,
                      'warmup_external_arrivals_per_replication':args.warmup,
                      'measured_external_arrivals_per_replication':args.arrivals,
                      'notes':'Each observed external arrival is followed until success/loss; the rest of the system continues without interruption.'},
        'analytic':{**formula,'lambda_external':a.lam,'lambda_exit_1':a.lam1,
                    'lambda_exit_2':a.lam2,'L':a.L,'Q_size':a.n,'tagged_states':a.tag_count},
        'simulation_mean':{k:float(np.mean([s[k] for s in sims])) for k in formula},
        'sweep':sweep,
    }
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    description='''# MAP tandem queue: воспроизводимый расчёт и визуализация

Запуск из каталога с программой:

```bash
python -m pip install numpy scipy matplotlib
python map_tandem_visual.py
```

- `comparison.csv`: аналитика и статистика по независимым имитационным прогонам; доверительные интервалы рассчитаны по t-распределению по средним прогонов, а не по числу заявок.
- `stationary_states.csv`: стационарные вероятности всех состояний Q и оценки доли времени симуляции.
- `cdf_interdeparture.csv`: распределение между выходами первого узла: матричная формула, эмпирика, экспоненциальный ориентир.
- `sample_path.csv`: одна траектория численностей заявок.
- `events.csv`: первые 120 событий одного прогона, включая фазы MAP и состояния до/после события.
- `orbit_sweep.csv`: влияние R, расчёт только матричным методом.
- `figures/`: 7–9 графиков PNG.

## Аналитический расчёт

1. `Q = kron(D0,I) + kron(D1,PA) + kron(I,B)`.
2. `pi Q = 0`, `pi e = 1`.
3. `P_loss = (pi loss0 + pi loss12) / lambda`.
4. Помеченная заявка: `(-A)h=g`, `(-A)u=h`, `E[T|success]=(gamma u)/(gamma h)`.
5. Выход первого узла: `H1` — помеченные переходы; `F(t)=1-alpha exp((Q-H1)t)e`.

## Имитационный расчёт

Сначала генерируются MAP-события, окончания обслуживания и попытки из орбиты. Интервал до очередного события распределён экспоненциально с параметром, равным сумме всех активных интенсивностей. Тип события выбирается пропорционально его интенсивности. Каждая внешняя заявка наблюдаемой когорты отслеживается до успеха или безвозвратной потери. Для заполнения используются доли времени, для интервалов — разности последовательных моментов окончания обслуживания первого узла.

В случае неудачной попытки из орбиты состояние не меняется; такая попытка всё равно генерируется в имитации. MAP-событие типа D1 с неизменной фазой тоже генерирует заявку.

Доверительные интервалы отражают статистическую вариацию независимых прогонов; небольшое число прогонов даёт неточную оценку самого интервала.
'''
    (out/'README.md').write_text(description,encoding='utf-8')
    print('\nСравнение (формулы / имитация):')
    for row in comparison:
        print(f'{row[0]:40s} {row[2]:>12s} {row[3]:>12s} [95%: {row[4]}, {row[5]}]')
    print(f'\nФайлы: {out.resolve()}')

if __name__=='__main__':
    main()
