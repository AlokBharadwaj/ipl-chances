#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 12:49:07 2021

@author: alok
"""

# Web scraping tool for IPL statistics
import bs4

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
    match_id_local = 1
    while match_id_local > 0:
        try:
            if len(schedule_html.contents[match_id_local]) == 11:
                match = schedule_html.contents[match_id_local].contents[3]
                team1 = match.contents[1].contents[5].contents[0]
                team2 = match.contents[3].contents[5].contents[0]
                if team1 != 'TBC' and team2 != 'TBC':
                    schedule_parsed[indx] = [shorthand(team1),shorthand(team2)]
                indx += 1
                #print(match_id_local, team1, team2)
            match_id_local += 1
            
        except IndexError:
            match_id_local = -100
            
    if verbose:
        print("Web scraping complete. \nNumber of remaining matches = "+str(len(schedule_parsed.keys())))
    
    return schedule_parsed
