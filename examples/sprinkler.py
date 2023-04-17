from bayes_net import *

cloudy=Variable("Cloudy",[True,False])
sprinkler=Variable("Sprinkler",[True,False],parents=[cloudy])    
rain=Variable("Rain",[True,False],parents=[cloudy])    
wetgrass=Variable("WetGrass",[True,False],parents=[rain,sprinkler])    

cloudy.set_cpt([0.5,0.5])
print cloudy.cpt

sprinkler.set_cpt([0.1,0.9,0.5,0.5])    
print sprinkler.cpt

rain.set_cpt([0.8,0.2,0.2,0.8])    
print rain.cpt

wetgrass.set_cpt([0.99,0.01,0.9,0.1,0.9,0.1,0.0,1.0])
print wetgrass.cpt


net=Network([cloudy,sprinkler,rain,wetgrass])