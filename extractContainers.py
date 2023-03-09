with open('RNASEQ.config', 'r') as file:
    tool_names = set()
    for line in file:
        if 'container =' in line:
            container_path = line.split("'")[1]
            tool_name = container_path.split('/')[-1].split('-')[0]
            tool_names.add(tool_name)
    for tool_name in tool_names:
        print(tool_name)