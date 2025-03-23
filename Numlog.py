def solution(numLog):
    log_dict = dict(zip(['w','s','a','d'], [1,-1,-10,10]))
    answer = ''
    for i in range(len(log_dict)-1):
        log = log_dict[i+1] - log_dict[i]
        answer += log_dict[log]

    return answer