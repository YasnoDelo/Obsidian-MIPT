#!/usr/bin/env python3
"""Точный расчёт MAP/M/1/K1 -> M/1/K2 с общей конечной орбитой."""
import numpy as np
from scipy.linalg import expm, solve

# Единственный численный пример. Вместимость узлов включает прибор.
D0 = np.array([[-0.80, 0.35], [0.55, -2.85]], dtype=float)
D1 = np.array([[0.45, 0.0], [0.0, 2.30]], dtype=float)
K1, K2, R = 2, 2, 2
mu1, mu2, nu = 1.80, 1.35, 0.90
m = D0.shape[0]


def invariant(G):
    """Строка стационарных вероятностей конечной неприводимой цепи."""
    n = G.shape[0]
    M = G.T.copy()
    M[-1, :] = 1.0
    b = np.zeros(n)
    b[-1] = 1.0
    p = solve(M, b)
    assert np.max(np.abs(p @ G)) < 1e-9
    return p


# 1. Генератор Q = D0 ⊗ I + D1 ⊗ PA + I ⊗ B.
zstates = [(a, b, r) for a in range(K1 + 1)
           for b in range(K2 + 1) for r in range(R + 1)]
zidx = {z: i for i, z in enumerate(zstates)}
N = len(zstates)
PA = np.zeros((N, N))
B = np.zeros((N, N))
H1 = np.zeros((m * N, m * N))
H2 = np.zeros_like(H1)
loss0 = np.zeros(m * N)
loss12 = np.zeros(m * N)


def add_B(z, target, rate):
    i, j = zidx[z], zidx[target]
    if i != j:
        B[i, j] += rate
        B[i, i] -= rate


for z in zstates:
    a, b, r = z
    if a < K1:
        target = (a + 1, b, r)
    elif r < R:
        target = (a, b, r + 1)
    else:
        target = z  # внешний отказ, численности не меняются
    PA[zidx[z], zidx[target]] = 1.0

    if a > 0:
        if b < K2:
            dst = (a - 1, b + 1, r)
        elif r < R:
            dst = (a - 1, b, r + 1)
        else:
            dst = (a - 1, b, r)
        add_B(z, dst, mu1)
        for v in range(m):
            H1[v * N + zidx[z], v * N + zidx[dst]] = mu1
    if b > 0:
        dst = (a, b - 1, r)
        add_B(z, dst, mu2)
        for v in range(m):
            H2[v * N + zidx[z], v * N + zidx[dst]] = mu2
    if r > 0 and a < K1:
        add_B(z, (a + 1, b, r - 1), r * nu)

Q = np.kron(D0, np.eye(N)) + np.kron(D1, PA) + np.kron(np.eye(m), B)
assert np.max(np.abs(Q.sum(axis=1))) < 1e-11
assert np.min(Q - np.diag(np.diag(Q))) >= -1e-12
states = [(v, a, b, r) for v in range(m) for a, b, r in zstates]
index = {s: i for i, s in enumerate(states)}
for i, (v, a, b, r) in enumerate(states):
    if a == K1 and r == R:
        loss0[i] = D1[v, :].sum()
    if a > 0 and b == K2 and r == R:
        loss12[i] = mu1

pi = invariant(Q)
theta = invariant(D0 + D1)
lam = float(theta @ D1 @ np.ones(m))
lambda1 = float(pi @ H1 @ np.ones(m * N))
lambda2 = float(pi @ H2 @ np.ones(m * N))
lambda_loss0 = float(pi @ loss0)
lambda_loss12 = float(pi @ loss12)
p_loss = (lambda_loss0 + lambda_loss12) / lam
L = float(sum(pi[i] * (a + b + r) for i, (_, a, b, r) in enumerate(states)))
assert abs(lam - lambda2 - lambda_loss0 - lambda_loss12) < 1e-9
assert abs(p_loss - (1 - lambda2 / lam)) < 1e-9

# 2. Помеченная заявка: side = 1, 2 или 3 (орбита), pos = 1,2,... или 0.
tagged = []
for v, a, b, r in states:
    tagged.extend((v, a, b, r, 1, pos) for pos in range(1, a + 1))
    tagged.extend((v, a, b, r, 2, pos) for pos in range(1, b + 1))
    if r > 0:
        tagged.append((v, a, b, r, 3, 0))
tidx = {s: i for i, s in enumerate(tagged)}
nt = len(tagged)
A = np.zeros((nt, nt))
g = np.zeros(nt)  # интенсивности успешного поглощения
ell = np.zeros(nt)  # интенсивности потери помеченной заявки


