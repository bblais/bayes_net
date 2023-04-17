#!/usr/bin/env python
# coding: utf-8

# https://medium.com/interfaith-now/does-evidence-for-jesus-resurrection-meet-hume-s-criteria-for-miracles-b23b069dd2e7

# In[1]:


from bayes_net import *


# In[2]:


T=Variable("Theism",[True,False])
T.set_cpt([0.5,0.5])
T.cpt


# In[3]:


M=Variable("Messiah",[True,False],parents=[T])
M.set_cpt([0.25,0.75,0,1])
M.cpt


# > Therefore, the prior probability of a Messiah p(M|K) is 12.5%
# 
# This is sloppy.  He should have P(T|K)=0.5, P(M|K,T)=0.25, etc...

# In[4]:


net=Network([T,M])


# In[5]:


net.P("Messiah")


# Need to marginalize over the $T$, like:
# 
# \begin{aligned}
# P(M)&=P(M|T)P(T) + P(M|\sim\! T)P(\sim\! T) \\
# &=0.25 \cdot 0.5 + 0 \cdot 0.5 \\
# &=0.125
# \end{aligned}

# > The prior probability of a resurrection given our background knowledge p(R|K) is 0.03 (3%):
# >
# > - p(R|M&K) — probability of a resurrection if there is a Messiah multiplied (0.25) by
# > - p(M|T) — probability of a Messiah if there is a God (0.25) multiplied by
# > - p(T) — probability of God’s existence (0.5)
# 
# again, sloppy

# In[6]:


R=Variable("Resurrection",[True,False],parents=[M])
R.set_cpt([0.25,0.75,0,1])
R.cpt


# In[7]:


net=Network([T,M,R])


# In[8]:


net.P("Resurrection")


# In[9]:


EM=Variable("EvidenceM",[True,False],parents=[M])
EM.set_cpt([0.1,0.9,0.001,.999])
EM.cpt


# In[10]:


net=Network([T,M,R,EM])


# In[11]:


net.P("EvidenceM and Messiah")


# In[12]:


ER=Variable("EvidenceR",[True,False],parents=[R])
ER.set_cpt([0.1,0.9,0.001,.999])
ER.cpt


# In[13]:


net=Network([T,M,R,EM,ER])


# In[14]:


net


# In[15]:


net.P("Resurrection")


# In[19]:


net.P("Resurrection|EvidenceR and EvidenceM")


# In[21]:


net.P("Theism|EvidenceR and EvidenceM")


# In[22]:


net.P("Messiah|EvidenceR and EvidenceM")


# In[ ]:




