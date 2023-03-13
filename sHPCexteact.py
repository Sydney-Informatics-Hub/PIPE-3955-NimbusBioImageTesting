import re
import subprocess

with open("results/pipeline_info/software_versions.yml", "r") as f:
    lines = f.readlines()
    results = []
    for line in lines:
        match = re.match(r"^(\b\w+-?\w*\b|\b\w+\s\w+\b):\s*(['\"]?[\d.]+[a-z-]*['\"]?)$", line.strip())
        if match:
            toolname = match.group(1)
            if not toolname.startswith(('python-', 'perl-')):
                command = f"shpc show --versions -f quay.io/biocontainers/{toolname}"
                output = subprocess.check_output(command, shell=True, text=True).strip()
                versions = set()
                for tool in output.split('\n'):
                    if not tool.startswith(('quay.io/biocontainers/star-', 'quay.io/biocontainers/python-', 'quay.io/biocontainers/python_','quay.io/biocontainers/perl-')):
                        versions.add(tool.strip())
                if versions:
                    version_str = ', '.join(versions)
                    # Get the version of the tool from the YAML file
                    version_match = re.search(rf"{toolname}:\s*([\d\.]+)", "".join(lines))
                    version = version_match.group(1) if version_match else None
                    # Append the tool name and its version to the results list
                    results.append(f"{toolname}/{version}: {version_str}")
    # Sort and deduplicate the results
    results = sorted(set(results))
    for result in results:
        print(result)