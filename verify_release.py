#!/usr/bin/env python3
"""Standard-library exact replay for the frozen [[10,2,3]] result."""
import argparse,itertools,json
from collections import Counter
from qec_exact import *
from fault_model import first_order_cnot_ambiguity,verify_witness

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
    assert code_parameters()==(10,2,3)
    zs=rowspace(Z_BASE); xs=rowspace(X_BASE)
    assert Counter(v.bit_count() for v in zs)==Counter({6:10,4:5})
    assert Counter(v.bit_count() for v in xs)==Counter({6:10,4:5})
    assert {v for v in zs if v.bit_count()==4}==set(map(mask,Z_CHECKS))
    assert {v for v in xs if v.bit_count()==4}==set(map(mask,X_CHECKS))
    assert all(gf2_rank(mask(Z_CHECKS[i]) for i in c)==4 for c in itertools.combinations(range(5),4))
    assert all(gf2_rank(mask(X_CHECKS[i]) for i in c)==4 for c in itertools.combinations(range(5),4))

    a8=s8=0
    for zi in itertools.combinations(range(5),4):
        zr=tuple(Z_CHECKS[i] for i in zi)
        for xi in itertools.combinations(range(5),4):
            xr=tuple(X_CHECKS[i] for i in xi); a8+=1; schedules=enumerate_four_layer_schedules(zr,xr); s8+=len(schedules)
            for colors in schedules:assert first_order_cnot_ambiguity(layers_from_colors(colors,zr,xr),zr,xr) is not None
    assert (a8,s8)==(25,740)

    zm=tuple(ids for ids in itertools.combinations_with_replacement(range(5),5) if gf2_rank(mask(Z_CHECKS[i]) for i in ids)==4)
    xm=tuple(ids for ids in itertools.combinations_with_replacement(range(5),5) if gf2_rank(mask(X_CHECKS[i]) for i in ids)==4)
    assert len(zm)==len(xm)==21
    a9=reject9=sched_arch9=s9=0
    for orient,multis in (("Z",zm),("X",xm)):
        for multi in multis:
            for sub in itertools.combinations(range(5),4):
                zi=multi if orient=="Z" else sub; xi=sub if orient=="Z" else multi
                zr=tuple(Z_CHECKS[i] for i in zi); xr=tuple(X_CHECKS[i] for i in xi); a9+=1
                degree=[0]*N_DATA
                for row in zr+xr:
                    for q in row:degree[q]+=1
                if max(degree)>4:reject9+=1; continue
                assert len(set(multi))==5
                schedules=enumerate_four_layer_schedules(zr,xr); sched_arch9+=bool(schedules); s9+=len(schedules)
                for colors in schedules:assert first_order_cnot_ambiguity(layers_from_colors(colors,zr,xr),zr,xr) is not None
    assert (a9,reject9,sched_arch9,s9)==(210,200,10,160)

    witness=verify_witness()
    report={
      "schema":"qec-10-2-3-four-layer-minimum-v1",
      "claim":{"code":"[[10,2,3]] CSS rotated-toric code","architecture":"direct one-ancilla-per-measured-stabilizer CSS extraction in exactly four conflict-free CNOT layers","fault_model":"three repeated rounds; arbitrary single nonidentity two-qubit Pauli after any CNOT; perfect ancilla resets and terminal syndrome closure; binary ancilla preparation/measurement flips also checked for the witness","minimum_measured_checks":10,"minimum_total_qubits_in_architecture":20},
      "code_parameters":[10,2,3],
      "rowspace_nonzero_weight_distribution":{"Z":{"4":5,"6":10},"X":{"4":5,"6":10}},
      "lower_bound":{"fewer_than_8_checks":"impossible because rank 4 must be measured in each CSS basis","eight_check_architectures":a8,"eight_check_ideal_schedules":s8,"eight_check_schedules_with_explicit_fault_collision":s8,"nine_check_rank4_multiset_architectures":a9,"nine_check_architectures_rejected_by_data_degree_gt_4":reject9,"nine_check_schedulable_architectures":sched_arch9,"nine_check_ideal_schedules":s9,"nine_check_schedules_with_explicit_fault_collision":s9},
      "upper_bound_witness":witness,"status":"PASS"}
    print(json.dumps(report,sort_keys=True,separators=(',',':')) if args.json else json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
