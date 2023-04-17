from bayes_net import *

disease=Variable("Disease",[True,False])
disease.set_cpt([0.0001,0.9999])

test1=Variable("Test1",[True,False],parents=[disease])
test1.set_cpt([.99,.01,.03,.97])

test2=Variable("Test2",[True,False],parents=[disease])
test2.set_cpt([.8,.2,.1,.9])


net=Network([disease,test1,test2])

print "Disease, given both positive tests"
print net.P("Disease|Test1=True and Test2=True")

print "Test2 alone"
print net.P("Test2")

print "Test2 positive Test1"
print net.P("Test2|Test1")