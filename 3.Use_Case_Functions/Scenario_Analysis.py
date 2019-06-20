def get_sens_matrix(model,factors,date,term):

    drivers = get_factor_drivers(model,date,term)

    stdevs = get_factor_stdevs(model,date,term)

    both_moves = []
    both_results = []
    for factor in factors:
        
        if float(stdevs.loc[factor]) > 5:
            move_c = int(round(float(stdevs.loc[factor]),-1))
            intervals = int(round(move_c/2,0))
            moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)

        elif float(stdevs.loc[factor]) > 2:
            move_c = int(round(float(stdevs.loc[factor]),0))
            intervals = int(round(move_c/2,0))
            moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)
            
        elif float(stdevs.loc[factor]) < 0.05:
            move_c = round(float(stdevs.loc[factor]),2)
            intervals = int((move_c/2)*100)
            move_c = int(100*move_c)
            moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)
            moves = [round(x/100,2) for x in moves]

        else:
            move_c = round(float(stdevs.loc[factor]),1)
            intervals = int((move_c/2)*100)
            move_c = int(100*move_c)
            moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)
            
            if intervals < 10:
                moves = [round(x/100,2) for x in moves]
                
            else:
                moves = [round(x/100,1) for x in moves]

        both_moves.append(moves)
        sens = float(drivers.loc[factor])
        stdev = float(stdevs.loc[factor])
        move_results = [(move/stdev)*sens for move in moves]
        both_results.append(move_results)

    total_moves = []
    for x in both_results[0]:
        total_moves.append([x+y for y in both_results[1]])

    final_df = pandas.DataFrame(total_moves, columns=both_moves[1], index=both_moves[0])
    final_df = round(final_df,2)
    
    return final_df
