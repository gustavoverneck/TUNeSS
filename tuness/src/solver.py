from .builder import build_kernel

class TUNeSS:
    def __init__(self):
        pass
    
    def run(self, kernels):
        # Handle both single kernel and list of kernels
        if isinstance(kernels, str):
            # Single kernel case
            kernel_list = [kernels]
        elif isinstance(kernels, list):
            # Multiple kernels case
            kernel_list = kernels
        else:
            raise TypeError("kernels must be either a raw string instance or a list of raw strings instances")
        
        # Example usage of build_kernel on each kernel in the list
        built_kernels = [build_kernel(kernel) for kernel in kernel_list]
        return built_kernels