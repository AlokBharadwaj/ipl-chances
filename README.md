# ipl-prediction
This project is to perform prediction of IPL-2020 standings based on the scores available as of today. 
We can simulate 10,000 matches with a a prior probability distribution and predict the outcome after all the remaining matches have been played. The current model also takes into account the NRR of a match, and not just the points. This enables a more precise prediction model where we can actually predict which two teams has the highest chance of being in the top 2, and top 4. 

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
    
    
