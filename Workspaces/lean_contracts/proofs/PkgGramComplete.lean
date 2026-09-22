import PkgC07Complete
import PkgGramBridges
import PkgC09Complete

namespace DLWContract

theorem c08_proved : C08 := c08_of_c07 c07_proved

theorem c16_proved : C16 := c16_of_c08_c09 c08_proved c09_proved

#print axioms c08_proved
#print axioms c16_proved
end DLWContract
