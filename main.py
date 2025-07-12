from tuness import TUNeSS, build

# Initialize F77 Kernel
kernel = build(parametrization = None,
                 use_magnetic = False, 
                 use_lsv = False, 
                 use_nlem = False, 
                 b_gauss = 0.0, 
                 lsv_xi = 0.0, 
                 nlem_xi = 0.0, 
                 lsv_model = None, 
                 nlem_model = None,
                 )

# Initialize TUNeSS Solver
solver = TUNeSS()
res = solver.run()