# -*- coding:utf-8 -*-
from miniadt import ADTTypeProvider
from miniadt.adttype import ADTType


T0 = ADTTypeProvider("T0")
C00 = T0("C0", "")
C01 = T0("C1", "")

T1 = ADTTypeProvider("T1")
C10 = T0("C0", "")


print(issubclass(C00, ADTType))  # => True
print(isinstance(C00(), C00))  # => True

# but
print(issubclass(C00, T0)) # => True?
# or someting as parent class of C00 and C01 (not C10)
