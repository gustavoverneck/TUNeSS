from tuness import TUNeSS, build_kernel

# Initialize F77 Kernel
kernel = build_kernel(parametrization = "gm1",
                 use_magnetic = False, 
                 use_lsv = False, 
                 use_nlem = False, 
                 b_gauss = 0.0, 
                 lsv_xi = 0.0, 
                 nlem_xi = 0.0, 
                 lsv_model = None, 
                 nlem_model = None,
                 )

print(kernel)

# # Initialize TUNeSS Solver
# solver = TUNeSS()

# res = solver.run()