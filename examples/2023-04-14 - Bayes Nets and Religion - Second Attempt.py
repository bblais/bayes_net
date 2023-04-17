#!/usr/bin/env python
# coding: utf-8

# In[25]:


import sorobn as hh
import pandas as pd


# https://github.com/MaxHalford/sorobn#usage

# In[26]:


bn = hh.BayesNet(
     ('Theism', 'Messiah'),
     ('Messiah', 'Evidence'),
)


# In[27]:


bn.P['Theism'] = pd.Series({False: 0.5, True: 0.5})


# In[28]:


bn.P['Messiah'] = pd.Series({
    (True, True): .25,   # P(M|T)
    (True, False): .75,  # P(~M|T)
    (False, True): 0,  # not specified  # P(M|~T)
    (False, False): 1,  # not specified # P(~M|~T)
})


# In[29]:


bn.P['Evidence'] = pd.Series({
    (True, True): 0.1,
    (True, False): .9,
    (False, True): .001,  # P(E|~M)
    (False, False): .999, 
})


# In[30]:


bn.prepare()


# In[31]:


bn.query('Messiah',event={})


# In[32]:


bn.query('Theism',event={'Evidence': True})


# In[33]:


bn.query('Messiah',event={'Evidence': True})


# https://medium.com/@nick-meader/a-bayesian-argument-for-the-resurrection-part-i-77a230293fc

# In[ ]:




