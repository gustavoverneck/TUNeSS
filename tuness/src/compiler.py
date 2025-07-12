import subprocess
import tempfile
import importlib.util
import sys
import os

def compile_fortran_module(fortran_code: str, module_name: str = "myfortran"):
    """
    Compile a Fortran subroutine using f2py and load it as a Python module.

    Args:
        fortran_code (str): The Fortran source code as a string.
        module_name (str): The name to give the compiled Python module.

    Returns:
        module: The loaded Python module.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write the Fortran code to a file
        source_file = os.path.join(tmpdir, f"{module_name}.f90")
        with open(source_file, "w") as f:
            f.write(fortran_code)

        # Compile with f2py
        compile_cmd = [
            "f2py",
            "-c",
            "-m",
            module_name,
            source_file
        ]
        result = subprocess.run(
            compile_cmd, capture_output=True, text=True
        )
        if result.returncode != 0:
            print("Compilation failed:")
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError("Fortran compilation failed.")

        # Move compiled module to current dir to import
        # This is usually a .so file (Linux/Mac) or .pyd (Windows)
        for file in os.listdir(tmpdir):
            if file.startswith(module_name) and file.endswith(('.so', '.pyd')):
                compiled_file = os.path.join(tmpdir, file)
                target_file = os.path.join(os.getcwd(), file)
                with open(compiled_file, "rb") as src, open(target_file, "wb") as dst:
                    dst.write(src.read())
                break
        else:
            raise FileNotFoundError("Compiled module file not found.")

        # Import the compiled module
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            sys.path.append(os.getcwd())
            spec = importlib.util.find_spec(module_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module