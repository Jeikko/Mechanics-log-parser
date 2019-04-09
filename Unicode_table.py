#! /usr/bin/python3
# -*- coding: utf-8 -*-

def legs_to_unicode(r, b, l, t, dotted=0):
    """
    Return a box drawing Unicode character
    
    These characters have up to 4 legs, going right, bottom, left and top.
     The first 4 parameters correspond to the thickness of these legs. 0 means
     there is no leg, 1 and 2 mean the leg is thin or thick. For example,
     ┼ corresponds to (1, 1, 1, 1) and ┫ to (0, 2, 2, 2).
    The last parameter allows to draw dotted horizontal or vertical lines. It
    is then the number of interruptions in the drawing, up to 3.
    """
    if r == 0:
        if b == 0:
            if l == 0:
                if t == 0:
                    return "\u0020"
                if t == 1:
                    return "\u2575"
                if t == 2:
                    return "\u2579"
            if l == 1:
                if t == 0:
                    return "\u2574"
                if t == 1:
                    return "\u2518"
                if t == 2:
                    return "\u251a"
            if l == 2:
                if t == 0:
                    return "\u2578"
                if t == 1:
                    return "\u2519"
                if t == 2:
                    return "\u251b"
        if b == 1:
            if l == 0:
                if t == 0:
                    return "\u2577"
                if t == 1:
                    if dotted == 0:
                        return "\u2502"
                    if dotted == 1:
                        return "\u254e"
                    if dotted == 2:
                        return "\u2506"
                    if dotted == 3:
                        return "\u250a"
                if t == 2:
                    return "\u257f"
            if l == 1:
                if t == 0:
                    return "\u2510"
                if t == 1:
                    return "\u2524"
                if t == 2:
                    return "\u2526"
            if l == 2:
                if t == 0:
                    return "\u2511"
                if t == 1:
                    return "\u2525"
                if t == 2:
                    return "\u2529"
        if b == 2:
            if l == 0:
                if t == 0:
                    return "\u257b"
                if t == 1:
                    return "\u257d"
                if t == 2:
                    if dotted == 0:
                        return "\u2503"
                    if dotted == 1:
                        return "\u254f"
                    if dotted == 2:
                        return "\u2507"
                    if dotted == 3:
                        return "\u250b"
            if l == 1:
                if t == 0:
                    return "\u2512"
                if t == 1:
                    return "\u2527"
                if t == 2:
                    return "\u2528"
            if l == 2:
                if t == 0:
                    return "\u2513"
                if t == 1:
                    return "\u252a"
                if t == 2:
                    return "\u252b"
    if r == 1:
        if b == 0:
            if l == 0:
                if t == 0:
                    return "\u2576"
                if t == 1:
                    return "\u2514"
                if t == 2:
                    return "\u2516"
            if l == 1:
                if t == 0:
                    if dotted == 0:
                        return "\u2500"
                    if dotted == 1:
                        return "\u254c"
                    if dotted == 2:
                        return "\u2504"
                    if dotted == 3:
                        return "\u2508"
                if t == 1:
                    return "\u2534"
                if t == 2:
                    return "\u2538"
            if l == 2:
                if t == 0:
                    return "\u257e"
                if t == 1:
                    return "\u2535"
                if t == 2:
                    return "\u2539"
        if b == 1:
            if l == 0:
                if t == 0:
                    return "\u250c"
                if t == 1:
                    return "\u251c"
                if t == 2:
                    return "\u251e"
            if l == 1:
                if t == 0:
                    return "\u252c"
                if t == 1:
                    return "\u253c"
                if t == 2:
                    return "\u2540"
            if l == 2:
                if t == 0:
                    return "\u252d"
                if t == 1:
                    return "\u253d"
                if t == 2:
                    return "\u2543"
        if b == 2:
            if l == 0:
                if t == 0:
                    return "\u250e"
                if t == 1:
                    return "\u251f"
                if t == 2:
                    return "\u2520"
            if l == 1:
                if t == 0:
                    return "\u2530"
                if t == 1:
                    return "\u2541"
                if t == 2:
                    return "\u2542"
            if l == 2:
                if t == 0:
                    return "\u2531"
                if t == 1:
                    return "\u2545"
                if t == 2:
                    return "\u2549"
    if r == 2:
        if b == 0:
            if l == 0:
                if t == 0:
                    return "\u257a"
                if t == 1:
                    return "\u2515"
                if t == 2:
                    return "\u2517"
            if l == 1:
                if t == 0:
                    return "\u257c"
                if t == 1:
                    return "\u2536"
                if t == 2:
                    return "\u253a"
            if l == 2:
                if t == 0:
                    if dotted == 0:
                        return "\u2501"
                    if dotted == 1:
                        return "\u254d"
                    if dotted == 2:
                        return "\u2505"
                    if dotted == 3:
                        return "\u2509"
                if t == 1:
                    return "\u2537"
                if t == 2:
                    return "\u253b"
        if b == 1:
            if l == 0:
                if t == 0:
                    return "\u250d"
                if t == 1:
                    return "\u251d"
                if t == 2:
                    return "\u2521"
            if l == 1:
                if t == 0:
                    return "\u252e"
                if t == 1:
                    return "\u253e"
                if t == 2:
                    return "\u2544"
            if l == 2:
                if t == 0:
                    return "\u252f"
                if t == 1:
                    return "\u253f"
                if t == 2:
                    return "\u2547"
        if b == 2:
            if l == 0:
                if t == 0:
                    return "\u250f"
                if t == 1:
                    return "\u2522"
                if t == 2:
                    return "\u2523"
            if l == 1:
                if t == 0:
                    return "\u2532"
                if t == 1:
                    return "\u2546"
                if t == 2:
                    return "\u254a"
            if l == 2:
                if t == 0:
                    return "\u2533"
                if t == 1:
                    return "\u2548"
                if t == 2:
                    return "\u254b"
