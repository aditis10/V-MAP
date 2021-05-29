import pandas as pd
import numpy as np
from scipy.integrate import odeint
import plotly.express as px
from data_collection import *

#beta = effective_contact_rate
#delta = death_rate
#alpha = vaccination_rate
#gamma = recovery_rate
#sigma = vaccination_effectiveness_rate
def deriv(state, t, N, beta, gamma, delta, alpha, sigma):
    S = state[0]
    I = state[1]
    R = state[2]
    D = state[3]
    #if the state is a top 5 infection rate then increase its alpha
    if(S<0):
        alpha = 0
    dSdt = ((-beta * S * I / N) - alpha) 
    dIdt = (beta * S * I / N - (gamma * I) +  (R*sigma*beta*I/N)) 
    dRdt = gamma * I * (1-delta) - (R*sigma*beta*I/N) +alpha
    # dSdt = ((-beta * S * I / N) - alpha) if S + (-beta * S * I / N) - alpha  > 0.01 else 0
    # dIdt = (beta * S * I / N - (gamma * I) +  (R*sigma*beta*I/N))  if I + (beta * S * I / N - (gamma * I) +  (R*sigma*beta*I/N))  > .010 else 0
    # dRdt = gamma * I * (1-delta) - (R*sigma*beta*I/N) + (alpha if S + (-beta * S * I / N) - alpha > 0.01 else 0) 
    dDdt = gamma * I * delta
    return dSdt, dIdt, dRdt, dDdt

# data_collection.high_priority #make sure those states have people to vaccinate
def calc_all():
    for location in high_priority():
        total_pop = pop[location]
        SIDRV = get_SIDRV(0, location)
        infected = SIDRV['a']['confirmed']
        recovered = SIDRV['a']['recovered'] + SIDRV['a']['vaccinated']
        susceptible = SIDRV['a']['susceptible']
        dead = SIDRV['a']['deceased']
        deriv()
#returns data for a given day

location = input('enter location:')
total_pop = pop[location]
SIDRV = get_SIDRV(0, location)
infected = SIDRV['a']['confirmed']
recovered = SIDRV['a']['recovered'] + SIDRV['a']['vaccinated']
susceptible = SIDRV['a']['susceptible']
dead = SIDRV['a']['deceased']
print(total_pop, susceptible, infected, recovered, dead)


# transmission_rate = 0.05
# contacts_per_day = 5
# effective_contact_rate = transmission_rate*contacts_per_day
effective_contact_rate = get_beta(location)
death_rate = get_delta(location)
recovery_rate = 1/3.5
vaccination_rate = 10000000
vaccination_effectiveness_rate = 0.95
print(effective_contact_rate, death_rate)


days = range(0,1600)

ret = odeint(deriv,[susceptible,infected,recovered,dead],days,args=(total_pop,effective_contact_rate,recovery_rate,death_rate,vaccination_rate,vaccination_effectiveness_rate))
S,I,R,D = ret.T

#calculate data frame for each state
def data_frame():

    df = pd.DataFrame({
        'susceptible': S,
        'infected': I,
        'recovered': R,
        'dead' : D,
        'day': days
    })

    return df

if __name__ == '__main__':
    df = data_frame()    
    print(df)
    fig = px.line(df, x="day", y="infected", title='Life expectancy in Canada')
    fig.write_image("fig1.png")
