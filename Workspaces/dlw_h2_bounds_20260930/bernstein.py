"""Exact rational branch and bound for a rational function on a rectangle.

N/D = sum(B_ij*d_ij*(n_ij/d_ij))/sum(B_ij*d_ij) when d_ij>0.
Thus the Bernstein coefficient ratios bound every value on the box.
De Casteljau subdivision uses exact Fraction arithmetic throughout.
"""
from fractions import Fraction as F
from math import comb
import heapq
import time
import sympy as s


def fraction(v):return F(int(s.numer(v)),int(s.denom(v)))


def coefficients(poly, variables, shape):
    nx,ny=shape
    p=s.Poly(poly,*variables)
    mat=[[F(0) for _ in range(ny+1)] for _ in range(nx+1)]
    for (i,j),c in p.terms():
        c=fraction(c)
        for k in range(i,nx+1):
            ci=F(comb(k,i),comb(nx,i))
            for l in range(j,ny+1):
                mat[k][l]+=c*ci*F(comb(l,j),comb(ny,j))
    return mat


def split_line(line):
    line=list(line)
    left,right=[line[0]],[line[-1]]
    while len(line)>1:
        line=[(a+b)/2 for a,b in zip(line,line[1:])]
        left.append(line[0]);right.append(line[-1])
    return left,list(reversed(right))


def split(mat,axis):
    if axis==0:
        tr=list(zip(*mat));pairs=[split_line(line) for line in tr]
        return [list(map(list,zip(*(p[i] for p in pairs)))) for i in (0,1)]
    pairs=[split_line(line) for line in mat]
    return [[p[i] for p in pairs] for i in (0,1)]


def bounds(num,den):
    vals=[]
    for nr,dr in zip(num,den):
        for n,d in zip(nr,dr):
            if d<=0:raise ValueError('Nonpositive denominator Bernstein coefficient')
            vals.append(n/d)
    return min(vals),max(vals)


def center_value(num,den):
    nx,ny=len(num)-1,len(num[0])-1
    top,bottom=F(0),F(0)
    for i in range(nx+1):
        for j in range(ny+1):
            b=comb(nx,i)*comb(ny,j)
            top+=b*num[i][j];bottom+=b*den[i][j]
    return top/bottom


def abs_sup(expr,variables,domain=None,tolerance=F(1,10**6),max_splits=20000,seconds=180):
    domain=domain or [(s.Rational(0),s.Rational(1))]*2
    xx,yy=s.symbols('bx by')
    substitutions={v:l+(r-l)*w for v,(l,r),w in zip(variables,domain,(xx,yy))}
    n,d=s.fraction(s.cancel(expr))
    n=s.Poly(n.subs(substitutions,simultaneous=True).expand(),xx,yy)
    d=s.Poly(d.subs(substitutions,simultaneous=True).expand(),xx,yy)
    shape=tuple(max(n.degree(v),d.degree(v)) for v in (xx,yy))
    num,den=coefficients(n.as_expr(),(xx,yy),shape),coefficients(d.as_expr(),(xx,yy),shape)
    try:lo,hi=bounds(num,den)
    except ValueError:
        den=[[-v for v in row] for row in den];num=[[-v for v in row] for row in num]
        lo,hi=bounds(num,den)
    witness=abs(center_value(num,den))
    box=((F(0),F(1)),(F(0),F(1)))
    witness_point=(F(1,2),F(1,2))
    upper=max(abs(lo),abs(hi))
    serial=0
    queue=[(-upper,serial,num,den,box,(0,0))]
    started=time.monotonic()
    splits=0
    while queue and -queue[0][0]-witness>tolerance and splits<max_splits and time.monotonic()-started<seconds:
        _,_,nm,dm,box,depth=heapq.heappop(queue)
        axis=0 if depth[0]<=depth[1] else 1
        nms,dms=split(nm,axis),split(dm,axis)
        midpoint=sum(box[axis])/2
        for child,(nchild,dchild) in enumerate(zip(nms,dms)):
            newbox=list(box)
            newbox[axis]=(box[axis][0],midpoint) if child==0 else (midpoint,box[axis][1])
            newbox=tuple(newbox)
            newdepth=list(depth);newdepth[axis]+=1
            value=abs(center_value(nchild,dchild))
            if value>witness:
                witness=value;witness_point=tuple(sum(iv)/2 for iv in newbox)
            lo,hi=bounds(nchild,dchild)
            cap=max(abs(lo),abs(hi))
            if cap>witness:
                serial+=1
                heapq.heappush(queue,(-cap,serial,nchild,dchild,newbox,tuple(newdepth)))
        splits+=1
    upper=max(witness,-queue[0][0] if queue else witness)
    point=[fraction(l)+(fraction(r)-fraction(l))*w for (l,r),w in zip(domain,witness_point)]
    return {'lower_exact':str(witness),'upper_exact':str(upper),
            'lower':float(witness),'upper':float(upper),'gap':float(upper-witness),
            'witness':[str(w) for w in point],'subdivisions':splits,'remaining_boxes':len(queue),
            'degrees':shape,'tolerance_reached':upper-witness<=tolerance,
            'method':'Exact rational Bernstein coefficient ratios with dyadic subdivision.'}
