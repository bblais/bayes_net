from bayes_net import *

light=Variable("light",[1,2,3,4])
light.set_cpt([.25,.25,.25,.25])

door=Variable("door",['open','closed'],parents=[light])
door.set_cpt([.1,.35,.1,.3,.6,.3,.2,.05])

net=Network([light,door])

print "net.P('door|light=3')"
print net.P('door|light=3')


light=Variable("light",[1,2,3,4])
light.set_cpt([.25,.25,.25,.25])

rng=Variable("range",[-1,0,1])
rng.set_cpt([.33,.33,.33])


door=Variable("door",['open','closed'],parents=[light,rng])
door.set_cpt([.1,.35,.1,.3,.6,.3,.2,.05])

net=Network([light,door,rng])

print "net.P('door|light=3')"
print net.P('door|light=3')

