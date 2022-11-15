def print_dict(dict,filler = "-",headers = ["key","value"]):
    dict_keys = sorted([x for x in dict.keys()])
    final_output = " ".join([str(headers[0]), str(filler), str(headers[1])])
    for key in dict_keys:
        final_output += " ".join(["\n", str(key), str(filler), str(dict[key])])
    return final_output

mem_l_dict ={
    0 : [0,1],
    1 : [20,3],
    2 : [40,5],
    3 : [60,7]
}


print(print_dict(mem_l_dict,filler="for",headers=["option",["fee","max_limit_to borrow"]]))