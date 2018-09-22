from openmdao.api import ExplicitComponent
import numpy as np
class AeroShell(ExplicitComponent):
    """Aeroshell of the pod"""
    def initialize(self):
       """Declare options"""
    
        # Need to convert this to an input at some point
        self.options.declare('Mass', 
                             default=1.,
                             types=np.ScalarType,
                             desc='Mass of the HyperJackets Pod')
    
        # The following properties need to be made more accurate ASAP.
        # These should not exist like this
    
        self.options.declare('Area'
                             default=1.
                             types=np.ScalarType,
                             desc='Pod Lift Area')
    
        self.options.declare('LiftCoefficient'
                             default=1.
                             types=np.ScalarType,
                             desc='Lift Coefficient of Pod')
    
        self.options.declare('DragCoefficient'
                             default=1.
                             types=np.ScalarType,
                             desc='Drag Coefficient of Pod')
    def setup(self):
       """Declare inputs and outputs"""
    
        # Inputs
        self.add_input('AirDensity', 
                       0.5,
                       desc="Air Density around the aeroshell")
        self.add_input('Velocity', 
                       0,
                       desc="Speed of the aeroshell (and of the pod)")
    
        # Outputs
        self.add_output('Lift', 0.0,
                        units="kg*m/s^2",
                        desc="Lifting force due to the aeroshell")
        self.add_output('Drag', 0.0, 
                        units="kg*m/s^2",
                        desc="Drag force due to the aeroshell")
    
        # Independence
        self.declare_partials('Lift',
                              'DragCoefficient',
                              dependent=False)
        self.declare_partials('Drag',
                              'LiftCoefficient',
                              dependent=False)
    
    def compute(self, inputs, outputs):
        """Compute outputs"""
    
        # Properties of the tube
        rho = inputs['AirDensity']
    
        # Aerodynamic Coefficients
        c_l = self.options['LiftCoefficient']
        c_d = self.options['DragCoefficient']
    
        # Properties of the pod
        area = self.options['Area']
        vel = inputs['Velocity']
    
        lift = - 0.5*rho*c_l*area*vel*vel
        drag = 0.5*rho*c_d*area*vel*vel
    
        outputs['Lift'] = lift
        outputs['Drag'] = drag
    def compute_partials(self, inputs, partials):
        """ Computation of partial derivatives."""
    
        c_l = self.options["LiftCoefficient"]
        c_d = self.options["DragCoefficient"]
        area = self.options["Area"]
        vel = inputs["Velocity"]
        rho = inputs["AirDensity"]
    
        partials['Lift', 'AirDensity'] = -0.5*c_l*area*vel*vel
        partials['Lift', 'Velocity'] = - c_l*area*rho*vel
