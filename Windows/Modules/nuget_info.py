import subprocess
import json

def list_installed_packages():
    try:
        result = subprocess.run(["nuget", "list", "-AllVersions", "-Prerelease", "-Source", "https://api.nuget.org/v3/index.json", "--outputformat", "json"], capture_output=True, text=True, check=True)
        packages_data = json.loads(result.stdout)
        return packages_data
    except Exception as e:
        return {"error": "NuGet command failed", "message": e}

if __name__ == "__main__":
    result = list_installed_packages()
    print(result)
    #print(json.dumps(result, indent=2))
