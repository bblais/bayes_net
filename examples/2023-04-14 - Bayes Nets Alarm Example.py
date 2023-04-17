#!/usr/bin/env python
# coding: utf-8

# ![image.png](attachment:46b26697-c5b3-4a26-a741-9b68422c01ae.png)

# https://github.com/MaxHalford/sorobn#usage

# In[1]:


from bayes_net import *


# In[2]:


B=Variable("Burglary",[True,False])
B.set_cpt([0.001,0.999])
print(B.cpt)


# In[3]:


E=Variable("Earthquake",[True,False])
E.set_cpt([0.002,0.998])
print(E.cpt)


# In[4]:


A=Variable("Alarm",[True,False],parents=[B,E])
A.set_cpt([0.95,0.05,0.95,.05,0.29,0.71,0.001,0.999])
print(A.cpt)


# In[5]:


J=Variable("John_Calls",[True,False],parents=[A])
J.set_cpt([0.9,0.1,0.05,0.95])
print(J.cpt)


# In[6]:


M=Variable("Mary_Calls",[True,False],parents=[A])
M.set_cpt([0.7,0.3,0.01,0.99])
print(M.cpt)


# In[7]:


net=Network([A,E,B,J,M])
net


# ![image.png](attachment:21fad176-0ab3-43dd-b052-2ba9d650742a.png)

# In[8]:


net.P("Burglary | John_Calls=True and Mary_Calls=True")


# In[ ]:




