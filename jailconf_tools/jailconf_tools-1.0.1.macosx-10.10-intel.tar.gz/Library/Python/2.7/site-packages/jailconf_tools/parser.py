import re

NO_MODE_CHARS = "[a-zA-Z0-9_\.,\"'\{\};=+/\$-]"

NO_MODE = 0
S_STRING_MODE = 1
D_STRING_MODE = 2


def get_jails_config(filename='jail.conf'):
    """Parse file `filename` and get it content as a dict

    :param filename: path to jail.conf file
    :type filename: str"""

    cfg = []
    try:
        with open(filename, 'r') as f:
            cfg_content = _remove_comments(f.read())

            curr_c = 0
            cfg_nb_c = len(cfg_content)

            # parse all file content
            while curr_c < cfg_nb_c:
                # by default, parameters are in global jail definition
                curr_c, data = _parse_section_content(jail_name='global',
                                                      start_pos=curr_c,
                                                      cfg=cfg_content)
                if data is not None:
                    if isinstance(data, list):
                        for _ in data:
                            cfg.append(_)
                    else:
                        cfg.append(data)

                curr_c += 1

            jailscfg = {}
            for jailname, p_name, p_value in cfg:
                if jailname not in jailscfg:
                    jailscfg[jailname] = []
                jailscfg[jailname].append((p_name, p_value))
            cfg = jailscfg
    except Exception as e:
        print(str(e))
    finally:
        return cfg


def _remove_comments(cfg):
    """Remove comments from `cfg` string

    :param cfg: string containing comments
    :type cfg: str"""

    cfg_structure = ""
    curr_mode = NO_MODE
    curr_c = 0
    cfg_nb_c = len(cfg)
    while curr_c < cfg_nb_c:
        if curr_mode == NO_MODE:
            # inline comment
            if cfg[curr_c] == '#' or cfg[curr_c:curr_c+2] == "//":
                while cfg[curr_c] != '\n':
                    curr_c += 1
                curr_c += 1  # remove trailing newline character
            # multilines comment
            elif cfg[curr_c:curr_c+2] == "/*":
                while cfg[curr_c:curr_c+2] != "*/":
                    curr_c += 1
                curr_c += 2  # remove "*/" trailing characters
            # simple line / character
            else:
                # enter in string mode -> keep all characters
                if cfg[curr_c] == '"':
                    curr_mode = D_STRING_MODE

                cfg_structure += cfg[curr_c]
                curr_c += 1
        else:
            cfg_structure += cfg[curr_c]

            # quit string mode if it's a '"' character and if it's not escaped
            if cfg[curr_c] == '"' and cfg[curr_c-1] != '\\':
                curr_mode = NO_MODE

            curr_c += 1

    return cfg_structure


def _get_param(start_pos, cfg):
    """Get parameter name which ends at character `start_pos`

    :param start_pos:
    :type start_pos: interger
    :param cfg:
    :type cfg: str"""

    mode = 0
    val = ""

    curr_c = start_pos - 1

    if cfg[curr_c] == '+':
        curr_c -= 1

    # Remove trailing whitespaces
    while len(cfg[curr_c].strip()) == 0:
        curr_c -= 1

    while curr_c >= 0:
        if (mode == NO_MODE
                and (len(cfg[curr_c].strip()) == 0 or cfg[curr_c] == ';')):
            break
        else:
            val += cfg[curr_c]
            curr_c -= 1

    return (start_pos, val[::-1])


def _get_value(start_pos, cfg):
    """Get value which starts at character `start_pos` and end at the ';'
    character

    :param start_pos:
    :type start_pos: interger
    :param cfg:
    :type cfg: str"""

    mode = 0
    val = ""

    curr_c = start_pos + 1
    # Remove begining whitespaces
    while len(cfg[curr_c].strip()) == 0:
        curr_c += 1

    while True:
        # each instruction ends with a ';'
        if mode == NO_MODE and cfg[curr_c] == ';':
            # end of an instruction, exit loop without keeping end of
            # instruction character
            break
        else:
            _mode, _val = _get_value_by_mode(mode, cfg, curr_c)
            if _mode is not None and _val is not None:
                if _val != '\\' and cfg[curr_c+1] != '\n':
                    val += _val
                    mode = _mode
                # \ is the last character on the line, so escape it and the
                # new line character too
                else:
                    curr_c += 1
            curr_c += 1

    for quote_c in ['"', "'"]:
        if val.startswith(quote_c) and val.endswith(quote_c):
            val = val[1:len(val)-1]
            break

    return (curr_c, val)


def _get_value_by_mode(mode, cfg, pos):
    # enter or exit string mode
    if cfg[pos] in ['"', "'"]:
        if mode == NO_MODE and cfg[pos] == '"':
            mode = D_STRING_MODE
        elif mode == NO_MODE and cfg[pos] == "'":
            mode = S_STRING_MODE
        elif (mode == D_STRING_MODE and cfg[pos] == '"'
                and cfg[pos-1] != '\\'):
            mode = NO_MODE
        elif (mode == S_STRING_MODE and cfg[pos] == "'"
                and cfg[pos-1] != '\\'):
            mode = NO_MODE

    if (mode in [S_STRING_MODE, D_STRING_MODE] or
            (mode == NO_MODE and re.match(NO_MODE_CHARS, cfg[pos]))):
        if cfg[pos] != '\\':
            return (mode, cfg[pos])

    return (None, None)


def _parse_jail_definition(start_pos, cfg):
    mode = 0
    val = None

    _, jailname = _get_param(start_pos, cfg)

    jaildef = ""
    curr_c = start_pos + 1
    # get the content of the jail definition part
    while True:
        # a jail definition ands with a '}'
        if mode == NO_MODE and cfg[curr_c] == '}':
            break
        else:
            _mode, _val = _get_value_by_mode(mode, cfg, curr_c)
            if _mode is not None and _val is not None:
                jaildef += _val
                mode = _mode
            curr_c += 1

    _curr_c = 0
    jaildef_nb_c = len(jaildef)

    # parse the content of jail definition part
    while _curr_c < jaildef_nb_c:
        _curr_c, data = _parse_section_content(jail_name=jailname,
                                               start_pos=_curr_c,
                                               cfg=jaildef)

        if data is not None:
            if val is None:
                val = []
            val.append(data)

        _curr_c += 1

    return (curr_c, val)


def _parse_section_content(jail_name, start_pos, cfg):
    val = None

    curr_c = start_pos
    # It seems to be a 'param = "value";' component
    if cfg[curr_c] == '=':
        _, param_name = _get_param(curr_c, cfg)
        curr_c, param_value = _get_value(curr_c, cfg)

        val = (jail_name, param_name, param_value)
    # begining of a jail definition
    elif cfg[curr_c] == '{':
        curr_c, val = _parse_jail_definition(curr_c, cfg)
    # it seems to be a boolean param
    elif cfg[curr_c] == ';':
        _, param_name = _get_param(curr_c, cfg)

        val = (jail_name, param_name, None)

    return (curr_c, val)
