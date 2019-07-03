import sys

command_line_list = sys.argv[1:]
def get_name(my_list):
    analysis = ""
    command_to_name = {}
    command_to_name['-e'] = "+Expression"
    command_to_name['-c'] = "+Clinical"
    command_to_name['-n'] = "+CNV"
    command_to_name['-d'] = "+DNA_Methylation"
    command_to_name['-p'] = "+RPPA"
    command_to_name['-s'] = "+SM"
    command_to_name['-m'] = "+miRNA"
    combo_list = [x for x in my_list if x.startswith('-')]
    if len(combo_list) == 0:
        analysis = "no_combination"
    else:
        for x in combo_list:
            analysis += command_to_name[x]
    return analysis

if __name__ == "__main__":
    print(get_name(command_line_list))