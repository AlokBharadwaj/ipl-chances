# ipl-chances based on current standings
What chances do each team in IPL have to qualify for play-offs?

IPL standings table gives an indicator of how each teams have performed so far. The points scored by each team mainly decide who gets to qualify for the next round. It is important for viewers to get a sense of how their favorite team is performing, and to know whether they qualify. Initially, the points table help give them an idea but at later stages the points table alone won't be sufficient - especially if your team is in the ranks 3-6. 

So far, newspapers and commmentators give a certain prediction based on the points scored. This approach is not very precise, as for crucial matches the net run rate plays a crucial role. It tells you "how good" a team need to win the remaining matches to qualify. 

This project uses Monte-carlo simulation on both the points and net-run rate to predict the chances each team has to qualify. For each simulated "game" the winner is chosen randomly at 50% probability. The net run rate is assumed to be equally probable between +5 and -5 (this will be updated in the next version). 

---------

Use the following code snippet to change the inputs
A "matches" variable is a list of tuples in teh following order: 
matches = [(team1,team2,p1,p2),(team3,team4,p3,p4),(team5,team6,p5,p6)...]
and each tuple is called a 'match' and is explained as below: 

(team1,team2,p1,p2)

team1: an object of the class 'team' representing one team which is playing
team2: an object of the class 'team' representing the second team which is playing
p1: the probability that team 1 will win (default 0.5)
p2: the probability that team 2 will win (default 0.5)

And after a match has been played, you can delete that match from the list, but before that update the table which gives current standings of each teams

    mi = team(0,16,1.186,'mi')
    dc = team(1,14,0.030,'dc')
    rcb = team(2,14,0.048,'rcb')
    kkr = team(3,12,-0.467,'kkr')
    kxip = team(4,12,-0.049,'kxip')
    rr = team(5,10,-0.505,'rr')
    srh = team(6,10,0.396,'srh')
    csk = team(7,10,-0.532,'csk')
    
    remaining_matches_list = [(kkr,kxip,0,1),(srh,dc,0.5,0.5),
                              (mi,rcb,0.5,0.5),(csk,kkr,0.5,0.5),
                              (kxip,rr,0.5,0.5),(dc,mi,0.5,0.5),
                              (rcb,srh,0.5,0.5),(csk,kxip,0.5,0.5),
                              (kkr,rr,0.5,0.5),(dc,rcb,0.5,0.5),(srh,mi,0.5,0.5)]
    
    '''
    After every match, update the index in 'remaingin_matches_list before sending it
    '''
    
    
    ipl2020 = tournament(remaining_matches_list[4:])
    
    
