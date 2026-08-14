"""Exact GF(2), stabilizer, and four-layer schedule primitives."""
from __future__ import annotations
import itertools
from collections import Counter
from typing import Iterable, Sequence

N_DATA = 10
ROUNDS = 3
Z_BASE = ((0,1,3,4),(2,3,5,6),(4,5,7,8),(0,6,7,9))
X_BASE = ((0,2,3,9),(1,2,4,5),(3,4,6,7),(5,6,8,9))
Z_REDUNDANT = (1,2,8,9)
X_REDUNDANT = (0,1,7,8)
Z_CHECKS = Z_BASE + (Z_REDUNDANT,)
X_CHECKS = X_BASE + (X_REDUNDANT,)
FOUR_PERMS = tuple(itertools.permutations(range(4)))

def mask(row: Sequence[int]) -> int:
    out=0
    for q in row: out |= 1<<q
    return out

def parity(bits:int)->int: return bits.bit_count()&1

def reduced_basis(values:Iterable[int])->tuple[int,...]:
    pivots={}
    for value in values:
        x=int(value)
        while x:
            p=x.bit_length()-1
            if p in pivots: x^=pivots[p]; continue
            pivots[p]=x
            for q in tuple(pivots):
                if q!=p and ((pivots[q]>>p)&1): pivots[q]^=x
            break
    return tuple(pivots[p] for p in sorted(pivots,reverse=True))

def gf2_rank(values:Iterable[int])->int: return len(reduced_basis(values))

def rowspace(rows:Sequence[Sequence[int]])->tuple[int,...]:
    gens=tuple(mask(r) for r in rows); out=[]
    for selector in range(1,1<<len(gens)):
        v=0
        for i,g in enumerate(gens):
            if (selector>>i)&1: v^=g
        out.append(v)
    return tuple(out)

def code_parameters()->tuple[int,int,int]:
    hz=tuple(map(mask,Z_BASE)); hx=tuple(map(mask,X_BASE))
    assert all(parity(a&b)==0 for a in hz for b in hx)
    k=N_DATA-gf2_rank(hz)-gf2_rank(hx)
    xs=set(rowspace(X_BASE))|{0}; zs=set(rowspace(Z_BASE))|{0}
    dx=dz=N_DATA+1
    for e in range(1,1<<N_DATA):
        w=e.bit_count()
        if w<dx and all(parity(e&z)==0 for z in hz) and e not in xs: dx=w
        if w<dz and all(parity(e&x)==0 for x in hx) and e not in zs: dz=w
    assert dx==dz
    return N_DATA,k,dx

def logical_basis()->tuple[tuple[int,int],tuple[int,int]]:
    hz=tuple(map(mask,Z_BASE)); hx=tuple(map(mask,X_BASE))
    def quotient(opp,stabs):
        current=tuple(stabs); found=[]; r=gf2_rank(current)
        for v in range(1,1<<N_DATA):
            if any(parity(v&c) for c in opp): continue
            nr=gf2_rank(current+(v,))
            if nr>r:
                found.append(v); current+=(v,); r=nr
                if len(found)==2:return tuple(found)
        raise AssertionError("logical basis not found")
    lx=quotient(hz,hx); lz=[]
    for target in (1,2):
        for v in range(1,1<<N_DATA):
            if any(parity(v&c) for c in hx): continue
            patt=parity(lx[0]&v)|(parity(lx[1]&v)<<1)
            if patt==target: lz.append(v); break
    assert [[parity(lx[i]&lz[j]) for j in range(2)] for i in range(2)]==[[1,0],[0,1]]
    return lx,(lz[0],lz[1])

LX,LZ=logical_basis()

def cross_intersections(z_rows,x_rows):
    mz=len(z_rows); rows=tuple(z_rows)+tuple(x_rows); out={}
    for xi in range(mz,len(rows)):
        for zi in range(mz):
            inter=tuple(sorted(set(rows[xi])&set(rows[zi])))
            if inter:
                assert len(inter)%2==0; out[(xi,zi)]=inter
    return out

def layers_from_colors(colors,z_rows,x_rows):
    mz=len(z_rows); rows=tuple(z_rows)+tuple(x_rows); layers=[[] for _ in range(4)]
    for i,(row,assignment) in enumerate(zip(rows,colors)):
        anc=N_DATA+i
        for q,layer in zip(row,assignment):
            layers[layer].append((q,anc) if i<mz else (anc,q))
    return tuple(tuple(layer) for layer in layers)

def backprop_pauli(x,z,layers):
    for layer in reversed(layers):
        for c,t in reversed(layer):
            if (x>>c)&1: x^=1<<t
            if (z>>t)&1: z^=1<<c
    return x,z

def ideal_measurement_ok(colors,z_rows,x_rows)->bool:
    layers=layers_from_colors(colors,z_rows,x_rows); mz=len(z_rows); mx=len(x_rows)
    data=(1<<N_DATA)-1
    za=sum(1<<(N_DATA+i) for i in range(mz)); xa=sum(1<<(N_DATA+mz+j) for j in range(mx))
    for i,row in enumerate(z_rows):
        anc=N_DATA+i; x,z=backprop_pauli(0,1<<anc,layers); dx=x; dz=z^mask(row)^(1<<anc)
        if dx&data or dz&data or dx&za or dz&xa:return False
    for j,row in enumerate(x_rows):
        anc=N_DATA+mz+j; x,z=backprop_pauli(1<<anc,0,layers); dx=x^mask(row)^(1<<anc); dz=z
        if dx&data or dz&data or dx&za or dz&xa:return False
    return True

def enumerate_four_layer_schedules(z_rows,x_rows):
    """Exhaustive ideal schedule enumeration with exact MRV branching."""
    rows=tuple(tuple(r) for r in z_rows)+tuple(tuple(r) for r in x_rows)
    cross=cross_intersections(z_rows,x_rows); used=[0]*N_DATA; assigned=[None]*len(rows); out=[]
    def assignment_ok(i,a):
        row=rows[i]
        if any((used[q]>>layer)&1 for q,layer in zip(row,a)):return False
        for (xi,zi),inter in cross.items():
            if i not in (xi,zi):continue
            other=zi if i==xi else xi
            if assigned[other] is None:continue
            if i==xi:
                xm={q:c for q,c in zip(rows[i],a)}; zm={q:c for q,c in zip(rows[other],assigned[other])}
            else:
                xm={q:c for q,c in zip(rows[other],assigned[other])}; zm={q:c for q,c in zip(rows[i],a)}
            if sum(xm[q]<zm[q] for q in inter)%2:return False
        return True
    def rec(left):
        if not left:
            sol=tuple(assigned); assert ideal_measurement_ok(sol,z_rows,x_rows); out.append(sol); return
        best_i=-1; best=None
        for i in left:
            opts=[a for a in FOUR_PERMS if assignment_ok(i,a)]
            if not opts:return
            if best is None or len(opts)<len(best):
                best_i,best=i,opts
                if len(opts)==1:break
        nxt=tuple(i for i in left if i!=best_i); row=rows[best_i]
        for a in best:
            assigned[best_i]=a
            for q,c in zip(row,a):used[q]|=1<<c
            rec(nxt)
            for q,c in zip(row,a):used[q]^=1<<c
            assigned[best_i]=None
    rec(tuple(range(len(rows))))
    return out
