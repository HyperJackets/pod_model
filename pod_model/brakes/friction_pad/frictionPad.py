from pod_model.brakes.frriction_pad.brakeForce import BrakeForce
from pod_model.brakes.frriction_pad.frictionCoefficient import FrictionCoefficient
from pod_model.brakes.frriction_pad.heatConduction import HeatConduction
from pod_model.brakes.frriction_pad.heatConvective import HeatConvective
from pod_model.brakes.frriction_pad.heatGeneration import HeatGeneration
from pod_model.brakes.frriction_pad.temperatureChange import TemperatureChange

class FrictionPad(Group):

        ################# Inputs ##################
        # mu.SurfaceVelocity                      # 
        # brakeForce.NormalForce                  #
        # heatConvective.AreaBrakePad             #
        # heatConvective.TemperatureSurrounding   #
        # heatConduction.AreaContact              #
        # heatConduction.TemperatureContact       #
        # temperatureChange.Mass                  #
        ###########################################

        ################ Outputs ##################
        # brakeForce.FrictionForce                #
        # heatGeneration.HeatRateTrack            #
        ###########################################

    def setup(self):

        # Add subsystems and prmoted inputs and outputs

        self.add_subsystem('mu', FrictionCoefficient(), promotes='SurfaceVelocity')

        self.add_subsystem('heatConduction', HeatConduction(), promotes=['AreaContact','TemperatureContact'])
        self.add_subsystem('heatConvective', HeatConvective(), promotes=['AreaBrakePad','TemperatureSurrounding'])
        self.add_subsystem('heatGeneration', HeatGenerative(), promotes=['HeatRateTrack'])

        self.add_subsystem('brakeForce', BrakeForce(), promotes=['NormalForce','FrictionForce'])
        self.add_subsystem('temperatureChange', TemperatureChange(), promotes=['Mass'])

        # Internal Connections
        self.connect('mu.FrictionCoefficient', 'brakeForce.FrictionCoefficient')

        self.connect('brakeForce.FrictionForce', 'heatGeneration.BrakingForce')

        self.connect('heatGeneration.HeatRatePad','temperatureChange.HeatGenerated')
        self.connect('heatConduction.HeatRate','temperatureChange.HeatConduction')
        self.connect('heatConvective.HeatRate','temperatureChange.HeatConvection')

        self.connect('temperatureChange.NewTemperature',['mu.Temperature','heatConduction.TemperatureBrakePad','heatConvective.TemperatureBrakePad','temperatureChange.Temperature'])

    def configure(self):
        # This solver won't solve the sytem. We want
        # to override it in the parent.
        self.nonlinear_solver = NonlinearBlockGS()
