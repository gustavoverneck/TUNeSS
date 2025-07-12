from ..kernels.utils import F77_DEFAULT_SPACING

def toF77Float():
    pass

def to_f77_spacing(text, level=1):
    lines = text.splitlines()
    spaced_lines = [F77_DEFAULT_SPACING * level + line for line in lines]
    return "\n".join(spaced_lines)