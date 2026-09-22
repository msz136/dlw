"""Exact exploration of local bilinear identities (not a proof by sampling)."""
from fractions import Fraction as F
from itertools import product
from math import prod
import sympy as s


def tau_data(p, q, h, a=F(0), shift='miwa'):
    n = len(p)
    masks = list(product((0, 1), repeat=n))
    data = []
    ell = [1/(p[i]-a)+1/(q[i]+a) for i in range(n)]
    if shift == 'miwa':
        R = [(1+h/(q[i]+a))/(1-h/(p[i]-a)) for i in range(n)]
    else:
        R = [(2+h*ell[i])/(2-h*ell[i]) for i in range(n)]
    for m in masks:
        active = [i for i in range(n) if m[i]]
        g = prod((1/(p[i]+q[i]) for i in active), start=F(1))
        for i in active:
            for j in active:
                if i < j:
                    g *= (p[i]-p[j])*(q[i]-q[j])/((p[i]+q[j])*(p[j]+q[i]))
        ratio = prod((-(p[i]-a)/(q[i]+a) for i in active), start=F(1))
        data.append((m, g*ratio, g, sum(p[i]+q[i] for i in active),
                     sum(q[i]**2-p[i]**2 for i in active),
                     prod((R[i] for i in active), start=F(1))))
    return data


def cross_rows(data, monomials):
    result = {}
    for m,f,g,k,w,R in data:
        for n,ff,gg,kk,ww,RR in data:
            key=tuple(x+y for x,y in zip(m,n))
            row=result.setdefault(key,[F(0)]*(2*len(monomials)))
            for i,(r,t) in enumerate(monomials):
                val=f*gg*(k-kk)**r*(w-ww)**t
                row[i]+=val*R
                row[i+len(monomials)]+=val*RR
    return [r for r in result.values() if any(r)]


if __name__ == '__main__':
    h=F(1,5)
    monomials=[(r,t) for t in range(3) for r in range(5) if r+2*t<=4]
    rows=[]
    for seed in range(1,7):
        p=list(map(F,[seed+1,2*seed+3]))
        q=list(map(F,[seed+4,3*seed+2]))
        rows.extend(cross_rows(tau_data(p,q,h),monomials))
    M=s.Matrix(rows)
    basis=M.nullspace()
    print('monomials:',monomials, 'matrix:',M.shape, 'nullity:',len(basis))
    k,w=s.symbols('k w')
    for v in basis:
        print('P=',s.factor(sum(v[i]*k**r*w**t for i,(r,t) in enumerate(monomials))))
        print('Q=',s.factor(sum(v[i+len(monomials)]*k**r*w**t for i,(r,t) in enumerate(monomials))))
