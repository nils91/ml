import random

transitions=[[0,0,0.8],[0,1,0.2],[1,0,0.07],[1,1,0.93]]
emissions=[[1,0.1667,0.58334],[2,0.1667,0.08334],[3,0.1667,0.08334],[4,0.1667,0.08334],[5,0.1667,0.08334],[6,0.1667,0.08334]]

curstate=0

def emission_generate():
    def cube():        
        cube_throw=random.random()
        cur_emmision_probability=0
        emission_prob_range=[0,0,0,0,0,0]
        for i in range(len(emissions)):
            emission=emissions[i]
            emission_prob_range[i]=[emission[0],cur_emmision_probability,cur_emmision_probability+emission[curstate+1]]
            cur_emmision_probability+=emission[curstate+1]
        chosen_em=0
        for i in range(len(emission_prob_range)):
            cur_emission_prop_range=emission_prob_range[i]
            emission=cur_emission_prop_range[0]
            if cube_throw >= cur_emission_prop_range[1] and cube_throw < cur_emission_prop_range[2]:
                chosen_em=emission
        return chosen_em
    def coin():
        coin_throw=random.random()
        cur_state_trans=[]
        for i in range(len(transitions)):
            transition=transitions[i];
            startstate=transition[0];
            if startstate == curstate:
                cur_state_trans.append([transition[1],transition[2]])
        cur_state_trans_prob_range=[]
        tmp=0
        for i in range(len(cur_state_trans)):
            state_trans=cur_state_trans[i]
            cur_state_trans_prob_range.append([state_trans[0],tmp,tmp+state_trans[1]])
            tmp+=state_trans[1]
        new_state=curstate
        outcome=0            
        for i in range(len(cur_state_trans_prob_range)):
            cur_state_trans_prob_range_cur=cur_state_trans_prob_range[i]
            if coin_throw >= cur_state_trans_prob_range_cur[1] and coin_throw < cur_state_trans_prob_range_cur[2]:
                new_state=cur_state_trans_prob_range_cur[0]
        return new_state

    ems=cube()
    global curstate
    curstate=coin()
    return ems
        
        
        
    
for i in range(100):
    print("Current state is ",curstate)
    print("Emission is ",emission_generate())
