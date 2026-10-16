import ResearchTarget
import FinalBridge

/-! Verified deliverable entry point.
The unrestricted conjecture SquarePacking37.GlobalOptimality is a definition,
not a proved theorem. The final lower bound below retains explicit support
assumptions. See ResearchTarget for the two remaining global obligations. -/

#check SquarePacking37.GlobalOptimality
#print axioms Packing37.exists_packing_37
#print axioms Packing37.closed_disjoint
#print axioms Cantrell37.candidateSide_strict_interval
#print axioms Cantrell37.support_model_minimum
#print axioms Cantrell37.support_model_attains_minimum
#print axioms Cantrell37.conditional_branch_lower_bound