def jump(i, state, rate):
    j = tidx[state]
    if i != j and rate > 0:
        A[i, j] += rate


for i, (v, a, b, r, side, pos) in enumerate(tagged):
    for w in range(m):
        if w != v and D0[v, w] > 0:
            jump(i, (w, a, b, r, side, pos), D0[v, w])
        rate = D1[v, w]
        if rate == 0:
            continue
        if a < K1:
            target = (w, a + 1, b, r, side, pos)
        elif r < R:
            target = (w, a, b, r + 1, side, pos)
        else:
            target = (w, a, b, r, side, pos)
        jump(i, target, rate)

    if a > 0:
        if side == 1 and pos == 1:  # завершение помеченной на узле 1
            if b < K2:
                dst = (v, a - 1, b + 1, r, 2, b + 1)
            elif r < R:
                dst = (v, a - 1, b, r + 1, 3, 0)
            else:
                dst = None
                ell[i] += mu1
        else:  # завершение чужой заявки на узле 1
            newpos = pos - int(side == 1)
            if b < K2:
                dst = (v, a - 1, b + 1, r, side, newpos)
            elif r < R:
                dst = (v, a - 1, b, r + 1, side, newpos)
            else:
                dst = (v, a - 1, b, r, side, newpos)
        if dst is not None:
            jump(i, dst, mu1)

    if b > 0:
        if side == 2 and pos == 1:
            g[i] += mu2  # успешное завершение помеченной заявки
        else:
            jump(i, (v, a, b - 1, r, side, pos - int(side == 2)), mu2)

    if r > 0 and a < K1:
        if side == 3:
            jump(i, (v, a + 1, b, r - 1, 1, a + 1), nu)
            if r > 1:
                jump(i, (v, a + 1, b, r - 1, 3, 0), (r - 1) * nu)
        else:
            jump(i, (v, a + 1, b, r - 1, side, pos), r * nu)

for i in range(nt):
    A[i, i] = -A[i, :].sum() - g[i] - ell[i]
assert np.max(np.abs(A.sum(axis=1) + g + ell)) < 1e-11

# Начальный вес — на одно внешнее поступление (не на принятую заявку).
gamma = np.zeros(nt)
for i, (v, a, b, r) in enumerate(states):
    for w in range(m):
        weight = pi[i] * D1[v, w] / lam
        if a < K1:
            target = (w, a + 1, b, r, 1, a + 1)
        elif r < R:
            target = (w, a, b, r + 1, 3, 0)
        else:
            continue  # немедленная потеря, T = 0
        gamma[tidx[target]] += weight

h = solve(-A, g)              # h_i = P(успех | состояние i)
weighted_time = solve(-A, h)  # E[T 1_успех | состояние i]
p_success = float(gamma @ h)
mean_success = float((gamma @ weighted_time) / p_success)
mean_all = float(gamma @ solve(-A, np.ones(nt)))
assert abs(p_success - lambda2 / lam) < 1e-9
assert abs(mean_all - L / lam) < 1e-9

# 3. Выход первого узла: распределение и корреляция интервалов.
alpha = pi @ H1 / lambda1
Z = H1 - Q
u1 = solve(Z, np.ones(m * N))
mean_delta = float(alpha @ u1)
second_delta = float(2 * alpha @ solve(Z, u1))
cross_delta = float(alpha @ solve(Z, solve(Z, H1 @ u1)))
corr_delta = (cross_delta - mean_delta ** 2) / (second_delta - mean_delta ** 2)
F1 = float(1 - alpha @ expm(-Z) @ np.ones(m * N))  # F_delta(1)
assert abs(mean_delta - 1 / lambda1) < 1e-9

print(f"Число состояний Q: {m * N}; A: {nt}")
print(f"lambda = {lam:.6f}")
print(f"lambda_out,1 = {lambda1:.6f}; lambda_out,2 = {lambda2:.6f}")
print(f"lambda_loss,0 = {lambda_loss0:.6f}; lambda_loss,12 = {lambda_loss12:.6f}")
print(f"P_loss = {p_loss:.6f}; P_success = {p_success:.6f}")
print(f"L = {L:.6f}; E[T_all] = {mean_all:.6f}")
print(f"E[T | success] = {mean_success:.6f}")
print(f"E[Delta] = {mean_delta:.6f}; F_Delta(1) = {F1:.6f}")
print(f"Corr(Delta_n, Delta_(n+1)) = {corr_delta:.6f}")
