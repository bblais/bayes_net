from bayes_net import *

if __name__=="__main__":

    asia=Variable("Asia",[True,False])
    smoking=Variable("Smoking",[True,False])
    tuberculosis=Variable("Tuberculosis",[True,False],parents=[asia])
    lung_cancer=Variable("Lung_Cancer",[True,False],parents=[smoking])
    lung_cancer_or_tb=Variable("Lung_Cancer_Or_TB",[True,False],
            parents=[lung_cancer,tuberculosis])
    bronchitis=Variable("Bronchitis",[True,False],parents=[smoking])
    xray=Variable("Xray",[True,False],
        parents=[lung_cancer_or_tb])
    trouble_breathing=Variable("Trouble_Breathing",[True,False],
        parents=[lung_cancer_or_tb,bronchitis])
    

    asia.set_cpt([.99,.01])
    smoking.set_cpt([.50,.50])
    tuberculosis.set_cpt([0.99,0.01,0.95,0.05])
    lung_cancer.set_cpt([0.99,0.01,0.90,0.10])
    lung_cancer_or_tb.set_cpt([1,0,1,0,1,0,0,1])
    bronchitis.set_cpt([0.70,0.30,0.40,0.60])
    xray.set_cpt([0.95,0.05,0.02,0.98])
    trouble_breathing.set_cpt([0.9,0.1, 0.2,0.8, 0.3,0.7, 0.1,0.9])
    
    net=Network([asia,smoking,tuberculosis,lung_cancer,
        lung_cancer_or_tb,bronchitis,xray,trouble_breathing])
        
    
    print net.P("Lung_Cancer|Trouble_Breathing")
    