class DoubleSellar(Group):

    def setup(self):

        self.add_subsystem('g1', SubSellar(units=units, scaling=scaling))
        self.add_subsystem('g2', SubSellar(units=units, scaling=scaling))

        self.connect('g1.y2', 'g2.x')
        self.connect('g2.y2', 'g1.x')

        # Converge the outer loop with Gauss Seidel, with a looser tolerance.
        self.nonlinear_solver = NewtonSolver()
        self.linear_solver = DirectSolver()
