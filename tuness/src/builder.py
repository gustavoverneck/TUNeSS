# src/builder

import warnings
from ..kernels.utils import F77_PROGRAM_END, F77_PROGRAM_START, F77_DEFAULT_SPACING
from ..kernels.parametrizations import GM1_PARAMETRIZATION, GM3_PARAMETRIZATION
from ..utils.converters import to_f77_spacing

AVAILABLE_LSV_MODELS = ("a", "isolated")
AVAILABLE_NLEM_MODELS = ("log", "born-infeld")
AVAILABLE_PARAMETRIZATIONS = ("gm1", "gm3")

def build_kernel(parametrization: str|None = None, 
                 use_hyperons: bool = False,
                 use_magnetic: bool = False, 
                 use_lsv: bool = False, 
                 use_nlem: bool = False, 
                 b_gauss: float = 0.0, 
                 lsv_xi: float = 0.0, 
                 nlem_xi: float = 0.0, 
                 lsv_model: str|None = None, 
                 nlem_model: str|None = None,
                 npoints: int = 1000,
                 ):
    # Check Parametrization
    if parametrization not in AVAILABLE_PARAMETRIZATIONS:
        raise ValueError(f"Invalid Parametrization model '{parametrization}'. Available models: {AVAILABLE_PARAMETRIZATIONS}")
    # Check LSV model availability
    if use_lsv and lsv_model not in AVAILABLE_LSV_MODELS:
        raise ValueError(f"Invalid LSV model '{lsv_model}'. Available models: {AVAILABLE_LSV_MODELS}")
    # Check NLEM model availability
    if use_nlem and nlem_model not in AVAILABLE_NLEM_MODELS:
        raise ValueError(f"Invalid NLEM model '{nlem_model}'. Available models: {AVAILABLE_NLEM_MODELS}")
    # Check LSV usage
    if lsv_model is not None and not use_lsv:
        warnings.warn("LSV model is specified but use_lsv is False. The model will be ignored.", UserWarning)
    # Check NLEM usage
    if nlem_model is not None and not use_nlem:
        warnings.warn("NLEM model is specified but use_nlem is False. The model will be ignored.", UserWarning)
    # Check Magnetic Field usage
    if use_magnetic and (b_gauss == 0.0):
        warnings.warn("'use_magnetic_field' is specified but 'b_gauss' is '0.0'.", UserWarning)
    # Check LSV usage
    if use_lsv and lsv_model is None:
        warnings.warn("use_lsv is True but no lsv_model is specified.", UserWarning)
    # Check NLEM usage
    if use_nlem and nlem_model is None:
        warnings.warn("use_nlem is True but no nlem_model is specified.", UserWarning)   
    
    # Create raw string to store f77 code
    code = r""""""

    # Add f77 program start
    code += F77_PROGRAM_START + "\n"
    
    # Add f77 implicit types
    code += get_f77_implicit() + "\n"
    
    # Add variables declaration
    
    # Add f77 program end
    code += F77_PROGRAM_END

    return code

def get_f77_implicit():
    return "      implicit double precision(a-h,k-z)"

def get_f77_parametrization(parametrization : str):
    match parametrization:
        case "gm1":
            return GM1_PARAMETRIZATION
        case "gm3":
            return GM3_PARAMETRIZATION
        case _:
            raise ValueError(f"Unknown parametrization '{parametrization}'. Available: {AVAILABLE_PARAMETRIZATIONS}")

def get_f77_variables(use_magnetic, use_lsv, use_nlem):
    pass

def get_f77_b_gauss(b_gauss):
    return 

def get_f77_lsv_xi(xi):
    return

def get_f77_nlem_xi(xi):
    return

def get_f77_tov(xi):
    return