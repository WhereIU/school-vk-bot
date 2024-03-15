"""get cmds:msgs dict"""
def add_msgs():
    """adding in dict"""
    msgs_path = 'src/data/msgs.txt'
    msgs_file = open(msgs_path, encoding='utf-8')
    msgs_dict = {}
    key = ''
    values = []
    while True:
        current_line = msgs_file.readline().strip()
        if len(current_line) == 0:
            msgs_dict[key] = values
            msgs_file.close()
            return msgs_dict

        if current_line[-1] == '`':
            if key != '' and values != []:
                msgs_dict[key] = values
                values = []
            key = current_line[: -1]
        else:
            values.append(current_line)

msgs = add_msgs()
