import pytest


testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]

@pytest.mark.parametrize("sFC,mFS,mFT,pFS,pFT,oT,fC", testdata)
def test_init(self,
              sFC, # steadyStateFrictionCoefficient,
              mFS, # multiplicationFactorSpeed,
              mFT, # multiplicationFactorTemperature,
              pFS, # parameticFactorSpeed,
              pFT, # parametricFactorTemperature,
              oT,  # originalTemperature,
              fC): # frictionCoefficient

    from openmdao.api import Group, Problem, IndepVarComp

    comp = IndepVarComp()
    comp.add_output('SurfaceVelocity', val=3.0, lower=0, upper=10)
    comp.add_output('Temperature', val=2.0, lower=1, upper=20)

    my_comp = TemperatureChange(steadyStateFrictionCoefficient=sFC,
                                multiplicationFactorSpeed=mFS,
                                multiplicationFactorTemperature=mFT,
                                parameticFactorSpeed=pFS,
                                parametricFactorTemperature=pFT,
                                originalTemperature=oT,
                                )
    prob = Problem()
    prob.model.add_subsystem('indep_var', comp)
    prob.model.add_subsystem('my_comp', my_comp)

    prob.model.connect('indep_var.SurfaceVelocity', 'my_comp.SurfaceVelocity')
    prob.model.connect('indep_var.Temperature',    'my_comp.Temperature')
    prob.setup()
    prob.run_model()
    assert prob['my_comp.FrictionCoefficient'] == fC
