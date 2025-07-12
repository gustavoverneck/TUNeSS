# src/builder

import warnings
from ..kernels.utils import F77_PROGRAM_END, F77_PROGRAM_START, F77_DEFAULT_SPACING
from ..utils.converters import to_f77_spacing

class F77Builder:
    def __init__(self,
                 parametrization: str|None = None,
                 use_magnetic: bool = False, 
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
        
        # Conditionals for custom kernels
        self.use_magnetic = use_magnetic
        self.use_lsv = use_lsv
        self.use_nlem = use_nlem

        self.b_gauss = b_gauss  # Magnetic field value in Gauss
        self.lsv_xi = lsv_xi    # Lorentz Symmetry Violation Background Field term
        self.nlem_xi = nlem_xi  # Nonlinear Magnetic Field term
        
        self.parametrization = parametrization.strip().lower() if parametrization is not None else None
        self.lsv_model = lsv_model.strip().lower() if lsv_model is not None else None
        self.nlem_model = nlem_model.strip().lower() if nlem_model is not None else None
        
        # Define code variable to be build
        self.code = r""""""
    
    def check_and_warn(self):
        # Check Parametrization
        if self.parametrization not in self.AVAILABLE_PARAMETRIZATIONS:
            raise ValueError(f"Invalid Parametrization model '{self.parametrization}'. Available models: {self.AVAILABLE_PARAMETRIZATIONS}")
        # Check LSV model availability
        if self.use_lsv and self.lsv_model not in self.AVAILABLE_LSV_MODELS:
            raise ValueError(f"Invalid LSV model '{self.lsv_model}'. Available models: {self.AVAILABLE_LSV_MODELS}")
        # Check NLEM model availability
        if self.use_nlem and self.nlem_model not in self.AVAILABLE_NLEM_MODELS:
            raise ValueError(f"Invalid NLEM model '{self.nlem_model}'. Available models: {self.AVAILABLE_LSV_MODELS}")
        # Check LSV usage
        if self.lsv_model != None and not self.use_lsv:
            warnings.warn("LSV model is specified but use_lsv is False. The model will be ignored.", UserWarning)
        # Check NLEM usage
        if self.nlem_model != None and not self.use_nlem:
            warnings.warn("NLEM model is specified but use_nlem is False. The model will be ignored.", UserWarning)
        # Check Magnetic Field usage
        if self.use_magnetic_field and (self.b_gauss == 0.0):
            warnings.warn("'use_magnetic_field' is specified but 'b_gauss' is '0.0'.", UserWarning)
    
    def write_f77_start(self):
        self.code += F77_PROGRAM_START + "\n"
        
    def write_f77_end(self):
        self.code += F77_PROGRAM_END + "\n"
    
    def run(self):
        self.check_and_warn()