import re
import subprocess

with open("results/pipeline_info/software_versions.yml", "r") as f:
    lines = f.readlines()
    for line in lines:
        match = re.match(r"^(\b\w+\b):\s*\d+\.\d+\.\d+$", line.strip())
        if match:
            toolname = match.group(1)
            if not toolname.startswith(('python-', 'perl-')):
                command = f"shpc show --versions -f quay.io/biocontainers/{toolname}"
                output = subprocess.check_output(command, shell=True, text=True).strip()
                versions = []
                for tool in output.split('\n'):
                    if not tool.startswith(('quay.io/biocontainers/python-', 'quay.io/biocontainers/python_', 'quay.io/biocontainers/pythonpy', 'quay.io/biocontainers/pythonnet', 'quay.io/biocontainers/perl-')):
                        versions.append(tool.strip())
                if versions:
                    unique_versions = list(set(versions))
                    print(f"{toolname}: {', '.join(unique_versions)}")
