import os
import pynumwrap as nw
try:
    import tisutil as tu
except:
    tu = None

num_field_chars=20

def _check_line_length(line, lin_num, num_elements):
    if len(line)!=num_elements*num_field_chars+1 and len(line)!=num_elements*num_field_chars+2: #Depending on new line sequence
        raise Exception("Line " + str(lin_num) + " bad: " + str(line) + "  Len: " + str(len(line)) + "  Elements: " + str(num_elements))

def _read_lines(kmats, ene, line, num_elements, c_element):
    for i in range(num_elements):
        indices = _get_indices(c_element)
        kmats[ene][indices[0],indices[1]] = _num(line[i*20:(i+1)*20])
        c_element += 1
    return c_element

def _get_indices(c_element):
    rows = 1
    cnt = 0
    while cnt < c_element:
        cnt += rows
        rows += 1
    ri = rows-2
    p_sum = _a_sum(rows-2)
    ci = c_element - p_sum - 1
    return (ri, ci)

def _a_sum(n):
    return n * (n+1) / 2

def _num(string):
    return float(string.replace("D", "E").replace(" ", ""))

def _flip_copy_diag(kmats):
    for ene in kmats:
        kmat = kmats[ene]
        num_channels = nw.shape(kmat)[0]
        num_unique_elements = _a_sum(num_channels) 
        c_element = 1
        for i in range(num_unique_elements):
            indices = _get_indices(c_element)
            c_element += 1
            if indices[0] != indices[1]:
                kmat[indices[1],indices[0]] = kmat[indices[0],indices[1]]

def _get_source_str(file_path, source_str):
    if source_str is not None:
        return source_str
    # If not specified just return the filename
    return os.path.splitext(file_path)[0].split(os.sep)[-1]

########################################################################   
######################### Public Interface #############################
########################################################################

def read_Kmats(file_path, asymcalc=None, source_str=None):
    kmats = {}
    with open(file_path, 'rb') as file:
        lin_num = 0
        for _ in range(0,5):
            lin_num += 1
            file.readline()
        ene = None
        num_complete_lines_per_mat = 0
        num_rem_elements = 0
        o_chan_desc = []
        last_num_channels = 0
        for line in file:
            lin_num += 1
            nums = filter(lambda x: x!="", line.split())
            if nums[0].find(".") == -1:
                num_channels = int(nums[0])
                if last_num_channels != num_channels:
                    last_num_channels = num_channels
                    if len(o_chan_desc) == 0:
                        o_chan_desc.append([num_channels,[0,1]])
                    else:
                        new_start_ind = o_chan_desc[-1][1][1]
                        new_end_ind = new_start_ind + 1
                        o_chan_desc.append([num_channels,
                                            [new_start_ind,new_end_ind]])
                else:
                    o_chan_desc[-1][1][1] += 1
                num_unique_elements = _a_sum(num_channels)
                num_complete_lines_per_mat = num_unique_elements / 4
                num_rem_elements = num_unique_elements % 4
                line_i = 0
                ene = _num(nums[3])
                kmats[ene] = nw.zero_matrix(num_channels)
                c_element = 1
            else:
                if line_i < num_complete_lines_per_mat:
                    _check_line_length(line, lin_num, 4)
                    c_element = _read_lines(kmats, ene, line, 4, c_element)
                elif num_rem_elements > 0:
                    _check_line_length(line, lin_num, num_rem_elements)
                    c_element = _read_lines(kmats, ene, line, num_rem_elements, c_element)
                line_i += 1
    _flip_copy_diag(kmats)
    if tu is not None and asymcalc is not None:
        assert asymcalc.get_units() == tu.rydbergs
        ret = tu.dKmat(kmats, asymcalc, _get_source_str(file_path,source_str))
    else:
        ret = kmats
    return ret, o_chan_desc

def use_python_types(dps=nw.dps_default_python):
    nw.use_python_types(dps)

def use_mpmath_types(dps=nw.dps_default_mpmath):
    nw.use_mpmath_types(dps)

def set_type_mode(mode, dps=None):
    nw.set_type_mode(mode, dps)
