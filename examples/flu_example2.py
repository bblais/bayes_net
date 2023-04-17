from __future__ import division
from bayes_net import *

flu=Variable("Flu",[True,False])
hightemp=Variable("HighTemp",[True,False],
    parents=[flu])
hightherm=Variable("HighTherm",[True,False],
    parents=[hightemp])

flu.set_cpt([0.05,0.95])
hightemp.set_cpt([0.9,0.1,0.2,0.8])
hightherm.set_cpt([0.95,0.05,0.15,0.85])

net=Network([flu,hightemp,hightherm])

print net.P("HighTherm|Flu")

print net.P("Flu|HighTherm")


# done by sampling
sample=net.sample(100000)
# calculate net.P("Flu|HighTherm") with sampling
count1=len([s for s in sample if s['Flu'] and s['HighTherm']])
count2=len([s for s in sample if s['HighTherm']])

print count1/count2
