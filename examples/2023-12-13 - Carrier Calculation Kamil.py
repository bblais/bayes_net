#!/usr/bin/env python
# coding: utf-8

# In[18]:


from bayes_net import *


# In[19]:


H=Variable("Historical",[True,False])
H.set_cpt([0.5,0.5])
print(H.cpt)


# In[20]:


e3=Variable("After_9th",[True,False])
e3.set_cpt([0.5,0.5])
print(e3.cpt)


# In[21]:


def LS(h,N):
    return (h+1)/(N+2)


# In[22]:


N_hb,N_ha,N_mb,N_ma=(0, 26, 13, 1)
N_h=N_hb+N_ha
N_m=N_mb+N_ma
N=N_h+N_m


# In[23]:


e2=Variable("Rank_Raglan",[True,False],parents=[H,e3])
e2.set_cpt([LS(N_ha,N_h)*LS(N_h,N),
            1-LS(N_ha,N_h)*LS(N_h,N),
            LS(N_hb,N_h)*LS(N_h,N),
            1-LS(N_hb,N_h)*LS(N_h,N),
            LS(N_ma,N_m)*LS(N_m,N),
            1-LS(N_ma,N_m)*LS(N_m,N),
            LS(N_mb,N_m)*LS(N_m,N),
            1-LS(N_mb,N_m)*LS(N_m,N),
           ])
print(e2.cpt)


# In[24]:


net=Network([H,e2,e3])
net


# ## With and without the 9th century reference class

# In[25]:


net.P("Historical | After_9th=True and Rank_Raglan=True")


# In[26]:


net.P("Historical | Rank_Raglan=True")


# In[28]:


net


# ## Update with $e_4$ and $e_5$

# In[10]:


N_hb,N_ha,N_mb,N_ma=(10, 100, 100, 10)
N_h=N_hb+N_ha
N_m=N_mb+N_ma
N=N_h+N_m


# In[11]:


e4=Variable("Founder",[True,False],parents=[H,e3])
e4.set_cpt([LS(N_ha,N_h)*LS(N_h,N),
            1-LS(N_ha,N_h)*LS(N_h,N),
            LS(N_hb,N_h)*LS(N_h,N),
            1-LS(N_hb,N_h)*LS(N_h,N),
            LS(N_ma,N_m)*LS(N_m,N),
            1-LS(N_ma,N_m)*LS(N_m,N),
            LS(N_mb,N_m)*LS(N_m,N),
            1-LS(N_mb,N_m)*LS(N_m,N),
           ])
print(e4.cpt)


# In[12]:


N_hb,N_ha,N_mb,N_ma=(0, 6, 0, 0)
N_h=N_hb+N_ha
N_m=N_mb+N_ma
N=N_h+N_m


# In[13]:


e5=Variable("Daniel",[True,False],parents=[H,e3])
e5.set_cpt([LS(N_ha,N_h)*LS(N_h,N),
            1-LS(N_ha,N_h)*LS(N_h,N),
            LS(N_hb,N_h)*LS(N_h,N),
            1-LS(N_hb,N_h)*LS(N_h,N),
            LS(N_ma,N_m)*LS(N_m,N),
            1-LS(N_ma,N_m)*LS(N_m,N),
            LS(N_mb,N_m)*LS(N_m,N),
            1-LS(N_mb,N_m)*LS(N_m,N),
           ])
print(e5.cpt)


# In[14]:


net=Network([H,e2,e3,e4,e5])


# In[15]:


net.P("Historical | Rank_Raglan=True")


# In[16]:


net.P("Historical | Rank_Raglan=True and Founder=True and Daniel=True and After_9th=True")


# In[17]:


net


# In[ ]:





# In[ ]:




