#This file is part of QNET.
#
#    QNET is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    QNET is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QNET.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2012-2013, Nikolas Tezak
#
###########################################################################

"""
Component definition file for a single mirror CQED Jaynes-Cummings cavity model.

See documentation of :py:class:`SingleSidedJaynesCummings`.
"""
import unittest

from qnet.algebra.circuit_algebra import  Destroy, Matrix, sqrt, SLH, LocalSigma, local_space, I
from qnet.circuit_components.library import make_namespace_string
from qnet.circuit_components.component import Component, SubComponent

from sympy.core.symbol import symbols


class SingleSidedJaynesCummings(Component):
    r"""
    Typical CQED Jaynes-Cummings model with a single laser input/output channel with coupling coefficient :math:`\kappa`
    and a single atomic decay channel with rate :math:`\gamma`.
    The full model is given by:

    .. math::
        S & = \mathbf{1}_2 \\
        L & = \begin{pmatrix} \sqrt{\kappa}a \\ \sqrt{\gamma} \sigma_- \end{pmatrix} \\
        H & = \Delta_f a^\dagger a + \Delta_a \sigma_+ \sigma_- + ig\left(\sigma_+ a - \sigma_- a^\dagger \right)

    As the model is reducible, sub component models for the mode and the atomic decay channel are given by
    :py:class:`CavityPort` and :py:class:`DecayChannel`, respectively.
    """
    
    CDIM = 2
    
    kappa = symbols('kappa', real = True) # decay of cavity mode through cavity mirror
    gamma = symbols('gamma', real = True) # decay rate into transverse modes
    g = symbols('g', real = True)   # coupling between cavity mode and two-level-system
    Delta_a = symbols('Delta_a', real = True) # detuning between the external driving field and the atomic transition
    Delta_f = symbols('Delta_f', real = True) # detuning between the external driving field and the cavity mode
    FOCK_DIM = 20
    
    _parameters = ['kappa', 'gamma', 'g', 'Delta_a', 'Delta_f', 'FOCK_DIM']
    
    
    PORTSIN = ['In1', 'VacIn']
    PORTSOUT = ['Out1', 'UOut']        
    
    sub_blockstructure = (1, 1)


    @property
    def fock_space(self):
        """
        The cavity mode's Hilbert space.

        :type: :py:class:`qnet.algebra.hilbert_space_algebra.LocalSpace`
        """
        return local_space("f", make_namespace_string(self.namespace, self.name), dimension = self.FOCK_DIM)

    @property
    def tls_space(self):
        """
        The two-level-atom's Hilbert space.

        :type: :py:class:`qnet.algebra.hilbert_space_algebra.LocalSpace`
        """
        return local_space("a", make_namespace_string(self.namespace, self.name), basis = ('h', 'g'))

    @property
    def _space(self):
        return self.fock_space * self.tls_space

    
    def _creduce(self):
        return CavityPort(self) + DecayChannel(self)
        
    def _toSLH(self):
        return self.creduce().toSLH()
        

class CavityPort(SubComponent):
    """
    Sub component model for port coupling the internal mode
    of a :py:class:`SingleSidedJaynesCummings` model to the external field.
    The Hamiltonian is included with this first port.
    """


    def __init__(self, cavity):
        super(CavityPort, self).__init__(cavity, 0)
    
    def _toSLH(self):

        sigma_p = LocalSigma(self.tls_space, 'h','g')
        sigma_m = sigma_p.adjoint()

        
        a = Destroy(self.fock_space)
        a_d = a.adjoint()
        
        #coupling to external mode
        L = sqrt(self.kappa) * a
        
        H = self.Delta_f * a_d * a + self.Delta_a * sigma_p * sigma_m + I * self.g * (sigma_p * a - sigma_m * a_d)
        
        return SLH(Matrix([[1]]), Matrix([[L]]), H)
        
class DecayChannel(SubComponent):

    """
    Sub component model for the port coupling the internal two-level atom
    to the vacuum of the transverse free-field modes, inducing spontaneous emission/decay.
    """

    
    def __init__(self, cavity):
        super(DecayChannel, self).__init__(cavity, 1)
    
    def _toSLH(self):
        
        sigma_p = LocalSigma(self.tls_space, 'h','g')
        sigma_m = sigma_p.adjoint()
        
        # vacuum coupling / spontaneous decay
        L = sqrt(self.gamma) * sigma_m
        
        return SLH(Matrix([[1]]), Matrix([[L]]), 0)


# Test the circuit
class _TestSingleSidedJaynesCummings(unittest.TestCase):
    def testCreation(self):
        a = SingleSidedJaynesCummings()
        self.assertIsInstance(a, SingleSidedJaynesCummings)

    def testCReduce(self):
        a = SingleSidedJaynesCummings().creduce()

    def testParameters(self):
        if len(SingleSidedJaynesCummings._parameters):
            pname = SingleSidedJaynesCummings._parameters[0]
            obj = SingleSidedJaynesCummings(name = "TestName", namespace = "TestNamespace", **{pname: 5})
            self.assertEqual(getattr(obj, pname), 5)
            self.assertEqual(obj.name, "TestName")
            self.assertEqual(obj.namespace, "TestNamespace")

        else:
            obj = SingleSidedJaynesCummings(name = "TestName", namespace = "TestNamespace")
            self.assertEqual(obj.name, "TestName")
            self.assertEqual(obj.namespace, "TestNamespace")

    def testToSLH(self):
        aslh = SingleSidedJaynesCummings().toSLH()
        self.assertIsInstance(aslh, SLH)

if __name__ == "__main__":
    unittest.main()
