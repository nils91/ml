import random

transitions=[[0,0,0.8],[0,1,0.2],[1,0,0.07],[1,1,0.93]]

def get_trans_prob(start,target):
    for i in range(len(transitions)):
        if transitions[i][0]==start-1 and transitions[i][1]==target-1:
            return transitions[i][2]
    return 1

emissions=[[1,1/6,7/12],[2,1/6,1/12],[3,1/6,1/12],[4,1/6,1/12],[5,1/6,1/12],[6,1/6,1/12]]
possible_emissions=[1,2,3,4,5,6]
states=[0,1]
start_state_prob=[1,0]

hmm=[states,possible_emissions,transitions,emissions,start_state_prob]

n=18

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

def get_start_state():
    random_value=random.random()
    state_prob_range=[]
    tmp=0
    for i in range(len(states)):
        state=states[i]
        state_prob=start_state_prob[i]
        state_prob_range.append([state,tmp,tmp+state_prob])
        tmp+=state_prob
    startstate=states[0]
    for i in range(len(state_prob_range)):
        if random_value >= state_prob_range[i][1] and random_value < state_prob_range[i][2]:
            startstate= state_prob_range[i][0]
    return startstate
        
def get_sequence_fixed_len(n):
    seq=[]
    for i in range(n):
        seq.append(emission_generate())
    return seq

def get_emissions_prob_in_state(state,em):
    for i in range(len(emissions)):
        if emissions[i][0] == em:
            return emissions[i][state]
    return 0



curstate=get_start_state()
sequence=[]
state_sequence=[]
for i in range(n):
    state_sequence.append(curstate+1)
    sequence.append(emission_generate())

def get_o(t):
    return sequence[t-1]

def get_maximum_combinational_probability_init(i):
    s_prob=start_state_prob[i-1]
    em_prob=get_emissions_prob_in_state(i,get_o(1));
    return s_prob*em_prob

def get_colluding_pre_state_init(i=0):
    return 0

def get_maximum_combinational_probability_rec(t,i):
    if t==1:
        return get_maximum_combinational_probability_init(i)
    maximum=0;
    for j in range(1,len(states)+1):
        trans_prob=get_trans_prob(j,i)
        mcp=get_maximum_combinational_probability_rec(t-1,j)
        maximum=max(maximum,trans_prob*mcp)
    em=get_o(t)
    em_prob=get_emissions_prob_in_state(i,em)
    return em_prob*maximum

def get_colluding_pre_state_rec(t,i):
    if t==1:
        return get_colluding_pre_state_init()
    argmaximum=0
    maximum=0
    for j in range(1,len(states)+1):
        val=get_trans_prob(j,i)*get_maximum_combinational_probability_rec(t-1,j)
        if val>maximum:
            argmaximum=j
            maximum=val
    return argmaximum

def get_q(t):
    if t == n:
        argmaximum=0
        maximum=0
        for j in range(1,len(states)+1):
            val=get_maximum_combinational_probability_rec(n,j)
            if val>maximum:
                argmaximum=j
                maximum=val
        return argmaximum
    return get_colluding_pre_state_rec(t+1,get_q(t+1))

def get_prob_o_q_star():
    maximum=0;
    for j in range(1,len(states)+1):
        maximum=max(maximum,get_maximum_combinational_probability_rec(n,j))

pred_sequence=[];
for i in range(n):
    print("Working(",i+1,")")
    pred_sequence.append(get_q(i+1))

def get_accuracy():
    accuracy=0;
    for i in range(0,len(sequence)):
        if state_sequence[i] == pred_sequence[i]:
            accuracy+=1
    return accuracy/n

print("Sequence: ",sequence)
print("State sequence: ",state_sequence)
print("Predicted state sequence: ",pred_sequence)
print("Prediction accuracy: ",get_accuracy())
