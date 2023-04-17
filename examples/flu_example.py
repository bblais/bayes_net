from bayes_net import *

flu=Variable("Flu",[True,False])
hightemp=Variable("HighTemp",[True,False],
    parents=[flu])

flu.set_cpt([0.05,0.95])
hightemp.set_cpt([0.9,0.1,0.2,0.8])

net=Network([flu,hightemp])

print net.P("HighTemp|Flu")

print net.P("Flu|HighTemp")
