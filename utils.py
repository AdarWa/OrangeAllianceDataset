def get_key():
    with open('./secrets', 'r') as file:
        for line in file:
            if line.startswith('KEY='):
                return line.split('=', 1)[1].strip()
    print("No key found in secrets file")
    return None

def get_ascent_level(level):
    if level == "OBSERVATION_ZONE":
        return 1
    elif level == "NONE":
        return -1
    else:
        return int(level[-1:])