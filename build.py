import subprocess
import sys
import os

def run_pyinstaller(script_path, onefile=True, windowed=True, icon_path=None, assets_path=None):
    # Convert paths to absolute paths
    script_path = os.path.abspath(script_path)
    if icon_path:
        icon_path = os.path.abspath(icon_path)
    if assets_path:
        assets_path = os.path.abspath(assets_path)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        script_path
    ]

    if onefile:
        cmd.append("--onefile")
    if windowed:
        cmd.append("--windowed")
    if icon_path:
        cmd += ["--icon", icon_path]

    if assets_path:
        sep = ";" if os.name == "nt" else ":"
        add_data_option = f"{assets_path}{sep}assets"
        cmd += ["--add-data", add_data_option]

    print("Running PyInstaller with command:")
    print(" ".join(cmd))

    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("PyInstaller failed.")
        sys.exit(result.returncode)
    else:
        print("Build completed successfully!")

if __name__ == "__main__":
    main_script = "main.py"
    icon = "src/assets/icon.ico"
    assets = "src/assets"

    run_pyinstaller(main_script, onefile=True, windowed=True, icon_path=icon, assets_path=assets)
