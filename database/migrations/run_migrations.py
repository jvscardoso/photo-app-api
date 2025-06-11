import subprocess
import os

BASE_DIR = os.path.dirname(__file__)

def run_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    print(f"Executing {script_name}...")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to execute {script_name}:\n{result.stderr}")
        return False
    print(f"{script_name}:\n{result.stdout} executed successfully")
    return True

def main():
    scripts = [
        "users_migration.py",
        "photos_migration.py"
    ]
    
    for script in scripts:
        success = run_script(script)
        if not success:
            print("Aborting migrations")
            break

if __name__ == "__main__":
    main()
