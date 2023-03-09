import subprocess

with open('RNASEQ.config', 'r') as file:
    tool_names = set()
    for line in file:
        if 'container =' in line:
            container_path = line.split("'")[1]
            tool_name = container_path.split('/')[-1].split('-')[0]
            tool_names.add(tool_name)
            #print(f'tool_name: {tool_name}')  # added line
    for tool_name in tool_names:
        command = ['shpc', 'show', '-f', 'quay.io/biocontainers/{}'.format(tool_name)]
        output = subprocess.check_output(command, text=True)
        expected_output = f'quay.io/biocontainers/{tool_name}'
        if output.strip() == expected_output:
            print(output.rstrip())