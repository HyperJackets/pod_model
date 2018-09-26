from openmdao.api import ExplicitComponent
import numpy as np
class HeatConvective(ExplicitComponent):
    """Class to find the heat generated due to the braking force"""

    def initialize(self):
        """Declare options"""
        self.options.declare('ConvectiveCoefficient',
                             default=0.5,
                             types=np.ScalarType,
                             desc="Convective Coefficient of the brake pad")

    def setup(self):
        """Declare inputs and outputs"""
        self.add_input('TemperatureBrakePad',
                       1.,
                       desc="Temperature of the brake pad")
        self.add_input('TemperatureSurrounding',
                       1.,
                       desc="Temperature of the surrounding")
        self.add_input('AreaBrakePad',
                       1.,
                       desc="Area subject to convective heat loss")
        self.add_output('HeatRate',
                        0.45,
                        desc="Rate of heat lost through convection")

    def compute(self,inputs,outputs):
        """Compute outputs"""
        h = self.options["ConvectiveCoefficient"]
        assert h > 0, "Convective Coefficient must be positive"
        area = inputs["Area"]
        assert area > 0, "Area must be a positive non-zero quantity"
        sur_temp = inputs["TemperatureSurrounding"]
        pad_temp = inputs["TemperatureBrakePad"]
        assert pad_temp > sur_temp, "Surrounding temperature is greater than the pad temperature - Convection is impossible"
        temp_diff = pad_temp - sur_temp
        
        heat_loss = -(h * temp_diff * area)
        
        assert heat_loss < 0, "Heat Loss is always a negative quantity"
        outputs["HeatRate"] = heat_loss
