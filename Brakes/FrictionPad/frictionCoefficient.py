from openmdao.api import ExplicitComponent
import numpy as np
class FrictionCoefficient(ExplicitComponent):
    """Class to find the friction coefficient of the friction pad"""

    def initialize(self):
        """Declare options"""
        self.options.declare('HeatCapacity',
                             default=1.0,
                             types=np.ScalarType,
                             desc="Heat Capacity of the Friction Brakes")

    def setup(self):
        """Declare inputs and outputs"""
        self.add_output('FrictionForce',
                        0.45,
                        desc="Friction Force generated by the friction pad")
        self.add_input('Temperature',
                       1.,
                       desc="Temperature of the friction pad.")
        self.add_input('Mass',
                       1.,
                       desc="Mass of the friction pad.")
        self.add_input('HeatConduction',
                       1.,
                       desc="Heat lost due to conduction")
        self.add_input('HeatConvection',
                       1.,
                       desc="Heat lost due to convection")
        self.add_input('HeatGenerated',
                       1.,
                       desc="Heat created due to friction")
        self.add_output('NewTemperature',
                        0.45,
                        desc="Friction Force generated by the friction pad")
        self.add_output('FrictionCoefficient',
                        0.45,
                        desc="Friction Coefficient of the friction pad")

    def compute(self,inputs,outputs):
        """Compute outputs"""
        c_f = inputs["FrictionCoefficient"]
        normal_force = inputs["NormalForce"]
        friction_force = c_f * normal_force
        outputs["FrictionForce"] = friction_force
        mass = inputs["Mass"]
        temperature = inputs["Temperature"]
        heat_capacity = self.options["HeatCapacity"]
                
        time_step = 0.01
        
        heat_convection = inputs["HeatConvection"]
        heat_conduction = inputs["HeatConduction"]
        heat_generated = inputs["HeatGenerated"]
        
        if heat_convection > 0:
            heat_convection *= -1
        if heat_conduction > 0:
            heat_conduction *= -1
        if heat_generated < 0:
            heat_generated *= -1
        heat_rate = heat_convection + heat_conduction + heat_generated
        change_in_temperature = heat_rate/(mass*heat_capacity)*time_step
        
        temperature += change_in_temperature
        outputs["NewTemperature"] = temperature


#run stand-alone component
if __name__ == "__main__":

#    from openmdao.api import Group, Problem, IndepVarComp
#
#    comp = IndepVarComp()
#    comp.add_output('brake_temperature', val=3.0, lower=0, upper=10)
#    comp.add_output('mass_brake_pad', val=2.0, lower=1, upper=20)
#    comp.add_output('heat_conductive', val=1.0, lower=0, upper=10)
#    comp.add_output('heat_convective', val=1.0, lower=1, upper=20)
#    comp.add_output('heat_generated', val=100.0, lower=1, upper=20)
#
#    prob = Problem()
#    prob.model.add_subsystem('indep_var', comp)
#    prob.model.add_subsystem('my_comp', TemperatureChange())
#
#    prob.model.connect('indep_var.brake_temperature', 'my_comp.Temperature')
#    prob.model.connect('indep_var.mass_brake_pad',    'my_comp.Mass')
#    prob.model.connect('indep_var.heat_conductive',   'my_comp.HeatConduction')
#    prob.model.connect('indep_var.heat_convective',   'my_comp.HeatConvection')
#    prob.model.connect('indep_var.heat_generated',    'my_comp.HeatGenerated')
#
#
#    prob.setup()
#    prob.run_model()
#    print(prob['my_comp.NewTemperature'])
