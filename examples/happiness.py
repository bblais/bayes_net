from bayes_net import *

sunny=Variable("Sunny",[True,False])
sunny.set_cpt([.7,.3])

lottery=Variable("Lottery",[True,False])
lottery.set_cpt([.01,.99])

happy=Variable("Happy",[True,False],parents=[lottery,sunny])
happy.set_cpt([1.0, 0.0,          # +S,+L
               0.9, 0.1,      # -S,+L
               0.7, 0.3,      # +S,-L
               0.1, 0.9])      # -S,-L

net=Network([happy,lottery,sunny])

print "Lottery alone"
print net.P("Lottery")

print "Lottery given Sunny"
print net.P("Lottery|Sunny")

print "Lottery given Happy"
print net.P("Lottery|Happy")

print "Lottery given Happy and Sunny"
print net.P("Lottery|Happy and Sunny")
