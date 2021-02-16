# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 11:59:44 2021

@author: rando
"""


### Craps Model: Pass line; Field; Place 6, 8 ###



from random import randint
import pandas as pd
import matplotlib.pyplot as plt

come_out = 'OFF'
point = 0
bet = 30
funds = 10000
roll_catalog = []
bank_account = [funds]
payout = 0
status = 'Start'

place_68_payout = 7/6
place_59_payout = 7/5
place_410_payout = 9/5
field_payout = 1
field_2_payout = 2
field_12_payout = 3

formatted_payout = '${:,.2f}'.format(payout)
formatted_funds = '${:,.2f}'.format(funds)

print('Funds: ' + str(formatted_funds))

#%%
###Game flow script###

#run the model 5,000 times
for x in range (0, 5000):
    
    #initialize pass line bet
    if status == 'Play':
        funds = funds
    else:
        funds = funds - bet
    
    #roll the dice
    die_1 = randint(1, 6)
    die_2 = randint(1, 6)
    dice_roll = die_1 + die_2

    #roll a 7 or 11 on first roll; pass line bet hits
    if come_out == 'OFF' and (dice_roll == 7 or dice_roll == 11):
        point = 0
        status = 'Winner!'
    #roll a 2, 3, or 12 on first roll - craps
    elif come_out == 'OFF' and (dice_roll == 2 or dice_roll == 3 or dice_roll == 12):
        point = 0
        status = 'Craps'
    #roll anything else, set the point
    elif come_out == 'OFF' and (dice_roll != [2, 3, 7, 11, 12]):
        point = dice_roll
        come_out = 'ON'
        status = 'Play'
    #roll the point - pass line hits
    elif dice_roll == point:
        point = 0
        come_out = 'OFF'
        status = 'Win!'
    #roll a 7 after point is established - lose all bets
    elif dice_roll == 7:
        point = 0
        come_out = 'OFF'
        status = 'Lose'
    #neither point or 7 hits; keep rolling with same point
    else:
        point = point
    
    #record each dice roll for future analysis
    roll_catalog.append(dice_roll)
        

    ###################################################
    ###Bet payouts###
    
    #before point is established:
    if come_out == 'OFF':
        #roll 7 or 11
        if status == 'Winner!':
            #pass line payout + recoup initial bet
            payout = bet * 2
            funds = funds + payout
            table_bet = 0
        #roll 2, 3, or 12
        elif status == 'Craps':
            #lose pass line bet
            payout = 0
            funds = funds + payout
            table_bet = 0
        #win by hitting point
        elif status == 'Win!':
            #if point is the field, we get all our bets back (table_bet)
            #we win field payout and pass line payout
            if (dice_roll == 3 or dice_roll == 4 or dice_roll == 9 or dice_roll == 10 or dice_roll == 11):
                payout = table_bet + bet * 2
            #if point is not the field, we get our place and pass line bets back
            #we win pass line, lose field
            else:
                payout = table_bet
            table_bet = 0
            funds = funds + payout
        #set the point  
        else:
            #no payout or loss yet, play on;
            #if 7, all bets lose
            payout = 0
            funds = funds + payout
    #first role (establish point)
    elif point == dice_roll:
        #point is 6 or 8 - we only do a place bet on one of them & the field
        if dice_roll == 6 or dice_roll == 8:
            payout = 0
            funds = funds - bet * 2
            table_bet = bet * 3
        #point is not 6 or 8 - we do a place bet on both & the field
        else:
            payout = 0
            funds = funds - bet * 3
            table_bet = bet * 4
    #non-winning rolls after point is established:
    else:
        #roll 6 or 8
        if dice_roll == 6 or dice_roll == 8:
            #the 6 or 8 place pays out and stays on;
            #field loses (payout 0) and gets put back on
            payout = bet * place_68_payout - bet
            funds = funds + payout
        #roll the field:        
        elif (dice_roll == 3 or dice_roll == 4 or dice_roll == 9 or dice_roll == 10 or dice_roll == 11):
            #only our field bet hits (all bets stay on)
            payout = bet * field_payout
            funds = funds + payout
        #roll 2
        elif dice_roll == 2:
            #field bet pays double (all bets stay on)
            payout = bet * field_2_payout
            funds = funds + payout
        #roll 12
        elif dice_roll == 12:
            #field bet pays triple (all bets stay on)
            payout = bet * field_12_payout
            funds = funds + payout
        #roll 5
        else:
            #no payout and put field bet back on
            payout = -bet
            funds = funds + payout
    
    #record funds amount for future analysis
    bank_account.append(funds)

#%%
#convert "roll_catalog" to dataframe
df_roll_catalog = pd.DataFrame(roll_catalog, columns=['Dice_Roll'])

#convert "bank_account" to dataframe and add a column to count the dice rolls
df_bank_account = pd.DataFrame(bank_account, columns=['Funds'])
df_bank_account.insert(0, 'Roll_#', range(0, len(df_bank_account)))


#%%
#create a histogram of dice roll frequency - confirm bell curve shape
fig, ax = plt.subplots()
ax.hist(df_roll_catalog['Dice_Roll'], bins=11, color='blue')
plt.show()

#plot line graph of funds after each roll
plt.plot(df_bank_account['Roll_#'], df_bank_account['Funds'])
plt.xlabel('Roll #')
plt.ylabel('Funds')

plt.show()