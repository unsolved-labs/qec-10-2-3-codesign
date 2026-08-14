"""Exact single-fault propagation and the released ten-check witness."""
from __future__ import annotations
from qec_exact import N_DATA,ROUNDS,Z_CHECKS,X_CHECKS,LX,LZ,mask,parity,ideal_measurement_ok

PAULI={"I":(0,0),"X":(1,0),"Y":(1,1),"Z":(0,1)}
TWO_QUBIT_PAULIS=tuple((a,b) for a in "IXYZ" for b in "IXYZ" if (a,b)!=("I","I"))
WITNESS_LAYERS=(
 ((1,10),(3,11),(5,12),(7,13),(9,14),(15,0),(16,2),(17,4),(18,6),(19,8)),
 ((0,10),(2,11),(4,12),(6,13),(8,14),(15,9),(16,1),(17,3),(18,5),(19,7)),
 ((4,10),(6,11),(8,12),(0,13),(2,14),(15,3),(16,5),(17,7),(18,9),(19,1)),
 ((3,10),(5,11),(7,12),(9,13),(1,14),(15,2),(16,4),(17,6),(18,8),(19,0)),
)

def apply_cnot(x,z,c,t):
    if (x>>c)&1:x^=1<<t
    if (z>>t)&1:z^=1<<c
    return x,z

def fault_signature(layers,z_rows,x_rows,location,pidx):
    mz=len(z_rows); mx=len(x_rows); nchecks=mz+mx; gates=tuple(g for layer in layers for g in layer)
    per=len(gates); fr,fg=divmod(location,per); assert 0<=fr<ROUNDS
    pa,pb=TWO_QUBIT_PAULIS[pidx]; data=(1<<N_DATA)-1; x=z=0; prev=0; syndrome=0
    for r in range(ROUNDS):
        x&=data; z&=data; gi=0
        for layer in layers:
            for c,t in layer:
                x,z=apply_cnot(x,z,c,t)
                if r==fr and gi==fg:
                    xa,za=PAULI[pa]; xb,zb=PAULI[pb]
                    if xa:x^=1<<c
                    if za:z^=1<<c
                    if xb:x^=1<<t
                    if zb:z^=1<<t
                gi+=1
        outcome=0
        for i in range(mz):outcome|=((x>>(N_DATA+i))&1)<<i
        for j in range(mx):outcome|=((z>>(N_DATA+mz+j))&1)<<(mz+j)
        syndrome|=(outcome^prev)<<(r*nchecks); prev=outcome
    xd=x&data; zd=z&data; terminal=0
    for i,row in enumerate(z_rows):terminal|=parity(xd&mask(row))<<i
    for j,row in enumerate(x_rows):terminal|=parity(zd&mask(row))<<(mz+j)
    syndrome|=(terminal^prev)<<(ROUNDS*nchecks)
    logical=0
    for i,lz in enumerate(LZ):logical|=parity(xd&lz)<<i
    for i,lx in enumerate(LX):logical|=parity(zd&lx)<<(2+i)
    return syndrome,logical

def first_order_cnot_ambiguity(layers,z_rows,x_rows):
    seen={0:(0,None)}; per=sum(map(len,layers))
    for location in range(ROUNDS*per):
        for pidx,pauli in enumerate(TWO_QUBIT_PAULIS):
            syndrome,logical=fault_signature(layers,z_rows,x_rows,location,pidx)
            fault={"location":location,"round":location//per,"gate_index":location%per,"pauli":"".join(pauli),"syndrome":syndrome,"logical":logical}
            if syndrome==0 and logical!=0:return {"kind":"undetected_logical","faults":[fault]}
            if syndrome in seen:
                old,old_fault=seen[syndrome]
                if old!=logical:return {"kind":"logical_collision","faults":[old_fault,fault]}
            else:seen[syndrome]=(logical,fault)
    return None

def verify_witness():
    for layer in WITNESS_LAYERS:
        active=set()
        for c,t in layer:
            assert c not in active and t not in active; active|={c,t}
        assert len(layer)==10
    colors=[[None]*4 for _ in range(10)]; mz=5
    for lid,layer in enumerate(WITNESS_LAYERS):
        for c,t in layer:
            if c<N_DATA:check=t-N_DATA; data=c; row=Z_CHECKS[check]; assert check<mz
            else:check=c-N_DATA; data=t; row=X_CHECKS[check-mz]; assert check>=mz
            pos=row.index(data); assert colors[check][pos] is None; colors[check][pos]=lid
    assert ideal_measurement_ok(tuple(tuple(r) for r in colors),Z_CHECKS,X_CHECKS)
    seen={0:0}; per=40; mechanisms=0
    for location in range(ROUNDS*per):
        for pidx in range(15):
            s,l=fault_signature(WITNESS_LAYERS,Z_CHECKS,X_CHECKS,location,pidx); mechanisms+=1
            assert not(s==0 and l!=0)
            if s in seen:assert seen[s]==l
            else:seen[s]=l
    spam=0
    for r in range(ROUNDS):
        for j in range(10):
            s=(1<<(r*10+j))|(1<<((r+1)*10+j)); assert seen.get(s,0)==0; seen[s]=0; spam+=2
    return {"cnot_fault_mechanisms":mechanisms,"ancilla_prep_measure_fault_mechanisms":spam,"detector_syndromes_seen":len(seen)}
