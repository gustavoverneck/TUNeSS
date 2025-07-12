import warnings

# src/header

class F77Header:
    def __init__(self,
                 parametrization: str|None = None,
                 use_magnetic_field: bool = False, 
                 use_lsv: bool = False, 
                 use_nlem: bool = False, 
                 b_gauss: float = 0.0, 
                 lsv_xi: float = 0.0, 
                 nlem_xi: float = 0.0, 
                 lsv_model: str|None = None, 
                 nlem_model: str|None = None):

        self.AVAILABLE_LSV_MODELS = ("a", "isolated")
        self.AVAILABLE_NLEM_MODELS = ("log", "born-infeld")
        self.AVAILABLE_PARAMETRIZATIONS = ("gm1", "gm3")

        self.b_gauss = b_gauss  # Magnetic field value in Gauss
        self.lsv_xi = lsv_xi    # Lorentz Symmetry Violation Background Field term
        self.nlem_xi = nlem_xi  # Nonlinear Magnetic Field term
        
        self.lsv_model = lsv_model.strip().lower() if lsv_model is not None else None
        self.nlem_model = nlem_model.strip().lower() if nlem_model is not None else None

        # Check LSV model availability
        if use_lsv and lsv_model not in self.AVAILABLE_LSV_MODELS:
            raise ValueError(f"Invalid LSV model '{lsv_model}'. Available models: {self.AVAILABLE_LSV_MODELS}")
        # Check NLEM model availability
        if use_nlem and nlem_model not in self.AVAILABLE_NLEM_MODELS:
            raise ValueError(f"Invalid NLEM model '{nlem_model}'. Available models: {self.AVAILABLE_LSV_MODELS}")
        # Check LSV usage
        if lsv_model != None and not use_lsv:
            warnings.warn("LSV model is specified but use_lsv is False. The model will be ignored.", UserWarning)
        # Check NLEM usage
        if nlem_model != None and not use_nlem:
            warnings.warn("NLEM model is specified but use_nlem is False. The model will be ignored.", UserWarning)