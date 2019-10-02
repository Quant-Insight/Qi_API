#######################################################################################################################################
# 
# This function creates a table showing the % change of an asset due to various combinations of movements in two factors.
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         model - model ticker (e.g. 'AAPL')
#         factors - 2 factors you want to compare (e.g. ['Brent', 'Copper'])
#         date - date (e.g. '2019-05-17')
#         term - term (e.g. 'Long Term')
#
# Output: 
#         Dataframe representing the % change of an asset as a result of certain movements in two factors.
#               
#               * e.g.
#
#                      | -15   | -10   | -5    | 0    | 5     | 10    | 15    | 
#                | -15 | -2.57 | -2.91 | -3.26 | -3.6 | -3.95 | -4.29 | -4.64 | 
#                | -10 | -1.37 | -1.71 | -2.06 | -2.4 | -2.75 | -3.09 | -3.44 |
#                | -5  | -0.17 | -0.51 | -0.86 | -1.2 | -1.55 | -1.89 | -2.23 |
#                | 0   | 1.03  | 0.69  | 0.34  | 0.0  | -0.34 | -0.69 | -1.03 |
#                | 5   | 2.23  | 1.89  | 1.55  | 1.2  | 0.86  | 0.51  | 0.17  | 
#                | 10  | 3.44  | 3.09  | 2.75  | 2.4  | 2.06  | 1.71  | 1.37  |
#                | 15  | 4.64  | 4.29  | 3.95  | 3.6  | 3.26  | 2.91  | 2.57  |
#
#######################################################################################################################################



def get_sens_matrix(model,factors,date,term):    
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:

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
