# src/header

class F77Header:
    def __init__(self, b_gauss: float = 0.0, lsv_xi: float = 0.0, nlem_xi: float = 0.0):
        self.b_gauss = b_gauss  # Magnetic field value in Gauss
        self.lsv_xi = lsv_xi
        self.nlem_xi = nlem_xi
        