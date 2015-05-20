import serpent

from ethereum import tester as t

s = t.state()
c = s.abi_contract('def foo(a:str):\n  return(text("dogerqwrqwr"):str)')
print c.foo("klein")
