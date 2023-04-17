#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bayes_net import *


# In[2]:


import numpy as np
from numpy import sqrt


# https://medium.com/interfaith-now/how-likely-is-it-that-jesus-is-the-messiah-part-iv-9a8bc820c801

# In[3]:


T=Variable("Theism",[True,False])
T.set_cpt([0.5,0.5])
T.cpt


# In[4]:


M=Variable("Messiah",[True,False],parents=[T])
M.set_cpt([0.25,0.75,0,1])
M.cpt


# In[5]:


E=Variable("Evidence",[True,False],parents=[M])
E.set_cpt([0.1,0.9,0.001,.999])
E.cpt


# In[6]:


net=Network([T,M,E])


# In[7]:


net.P("Messiah")


# In[8]:


net.P("Theism")


# In[9]:


net.P("Theism | Evidence=True")


# In[10]:


net.P("Messiah | Evidence=True")


# In[11]:


net


# ## Number 2

# https://medium.com/@nick-meader/does-naturalism-or-christianity-better-account-for-the-universes-existence-4f44683a4c42

# In[12]:


B=Variable("Belief",["Christianity","Naturalism"])
B.set_cpt([0.5,0.5])
B.cpt


# In[16]:


E=Variable("Existence",[True,False],parents=[B])
E.set_cpt([0.8,.2,.4,.6])
E.cpt


# In[17]:


F=Variable("Finite",[True,False])
F.set_cpt([0.8,0.2])
F.cpt


# In[19]:


X=Variable("External",[True,False],parents=[F,E])
X.set_cpt([0.95,0.05,0.95,.05,0.29,0.71,0.001,0.999])
X.cpt


# In[ ]:




