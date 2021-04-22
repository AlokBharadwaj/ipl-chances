# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 19:01:42 2020

@author: Alok
"""

# Program to simulate winning probabilites for the remaining matches in IPLT20 2020 edition

import numpy as np
import random
import matplotlib.pyplot as plt
from statistics import mode
import pandas as pd

class league:
    ''' 
    Creates a league object which have the following properties: "Teams". 
    self.teams is just a list of teams, where each team is of the class 'team'
    '''
    
    def __init__(self,teams):
        '''
        A python list of team objects
        '''
        self.teams = teams
    
    def standings(self):
       '''
       Gives the current standings of all the teams in the league as a dictionary.
       The keys are arranged as per their rank order, which is calculated from both points 
       and NRR
       '''
        
       team_list = []
       for team in self.teams:
           team_list.append([team.id,team.point,team.nrr])
           
       team_list = np.array(team_list)
       
       sorted_teams = team_list[np.lexsort((team_list[:,2],team_list[:,1]))][::-1]
       sorted_teams_with_name = {}
       for i,team_row in enumerate(sorted_teams):
           team_id = team_row[0]
           points = team_row[1]
           nrr = team_row[2]
           team = self.get_team_from_id(team_id)
           sorted_teams_with_name[i] = [team.name,team.point,team.nrr,team]
       return sorted_teams_with_name
    
    def get_team_from_id(self,teamid):
        for team in self.teams:
            if team.id == teamid:
                return team
    
    def copy(self):
        copied_list = [team(x.id,x.score,x.nrr,x.name) for x in self.teams]
        return league(copied_list)
    
    
class team:
    ''' 
    A python class which has the following properties: 
        id: is a number 0 to 7 to identify a team
        point: is a number which gives the total points a team has had in the table
        nrr: teh overall NRR a team has achieved until this point
        name: the team name given as a string
        '''
        
    def __init__(self,id,initial_point,initial_nrr,name):
        self.id = id
        self.point = initial_point
        self.nrr = initial_nrr
        self.name = name
    
    def add_points(self,point):
        self.point += point
    
    def add_nrr(self,nrr):
        self.nrr += nrr

class tournament:
    '''
    the tournament class has the following properties: 
        matches: This contains the list of all remaining matches in the tourname
        
        
                
    '''
    def __init__(self,matches):
        '''
        A "matches" variable is a list of tuples in teh following order: 
            matches = [(team1,team2,p1,p2),(team3,team4,p3,p4),(team5,team6,p5,p6)...]
            
            and each tuple is called a 'match' and is explained as below: 
                (team1,team2,p1,p2)
                team1: an object of the class 'team' representing one team which is playing
                team2: an object of the class 'team' representing the second team which is playing
                p1: the probability that team 1 will win (default 0.5)
                p2: the probability that team 2 will win (default 0.5)
    '''                
        self.matches = matches
    
    def get_matches(self):
        list_of_matches = []
        for match in self.matches:
            team1 = match[0]
            team2 = match[1]
            team1_prob = match[2]
            team2_prob = match[3]
            list_of_matches.append((team1,team2,team1_prob,team2_prob))
        return list_of_matches

def get_match_result(match):
    ''' 
    A function which "chooses" the winner of a particular match based on the prior probability
    of that match
    
    suppose a 'match' variable is called with following example: (team1,team2,0.7,0.3)
    here the probability of team 1 winning is set as 0.7, while that of team 2 is 0.3. 
    Thus the function returns team 1, with a probaability of 0.7, and team 2 with a 
    probabilty of 0.3. If this function is called with the same 'match' for 100 times,
    then the function returns team1  70 times, and team2 30 times (approx)
    
    '''
    teams = np.array([match[0],match[1]])
    probabilities = [match[2],match[3]]
    
    return np.random.choice(teams,1,replace=False,p=probabilities)[0]

def probability_upto_n(teamname,n):
    '''
    Calculates the probability of a team being in top 'n' positions
    '''
    
    p1 = positions[0].count(teamname) / 10000
    p2 = positions[1].count(teamname) / 10000
    p3 = positions[2].count(teamname) / 10000
    p4 = positions[3].count(teamname) / 10000
    p5 = positions[4].count(teamname) / 10000
    p6 = positions[5].count(teamname) / 10000
    p7 = positions[6].count(teamname) / 10000
    p8 = positions[7].count(teamname) / 10000
    
    p = [p1,p2,p3,p4,p5,p6,p7,p8]

    return sum(p[:n])

def probability_at_n(teamname,n):
    '''
    Calculates the probability of a team being at the 'n'th position
    '''
    p = positions[n].count(teamname) / 10000

    return p


def get_scenario(tournament_matches):
    
    ''''
    A scenario is one set of results for all the remaining matches of the tournament
    The input is tournament matches which is apython list of all remaining matches
    For each match the winner and loser is collected and returned as a python dictionary
    winners{0:winner1,1: winner2,..} where 0, 1, 2 are jjust index 
    '''
    winners = {}
    losers = {}
    for i,match in enumerate(tournament_matches):
        team1 = match[0].name
        team2 = match[1].name
        nrr = random.uniform(0,1)
        winner = get_match_result(match)
        loser = [x for x in match[:2] if x.name != winner.name][0]
        winners[i] = [(team1,team2),winner.name,winner.id,nrr]
        losers[i] = [(team1,team2),loser.name,loser.id,-nrr]
    
    return winners,losers
    
    
number_of_scenarios = 10000
winners = {}
losers = {}

final_standings = {}

current_standings = {}

for i in range(number_of_scenarios):   
    '''
    Input the current standings of all the teams 
    call each team in the following format: 
    mi = team(team_id, current_points, current_nrr, teamname) and so on
    '''
     
    mi = team(0,16,1.186,'mi')
    dc = team(1,14,0.030,'dc')
    rcb = team(2,14,0.048,'rcb')
    kkr = team(3,12,-0.467,'kkr')
    kxip = team(4,12,-0.049,'kxip')
    rr = team(5,10,-0.505,'rr')
    srh = team(6,10,0.396,'srh')
    csk = team(7,10,-0.532,'csk')
    
    teams_list = [mi,dc,rcb,kkr,kxip,rr,srh,csk]
    teams = league(teams_list)
    
    if i == 0:
        current_standings[i] = teams.standings()
    
    remaining_matches_list = [(kkr,kxip,0,1),(srh,dc,0.5,0.5),
                              (mi,rcb,0.5,0.5),(csk,kkr,0.5,0.5),
                              (kxip,rr,0.5,0.5),(dc,mi,0.5,0.5),
                              (rcb,srh,0.5,0.5),(csk,kxip,0.5,0.5),
                              (kkr,rr,0.5,0.5),(dc,rcb,0.5,0.5),(srh,mi,0.5,0.5)]
    
    '''
    After every match, update the index in 'remaingin_matches_list before sending it
    '''
    
    
    ipl2020 = tournament(remaining_matches_list[4:])


    winners[i],losers[i] = get_scenario(ipl2020.get_matches())
    
    for win_row in winners[i].values():
        winning_team_id = win_row[2]
        winning_team = teams.get_team_from_id(winning_team_id)
        winning_team.add_points(2)
        winning_team.add_nrr(win_row[3])
    
    for loser_row in losers[i].values():
        losing_team_id = loser_row[2]
        losing_team = teams.get_team_from_id(losing_team_id)
        losing_team.add_nrr(loser_row[3])
    
    final_standings[i] = teams.standings()
    
    del teams,mi,dc,rcb,kkr,kxip,rr,srh,csk
            
        
positions = []
for position in range(8):
    names = []
    for standing in final_standings.values():
        names.append(standing[position][0])
    positions.append(names)


rank = {}
for pos in range(8):
    teamname = mode(positions[pos])
    rank[pos] = [teamname,round(positions[pos].count(teamname)/number_of_scenarios*100,2)]

teamname_list = [x.name for x in teams_list]
    
overall_team_chances = {}
team_colors = {
        'mi':'blue',
        'dc':'purple',
        'rcb':'red',
        'csk':'yellow',
        'kkr':'black',
        'rr':'green',
        'kxip':'pink',
        'srh':'orange'}
for teamname in teamname_list:
    team_chances = []
    for pos in range(8):
        team_chances.append(positions[pos].count(teamname)/number_of_scenarios*100)
    team_chances = np.array(team_chances)
    overall_team_chances[teamname] = team_chances
x = np.arange(1,9,1)


for teamname in teamname_list:
    y = overall_team_chances[teamname]
    plt.fill_between(x,y,color=team_colors[teamname],alpha=0.6);
    plt.ylabel('Percentage chance')
    plt.xlabel('Position')
    plt.ylim([0,100])
    plt.title('Number of simulations: '+str(number_of_scenarios))

plt.legend(teamname_list,ncol=3,loc='upper left')


## Calculate average score and NRR

average_standing = {}

for teamname in teamname_list:
    avg_score = 0
    avg_nrr = 0
    for standing in final_standings.values():
        [(score,nrr)] = [(x[1],x[2]) for x in standing.values() if x[0] == teamname]
        avg_score += score
        avg_nrr += nrr

    average_standing[teamname] = [round(avg_score/number_of_scenarios),round(avg_nrr/number_of_scenarios,2)]

final_sorted_teamnames = sorted(average_standing,key=average_standing.get,reverse=True)

print('Team\t\t\t Score \t\t\t NRR \n\n')
for teamname in final_sorted_teamnames:
    print(teamname+'\t\t\t'+str(average_standing[teamname][0])+'\t\t\t'+str(average_standing[teamname][1]))


team_chances = []
for teamname in final_sorted_teamnames:
    
    if round(probability_upto_n(teamname,4),2) > 0:
        top2_if_top4 = round(probability_upto_n(teamname,2)/round(probability_upto_n(teamname,4),2),2)
    else:
        top2_if_top4 = 'N/A'
    team_chances.append([teamname,round(probability_upto_n(teamname,2),2),round(probability_upto_n(teamname,4),2),top2_if_top4])
    #print(teamname+'\t\t\t'+str(round(top_x_chance(teamname,2),2))+'\t\t\t'+str(round(top_x_chance(teamname,4),2)))

topchances_df = pd.DataFrame(team_chances,columns=['team','top 2','top 4','top 2 if (top 4)'])
display(topchances_df)
    
    
    