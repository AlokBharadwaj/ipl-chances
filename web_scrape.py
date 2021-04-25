#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 12:49:07 2021

@author: alok
"""

# Web scraping tool for IPL statistics
import bs4
import os, sys
import pandas as pd

def get_standings(year=2021,num_teams=8, verbose=True):
    '''
    Function to scrap webdata to retrieve IPL standings of a given year

    Parameters
    ----------
    year : int, optional
        IPL year. The default is 2021.
    num_teams : int, optional
        How many teams participated in IPL that year?. The default is 8.
    verbose : bool, optional
        verbose. The default is True.

    Returns
    -------
    ranks : dict
        ranks[order] = [name, nrr, points]

    '''
    
    from urllib.request import urlopen as uReq
    from bs4 import BeautifulSoup as soup

    year_str = str(year)
    myurl="https://www.iplt20.com/points-table/men/"+year_str
    
    tablename = "standings-table standings-table--full"
    
    # Start a client and download the page to a variable
    
    uClient = uReq(myurl)
    page_html = uClient.read()
    uClient.close()
    
    # Parse HTML using bs
    
    page_soup = soup(page_html, "html.parser")
    
    # Grab the table
    
    container_standings = page_soup.findAll("table",{"class":tablename})
    
    assert len(container_standings) == 1
    
    tag = container_standings[0]
    
    ipl_table_html = tag.contents
    
    #assert len(ipl_table_html) == 3+num_teams*2
    
    ranks = {}
    for i in range(num_teams):
        index_rank = 3+i*2
        name = ipl_table_html[index_rank].contents[3].contents[3].contents[1].contents[0]
        nrr = float(ipl_table_html[index_rank].contents[15].contents[0])
        points = float(ipl_table_html[index_rank].contents[21].contents[0])
        ranks[i] = [i, points, nrr, name]
    
    if verbose:
        print("Web scrap complete. \nURL: "+myurl+
              "\nReturn type: dict..."+
              "\nranks[rank_value]=[rank (int), points (float), nrr (float), name (str)]")
        
    return ranks
        
def get_schedule(verbose = True):
    from urllib.request import urlopen as uReq
    from bs4 import BeautifulSoup as soup
    from utils import shorthand
    
    schedule_url = "https://www.iplt20.com/matches/schedule/men"
    
    uClient = uReq(schedule_url)   
    page_html = uClient.read()
    uClient.close()
    
    page_soup = soup(page_html, "html.parser")
    
    container_schedule = page_soup.findAll("div",{"class":"match-list__list"})
    
    tag = container_schedule[0]
    
    schedule_html = tag.contents[1]
    
    schedule_parsed = {}
    indx = 0
    div_id = 1
    while div_id > 0:
        try:
            if len(schedule_html.contents[div_id]) == 11:
                match = schedule_html.contents[div_id].contents[3]
                team1 = match.contents[1].contents[5].contents[0]
                team2 = match.contents[3].contents[5].contents[0]
                if team1 != 'TBC' and team2 != 'TBC':
                    schedule_parsed[indx] = [shorthand(team1),shorthand(team2)]
                indx += 1
                #print(div_id, team1, team2)
            div_id += 1
            
        except IndexError:
            div_id = -100
            
    if verbose:
        print("Web scraping complete. \nNumber of remaining matches = "+str(len(schedule_parsed.keys())))
    
    return schedule_parsed

def get_IPL_statistics(years=list(range(2008,2021)),verbose = True):
    from urllib.request import urlopen as uReq
    from bs4 import BeautifulSoup as soup
    from utils import shorthand
    import bs4
    
    statistics = {}
    match_num = 0
    errors = []
    for year in years:
        
        url = "https://www.iplt20.com/matches/results/men/"+str(year)
        
        uClient = uReq(url)   
        page_html = uClient.read()
        uClient.close()
        if verbose:
            print("Read URL successfully \nParsing the page \n")
            
            
        page_soup = soup(page_html, "html.parser")
        
        container_results = page_soup.findAll("div",{"class":"match-list__list"})
        tag = container_results[0]
        all_matches = tag.contents[1]
        div_id = 1
        for check_div in all_matches:
            
            try:
                #check_div = all_matches.contents[div_id]
                if len(check_div) == 1 and isinstance(check_div, bs4.element.Tag):
                    match_date = check_div.contents[0]
                    #div_id += 2
                    #print(match_date)

                
                if len(check_div) == 11 and isinstance(check_div, bs4.element.Tag):
                    
                    result_html = check_div.findAll("div",{"class":"result__teams"})[0]
                    match_type = result_html.findAll("span",{"class":"result__description"})[0].contents[0]
                    match_place_time = result_html.contents[5].contents[2]
                    
                    
                    loser_html = result_html.findAll("div",{"class":"result__team result__team--loser"})[0]
                    loser_name_raw = loser_html.findAll("p",{"class":"result__team-name"})[0].contents[0]
                    loser_score_raw = loser_html.findAll("span",{"class":"result__score"})[0].contents[1].contents[0]
                    loser_wkts_raw = loser_html.findAll("span",{"class":"result__score"})[0].contents[2]
                    loser_overs_raw = loser_html.findAll("span",{"class":"result__score"})[0].contents[3].contents[0]
                    #print(loser_html)
                    winner_html = result_html.select("div[class=result__team]")[0]
                    winner_name_raw = winner_html.findAll("p",{"class":"result__team-name"})[0].contents[0]
                    winner_score_raw = winner_html.findAll("span",{"class":"result__score result__score--winner"})[0].contents[1].contents[0]
                    winner_wkts_raw = winner_html.findAll("span",{"class":"result__score result__score--winner"})[0].contents[2]
                    winner_overs_raw = winner_html.findAll("span",{"class":"result__score result__score--winner"})[0].contents[3].contents[0]
                    
                    ## Postprocess data
                    
                    time = "".join(match_place_time.split(sep=",")[0]).strip()
                    place = "".join(match_place_time.split(sep=",")[-1]).replace("\n","").strip()
                    
                    
                    winner = shorthand(winner_name_raw)
                    winner_runs = int(winner_score_raw)
                    winner_wickets = int(winner_wkts_raw.replace("\n","").split("/")[-1].strip())
                    winner_over = float(winner_overs_raw.replace("\n","").strip().split("/")[0])
                    
                    loser = shorthand(loser_name_raw)
                    loser_runs = int(loser_score_raw)
                    
                    if(len(loser_wkts_raw) < 2):
                        loser_wickets = 10
                    else:
                        loser_wickets = int(loser_wkts_raw.replace("\n","").split("/")[-1].strip())
                        
                    loser_over = float(loser_overs_raw.replace("\n","").strip().split("/")[0])
                    
                    ## Calculations 
                    
                    win_by_runs = winner_runs - loser_runs
                    win_run_rate = float((winner_runs/winner_over) - (loser_runs/loser_over))
                    
                    statistics[match_num] = [match_type, match_date, time, place, winner, 
                                             winner_runs, winner_wickets, winner_over, loser, loser_runs, 
                                             loser_wickets, loser_over, win_by_runs, win_run_rate]
                    #print(statistics[match_num])
                    match_num += 1
                    

            
            except IndexError:
                if verbose: 
#                    print("End of reading for the year: "+str(year)+"\n")
                    print(sys.exc_info())
                errors.append(["IndexError",year, match_num, result_html])
                match_num += 1
                
            except :
                errors.append(["OtherError",year, match_num, result_html])
                match_num += 1
                
                
        
    statistics_df = pd.DataFrame(statistics, index=['match_type','match_date', 'time', 'place',
                                                      'winner','winner_runs','winner_wkt','winner_overs',
                                                      'loser','loser_runs','loser_wkt','loser_overs',
                                                      'win_by_runs','win_run_rate'])
    
    
    return statistics_df.T, errors