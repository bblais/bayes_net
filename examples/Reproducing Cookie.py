#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bayes_net import *


# In[6]:


fuel=Variable("Fuel",[True,False])
spark=Variable("Spark",[True,False])
gauge=Variable("Gauge",['f','h','e'],parents=[fuel])
start=Variable("Start",[True,False],parents=[fuel,spark])
    
fuel.set_cpt([.98,.02])
spark.set_cpt([.96,.04])
gauge.set_cpt([.39,.60, .01,.001,.001,.998])
start.set_cpt([.99,.01,.01,.99,0,1,0,1])

net=Network([fuel,spark,gauge,start])


print (net.P("Start|Spark=False"))


# In[7]:


bowl=Variable("Bowl",["A","B"])
cookie=Variable("Cookie",["Chocolate","Vanilla"],parents=[bowl])


# In[8]:


bowl.set_cpt([.5,.5]) # equal priors on the bowls
cookie.set_cpt([.25,.75,.5,.5])
print (cookie)


# In[9]:


cookie.cpt


# In[10]:


net=Network([bowl,cookie])


# In[11]:


net.P("Cookie=Vanilla|Bowl=A")


# In[12]:


net.P("Bowl=A|Cookie=Vanilla")


# In[13]:


bowl.cpt


# In[14]:


cookie.cpt


# In[15]:


new_cpt=bowl.cpt*cookie.cpt
print (new_cpt)


# In[16]:


new_cpt.condition(bowl,'A')


# In[17]:


new_cpt.marginalize(bowl)


# In[18]:


new_cpt.marginalize(cookie)


# In[ ]:




