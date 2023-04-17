from bayes_net import *

disease=Variable("Disease",[True,False])
disease.set_cpt([0.0001,0.9999])

test=Variable("Test",[True,False],parents=[disease])
test.set_cpt([.99,.01,.03,.97])


net=Network([disease,test])

print "Disease, given a positive test"
print net.P("Disease|Test=True")