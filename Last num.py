def solution(num_list):
    if len(num_list) < 2:
        return num_list

    last, twolast = num_list[-1], num_list[-2]

    if last > twolast :
        num_list.append(last - twolast)
    else :
        num_list.append(last * 2)
    return num_list