# end

def make_table(data, v_lines, h_lines, min_width=3, min_height=1):
    """
    Make a table using the unicoge box drawing characters
    
    data is a rectangular list of lists. Its elements can be anything with a
     str representation, and can include line breaks ("\n")
    v_lines and h_lines are strings corresponding to the box formatting.
     For example, "2101" means the first separator is bold (2), the second one
     thin (1), there is no third separator and the last one is thin. It has to
     match the size of data
    min_width and min_height are the minimal width and height of cells
    """
    #Nested list manipulation
    def flatten(nlist):
        return [y for x in nlist for y in x]
    def transpose(nlist):
        h = len(nlist)
        w = len(nlist[0])
        return [[nlist[i][j] for i in range(h)] for j in range(w)]
    # end

    def make_sep_line(thickness, format, position):
        # thickness is the line thickness
        # format is a string like "20010002" telling where to put vertical
         # lines. In that example:
          # -the first separator is thick (starts with a "2")
          # -the first column is 2 character wide (the two following zeroes)
          # -the second separator is thin (the following character is "1"
          # -the second column is 3 characters wide
          # -the last separator is thick
        # position is "top" if it's the first table line, "bottom" if the
         # last one, anything otherwise
        def top(elem):
            if position == "top":
                return 0
            else:
                return int(elem)
        def bottom(elem):
            if position == "bottom":
                return 0
            else:
                return int(elem)
        args = [[thickness, bottom(elem), thickness, top(elem)] for elem in format]
        if format[0] != "0":
            args[0][2] = 0
        if format[-1] != "0":
            args[-1][0] = 0
        return "".join([legs_to_unicode(*elem) for elem in args])
    # end

    def make_fill_line(format, l_strings):
        # format is a string like "20010002" telling where to put vertical
         # lines. In that example:
         # -the first separator is thick (starts with a "2")
         # -the first column is 2 character wide (the two following zeroes)
         # -the second separator is thin (the following character is "1"
         # -the second column is 3 characters wide
         # -the last separator is thick
        # l_strings is the list of strings that will be used to fill the
         # table line. Their length must match the number of zeroes in format
        res = ""
        while True:
            try:
                if format[0] == "0":
                    fill = l_strings.pop(0)
                    assert format[:len(fill)] == len(fill)*"0"
                    res += fill
                    format = format[len(fill):]
                else:
                    t, format = int(format[0]), format[1:]
                    res += legs_to_unicode(0, t, 0, t)
            except IndexError:
                return res
    # end

    # assert the data table is rectangular and that the specified formats are
    # consistent with it
    n_rows = len(data)
    assert len(h_lines) == n_rows + 1
    n_columns = len(data[0])
    assert len(v_lines) == n_columns + 1
    for line in data:
        assert len(line) == n_columns

    # compute cell sizes
    # height of a given row
    heights = [max([str(data[i][j]).count("\n")+1 for j in range(n_columns)]
                   + [min_height])
               for i in range(n_rows)]
    # if there are line breaks in the cells, create corresponding additional
    # lines. exp is for expanded
    def split_enough_lines(elem, n):
        res = str(elem).split("\n")
        while len(res) < n:
            res.append("")
        return res
    # transpose([split_enough_lines]) is a list of rows corresponding to a
    # single table row. [transpose([split_enough_lines])] is a list of list
    # of rows and has to be flattened
    data_exp = flatten([transpose([split_enough_lines(data[i][j], heights[i])
                                   for j in range(n_columns)])
                        for i in range(n_rows)])
    # actual number of rows
    n_exp_rows = len(data_exp)
    # compute cell widths
    widths = [max([len(str(data_exp[i][j])) for i in range(n_exp_rows)]
                  + [min_width])
              for j in range(n_columns)]
    # list of lines, each of them being a list of strings with the right size
    lines = [[data_exp[i][j].rjust(widths[j])
              for j in range(n_columns)]
             for i in range(n_exp_rows)]

    # compute formats
    # h_format is a string used by make_sep_line and make_fill_line. 2 means
    # thick line, 1 thin line, 0 absence of line (used by the table data)
    h_format = ""
    for sep, w in zip(v_lines, widths + [0]):
        if sep != "0":
            h_format += sep
        h_format += w*"0"
    # v_format is a string telling what is the purpose of each line. 2 means
    # thick line, 1 thin line, 0 absence of line (used by the table data)
    v_format = ""
    for sep, w in zip(h_lines, heights + [0]):
        if sep != "0":
            v_format += sep
        v_format += w*"0"

    # prepare the resulting string
    result = []
    for i, lt in enumerate(v_format):
        if lt != "0":
            if i == 0:
                pos = "top"
            elif i == len(v_format) - 1:
                pos = "bottom"
            else:
                pos = "mid"
            result.append(make_sep_line(int(lt), h_format, pos))
        else:
            fill = lines.pop(0)
            result.append(make_fill_line(h_format, fill))

    return "\n".join(result)
# end

if __name__ == "__main__":
    print(make_table([["AA", "B", "C\nD"], [1, 2, 333]],
                     "1111",
                     "111",
                     min_width=3))


