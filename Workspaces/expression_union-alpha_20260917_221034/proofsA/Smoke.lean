import Common.Operators

namespace SmokeCommon

open DLWCommon

theorem hx_antisym (F G : Jet ℚ) : hirotaX F G = -hirotaX G F :=
  hirotaX_antisymmetric F G

end SmokeCommon