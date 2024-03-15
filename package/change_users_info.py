"""change users:info dict"""

def change_user_info(uid, new_status):
    """changing info"""
    filepath = 'src/data/users.txt'
    lines = []
    sucess_add = False
    with open(filepath) as file:
        updated_line = str(uid) + ':' + new_status + '\n'
        for line in file:
            if line.startswith(str(uid)):
                lines.append(updated_line)
                sucess_add = True
            else:
                lines.append(line)
        if not sucess_add:
            lines.append(updated_line)
    with open(filepath, 'w') as file:
        file.writelines(lines)

