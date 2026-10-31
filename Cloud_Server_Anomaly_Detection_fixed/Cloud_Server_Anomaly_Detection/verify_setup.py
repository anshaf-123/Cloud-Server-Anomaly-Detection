import sys
import subprocess
import os
import shutil
from pathlib import Path

# ANSI colors for nice terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(title):
    print("\n" + "=" * 60)
    print(f"{BOLD}{title}{RESET}")
    print("=" * 60)

def check_python():
    print_header("1. Python Environment Check")
    version = sys.version.split()[0]
    expected_major_minor = "3.11"
    
    status = GREEN + "OK" + RESET
    if not version.startswith(expected_major_minor):
        status = YELLOW + f"Warning (Recommended {expected_major_minor}.x, current version is {version})" + RESET
    
    print(f"Python Version: {version} -> {status}")
    print(f"Executable: {sys.executable}")
    
    # Check Conda Environment
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "None")
    print(f"Active Conda Env: {conda_env} -> ", end="")
    if conda_env == "cloud_anomaly":
        print(GREEN + "OK" + RESET)
    else:
        print(YELLOW + "Warning (Recommended to run inside 'cloud_anomaly' environment)" + RESET)

def check_dependencies():
    print_header("2. Python Packages Dependency Check")
    dependencies = [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "sklearn",
        "scipy",
        "joblib",
        "plotly",
        "mysql.connector",
        "pyspark",
        "dotenv",
        "findspark",
        "shap",
        "statsmodels"
    ]
    
    missing = []
    for dep in dependencies:
        try:
            if dep == "sklearn":
                import sklearn
            elif dep == "mysql.connector":
                import mysql.connector
            elif dep == "dotenv":
                import dotenv
            else:
                __import__(dep)
            print(f"  [+] {dep:<25} : {GREEN}Installed{RESET}")
        except ImportError:
            print(f"  [-] {dep:<25} : {RED}MISSING{RESET}")
            missing.append(dep)
            
    return missing

def check_external_runtimes():
    print_header("3. External Runtimes Check (Java & R)")
    
    # Check Java (required for PySpark)
    java_path = shutil.which("java")
    if java_path:
        try:
            result = subprocess.run(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            java_ver = result.stderr.split("\n")[0]
            print(f"  [+] Java (PySpark)      : {GREEN}Found{RESET} ({java_ver})")
        except Exception as e:
            print(f"  [-] Java (PySpark)      : {YELLOW}Found but failed to execute{RESET} ({str(e)})")
    else:
        # Check standard Java environment variables
        java_home = os.environ.get("JAVA_HOME")
        if java_home and os.path.exists(os.path.join(java_home, "bin", "java.exe")):
            print(f"  [+] Java (PySpark)      : {GREEN}Found via JAVA_HOME{RESET} ({java_home})")
        else:
            print(f"  [-] Java (PySpark)      : {RED}NOT FOUND in PATH or JAVA_HOME{RESET}")
            print("      -> Action Required: Install Java JDK 11 or 8 to run PySpark.")

    # Check R (required for statistical models)
    r_path = shutil.which("Rscript")
    if r_path:
        try:
            result = subprocess.run(["Rscript", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            r_ver = result.stderr.strip() or result.stdout.strip()
            print(f"  [+] R Runtime           : {GREEN}Found{RESET} ({r_ver})")
        except Exception as e:
            print(f"  [-] R Runtime           : {YELLOW}Found but failed to execute{RESET} ({str(e)})")
    else:
        # Check standard installation path
        r_common = glob_r_installations()
        if r_common:
            print(f"  [+] R Runtime           : {GREEN}Found in default path{RESET} ({r_common[0]})")
            print("      -> Note: Please add this to your PATH environment variable.")
        else:
            print(f"  [-] R Runtime           : {RED}NOT FOUND{RESET}")
            print("      -> Action Required: Install R (https://cran.r-project.org/) to run R models.")

def glob_r_installations():
    import glob
    return glob.glob("C:/Program Files/R/R-*/bin/x64/Rscript.exe")

def check_local_services():
    print_header("4. Local Web & DB Services Check (XAMPP / MySQL)")
    
    # Check XAMPP directory
    xampp_path = Path("C:/xampp")
    if xampp_path.exists():
        print(f"  [+] XAMPP installation  : {GREEN}Found at C:\\xampp{RESET}")
    else:
        print(f"  [-] XAMPP installation  : {YELLOW}Not found at C:\\xampp{RESET} (Check WAMP/XAMPP custom location)")

    # Check if MySQL Port (3306) is open / active
    import socket
    mysql_active = False
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect(("127.0.0.1", 3306))
        s.close()
        mysql_active = True
        print(f"  [+] MySQL Port (3306)   : {GREEN}Active / Listening{RESET}")
    except Exception:
        print(f"  [-] MySQL Port (3306)   : {RED}Offline / Closed{RESET}")
        print("      -> Action Required: Start MySQL inside your XAMPP Control Panel.")

    if mysql_active:
        # Test connection
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                password=""
            )
            print(f"  [+] MySQL Connection    : {GREEN}Successful (Auth OK){RESET}")
            conn.close()
        except ImportError:
            pass
        except Exception as e:
            print(f"  [-] MySQL Connection    : {YELLOW}Failed to authenticate{RESET} ({str(e)})")

def main():
    print("=" * 60)
    print("  CLOUD SERVER ANOMALY DETECTION SYSTEM SETUP VERIFIER")
    print("=" * 60)
    
    check_python()
    missing_packages = check_dependencies()
    check_external_runtimes()
    check_local_services()
    
    print_header("Summary & Recommendations")
    if missing_packages:
        print(f"{RED}Missing Python packages:{RESET} {', '.join(missing_packages)}")
        print(f"Please run: {BOLD}pip install -r requirements.txt{RESET} within the 'cloud_anomaly' environment.")
    else:
        print(f"{GREEN}All required Python packages are installed!{RESET}")
        
    print("\nNext step: Set up any missing external runtimes (Java, R) and start the XAMPP services.")
    print("=" * 60)

if __name__ == "__main__":
    main()
