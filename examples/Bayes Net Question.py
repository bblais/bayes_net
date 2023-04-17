#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bayes_net import *


# http://stats.stackexchange.com/questions/79117/i-have-a-problem-in-bayesian-networks-get-pea
# 
# <img width=800 src="http://i.stack.imgur.com/cGYpA.png">

# In[23]:


A=Variable("A",[True,False])
B=Variable("B",[True,False])
E=Variable("E",[True,False],parents=[B])
D=Variable("D",[True,False],parents=[A,B])
                                     
A.set_cpt([0.2,0.8])
B.set_cpt([0.7,0.3])
print A.cpt
print B.cpt
E.set_cpt([0.1,0.9,0.9,0.1])
print E.cpt


# <img width=500 src="http://i.stack.imgur.com/cGYpA.png">

# In[24]:


D.set_cpt([.5,.5,.6,.4,.1,.9,.8,.2])
print D.cpt


# In[25]:


net=Network([A,B,D,E])


# weird that this gives this answer.  perhaps there is something I am missing

# In[31]:


net.P("A and B")  # should be 0.24 for A=False and B=False


# In[32]:


net.P("A=False and B=False")


# In[34]:


A.cpt*B.cpt


# In[ ]:




