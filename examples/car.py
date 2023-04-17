from bayes_net import *

if __name__=="__main__":

    fuel=Variable("Fuel",[True,False])
    spark=Variable("Spark",[True,False])
    gauge=Variable("Gauge",['f','h','e'],parents=[fuel])
    start=Variable("Start",[True,False],parents=[fuel,spark])
        
    fuel.set_cpt([.98,.02])
    spark.set_cpt([.96,.04])
    gauge.set_cpt([.39,.60, .01,.001,.001,.998])
    start.set_cpt([.99,.01,.01,.99,0,1,0,1])

    net=Network([fuel,spark,gauge,start])


    print net.P("Start|Spark=False")
    