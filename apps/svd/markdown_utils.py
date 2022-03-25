def generate_markdown_header(dict):
    header = '|'
    for key in dict:
        header  = header + str(key)+ "|"
    return header

def generate_markdown_line_sep(dict):
    header = '|'
    for key in dict:
        header  = header + "--|"
    return header

def generate_markdown_line(dict):
    header = '|'
    for key in dict:
        header  = header + str(dict[key])+ "|"
    return header

def generate_markdown_from_list(list):
    ## add header
    header = '|'
    for c in list:
        header = header + str(c) + '|'
    header = header + "\n"
    return header

def generate_sep(n):
    header = '|'
    for c in range(n):
        header = header + '--' + '|'
    header = header + '\n'
    return header

def df_to_markdown(df):
    ## add header
    header = generate_markdown_from_list(df.columns)
    header = header+ generate_sep(len(df.columns))
    for i in range(df.shape[0]):
        header = header+generate_markdown_from_list(df.iloc[i,:])
    return header
