


import numpy as np
from copy import deepcopy
import re
from .utils import *
import time
import random

class Variable(object):

    def __init__(self,name,values,parents=None,children=None,
                    verbose=True):
        self.name=name
        self.values=values
        self.cpt=None
        self.verbose=verbose
        
        if not parents:
            parents=[]
            
        if not children:
            children=[]
        
        self.parents=[]
        self.children=[]
        
        self.add_parents(parents)
        self.add_children(children)

    def __eq__(self,other):
        return other==self.name

    def __ne__(self,other):
        return other!=self.name

    def __hash__(self):
        return hash(self.name)  #  allow it in a dictionary
        
    def __len__(self):
        return len(self.values)
        
    def __contains__(self,value):
        return value in self.values
        
    def __repr__(self):
    
        _str="%s with values %s" % (self.name,str(self.values))
        
        return _str

    def add_parents(self,parents):
        if not parents:
            return
        
        self.parents.extend(parents)
        
        for p in parents:
            p.children.append(self)
        
    def add_children(self,children):
        if not children:
            return
            
        self.children.extend(children)

        for child in children:
            child.parents.append(self)
        
    def set_cpt(self,pvals=None):
        variables=self.parents[:]
        if pvals is None:
            v=[]
            pvals=variables
        else:
            v=variables
            
        v.append(self)
        self.cpt=CPT(v,pvals)

class CPT(object):

    def __init__(self,variables,pvals):
        #np.set_printoptions(precision=4,suppress=True)
        self.variables=variables[:]
        
        vals=[x.values for x in self.variables]
        idx=[list(range(len(x))) for x in self.variables]
        combos=list(combinations(idx))

        if isinstance(pvals,list):
            pvals=flatten(pvals)
        else:
            pvals=pvals.ravel()


        dims=[len(x) for x in self.variables]
        self.data=np.zeros(shape=dims)
        
        for i,c in enumerate(combos):
            c=tuple(c)
            self.data[c]=pvals[i]
       
    def __getitem__(self,instance):
    
        idx=[]
        for v,i in zip(self.variables,instance):
            idx.append(v.values.index(i))
        idx=tuple(idx)
        return self.data[idx]
            
    def __setitem__(self,instance,value):
    
        idx=[]
        for v,i in zip(self.variables,instance):
            idx.append(v.values.index(i))
        idx=tuple(idx)
        self.data[idx]=value
            
       
    def __repr__(self):
    
        vals=[x.values for x in self.variables]
        idx=[list(range(len(x))) for x in self.variables]
        combos=list(combinations(idx))
        combo_vals=list(combinations(vals))
        _str=""
        line=""
        line2=""
        lengths=[]



        row=[v.name for v in self.variables]
        row+=['p']
        _str+=("{: ^10} "*len(row)).format(*row)
        _str+="\n"

        row=["="*len(v.name) for v in self.variables]
        row+=["="]
        _str+=("{: ^10} "*len(row)).format(*row)
        _str+="\n"

        
    
        for i,c in enumerate(combos):
            row=[]

            for j,v in zip(c,vals):
                row.append(str(v[j]))
            c=tuple(c)
            row.append("%f" % (self.data[c]))

            _str+=("{: ^10} "*len(row)).format(*row)
            _str+="\n"
            

        return _str

    def normalize(self,var=None):
        if var is None:
            new_data=self.data.copy()
            new_data/=new_data.sum()
            return CPT(self.variables,new_data)

            #var=self.variables[-1]
            
        var_idx=self.variables.index(var)
           
        new_data=self.data.copy()
        sub=self.marginalize(var)
        
        # reshape marginal for broadcasting
        dims=list(self.data.shape)
        dims[var_idx]=1
        divisor=sub.data
        divisor.shape=dims
        
        new_data/=divisor
        
        return CPT(self.variables,new_data)
        
    def condition(self,var,value):
        slices=[]
        for v in self.variables:
            if v==var:
                value_idx=v.values.index(value)
                slices.append(value_idx)
            else:
                slices.append(slice(None,None,None))

        slices=tuple(slices)
        new_data=self.data[:]
        new_data=new_data[slices]
        new_variables=self.variables[:]
        
        var_index=self.variables.index(var)
        new_variables.remove(var)

        return CPT(new_variables,new_data)
        
    def max(self):
        return self.data.max()
        
    def argmax(self):
        flat_idx=self.data.argmax()
        
        ind=np.indices(self.data.shape)
        vals=[]
        for i,v in zip(ind,self.variables):
            idx=i.flat[flat_idx]
            vals.append(v.values[idx])
            
        return vals
        
        
    def marginalize(self,*args):
        new_cpt=self    
        
        if isinstance(args[0],list):
            args=args[0]
        
        for var in args:
            var_idx=new_cpt.variables.index(var)
            new_variables=[v for v in new_cpt.variables if v!=var]
            
            new_data=new_cpt.data.sum(axis=var_idx)
            new_cpt=CPT(new_variables,new_data)
            
        return new_cpt

    def maximize(self,*args):
        new_cpt=self    
        for var in args:
            var_idx=new_cpt.variables.index(var)
            new_variables=[v for v in new_cpt.variables if v!=var]
            
            new_data=new_cpt.data.max(axis=var_idx)
            new_cpt=CPT(new_variables,new_data)
            
        return new_cpt
        
    def __rmul__(self,other):
        return self.__mul__(other)
        
    def __mul__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            return CPT(self.variables,self.data*other)
            
        new_variables=self.variables[:]
        new_axes=[]
        
        new_variables.extend([v for v in other.variables 
                    if not v in new_variables])

        # reshape the self data
        L=len(new_variables)
        data_self=self.data[:]
        new_shape=list(data_self.shape)
        new_shape.extend([1]*(L-len(new_shape)))
        data_self.shape=new_shape
        
        # adjust the axes of other
        new_axes=[new_variables.index(v) for v in other.variables]
        data_other=other.data[:]

        # bubble sort!
        switched=True
        while switched:
            switched=False
            for i in range(len(new_axes)-1):
                if new_axes[i+1]<new_axes[i]:
                    data_other=data_other.swapaxes(i,i+1)
                    other.variables[i+1],other.variables[i]=other.variables[i],other.variables[i+1]
                    new_axes[i+1],new_axes[i]=new_axes[i],new_axes[i+1]
                    switched=True

        # calculate the new shape of the data
        dims=[]
        count=0
        for i in range(L):
            if i in new_axes:
                dims.append(len(other.variables[count]))
                count+=1
            else:
                dims.append(1)
                
        data_other.shape=dims
            
        return CPT(new_variables,data_self*data_other)

 
class Network(object):
    
    def __init__(self,vars,name='untitled',verbose=True):
    
        self.verbose=verbose
        self.name=name
        self.node_dict={}
        
        if isinstance(vars,str):  # filename
            self.read(vars)
        else:            
            self.node_list=vars
            for var in vars:
                self.node_dict[var.name]=var
        
    def __repr__(self):
        _str="P("+",".join(self.node_dict.keys())+")="

        
        for key in self.node_dict:
            _str+="P("+key
            v=self.node_dict[key]
            if v.parents:
                _str+="|"
            _str+=",".join([_.name for _ in v.parents])
            _str+=")"

        _str+="\n\n"

        for key in self.node_dict:
            _str+="P("+key
            v=self.node_dict[key]
            if v.parents:
                _str+="|"
            _str+=",".join([_.name for _ in v.parents])
            _str+="):"
            _str+="\n\n"

            _str+=str(self.node_dict[key].cpt)
            _str+="============\n\n"

        return _str




    def _parse_string_query(self,query):

        
        q={}
        e={}
        
        try:
            left,right=query.split("|")
        except ValueError:
            left=query
            right=""

        left_parts=[x.strip() for x in left.split(" and ")]
        right_parts=[x.strip() for x in right.split(" and ")]
        
        if not right_parts[0]:
            right_parts=[]

        for part in left_parts:
        
            if "=" in part:
                var,val=part.split('=')
                var=var.strip()
                val=val.strip()
                if val=='true' or val=='True':
                    val=True
                if val=='false' or val=='False':
                    val=False
                    
                try:
                    val=int(val)
                except ValueError:
                    pass
                    
                q[var]=val
            else:
                part=part.strip()
                q[part]=None

        for part in right_parts:
        
            if "=" in part:
                var,val=part.split('=')
                var=var.strip()
                val=val.strip()
                if val=='true' or val=='True':
                    val=True
                if val=='false' or val=='False':
                    val=False
                    
                try:
                    val=int(val)
                except ValueError:
                    pass

                e[var]=val
            else:
                part=part.strip()
                e[part]=True
                
        return q,e    
        
    def P(self,query):
    
        q,e=self._parse_string_query(query)
        return self.inference(q,e)
        
    def inference(self,query,evidence={}):
    
        cpt=1.0
        for node in self.node_list:
            cpt=cpt*node.cpt
        
        marg_vars=[v for v in self.node_list if 
            not v in query and not v in evidence]

        cpt=cpt.marginalize(marg_vars)

        # condition on evidence
        for e in evidence:
            cpt=cpt.condition(e,evidence[e])

        
        #cpt=cpt.normalize(list(query.keys())[0])  # why this one?
        cpt=cpt.normalize()  


        for q in query:
            if not query[q] is None:
                cpt=cpt.condition(q,query[q])

        
        if not cpt.data.shape:  # single number
            cpt=float(cpt.data)
        
        return cpt
        
    def __getitem__(self,name):

        try:
            val=self.node_dict[name]
        except KeyError:
            val=self.node_list[name]

        return val

    def __getattr__(self,name):
        
        try:
            val=self.__getattribute__(name)  # circular?
        except AttributeError:
            val=self[name]

        return val
    
    def sort(self):
        # sort, so that no node depends on a node later in the list
        old_nodes=self.node_list
        nodes=[]
        names=[]
        
        # find all nodes without parents
        no_parents=[x for x in old_nodes if not x.parents]
        nodes.extend(no_parents)
        names.extend([x.name for x in no_parents])
        for node in no_parents:
            old_nodes.remove(node)
            
        while old_nodes:
            next_nodes=[]
            for node in old_nodes:
                parent_names=[x.name for x in node.parents]
                not_seen=[x for x in parent_names if not x in names]
                
                if not not_seen:
                    next_nodes.append(node)
        
            nodes.extend(next_nodes)
            names.extend([x.name for x in next_nodes])
            for node in next_nodes:
                old_nodes.remove(node)
        
        self.node_list=nodes
 
    
    def sample(self,N=1):  
                           
        self.sort()
        N=int(N)

        if self.verbose:
            print("Sampling %d times..." % N)
        t1=time.time()
        samples=[]
        for i in range(N):
        
            d={}
            for node in self.node_list:
                vals=node.values
                name=node.name
            

                p={}                
                if node.parents:
                    evidence=[d[x.name] for x in node.parents]
                    
                    #print "\tevidence: ",evidence
                    for v in vals:
                        p[v]=node.cpt[tuple(evidence+[v])]
                else:
                    for v in vals:
                        p[v]=node.cpt[v,]
                
                #print name
                #print "\t",p
                total=sum([p[v] for v in vals])
                prob=[p[v]/total for v in vals] # make sure it adds to 1
            
                cumulative_sum=[]
                total=0.0
                for v in prob:
                    total+=v
                    cumulative_sum.append(total)
                
            
                r=random.random()
                
                for v,c in zip(vals,cumulative_sum):
                    if r<=c:
                        d[name]=v
                        break
                #print "\t",d

            samples.append(d)
            
        self.samples=samples
        t2=time.time()
        s=time2str(t2-t1)
        if self.verbose:
            print("done. (%s)" % s)

        return samples


    def read(self,fname):
        
        with open(fname) as fid:
            s=fid.read()
            
        # do the variables
        p=re.compile("variable (.*) {.*\n.*{(.*)}")
        variables=p.findall(s)      
        
        new_variables=[]
        new_values=[]
        self.node_list=[]
        for v in variables:
            
            name=v[0]
            vals=[x.strip() for x in v[1].split(",")]
            newvals=[]
            for vv in vals:
                if vv=="True":
                    vv=True
                if vv=="False":
                    vv=False

                try:
                    vv=int(vv)
                except ValueError:
                    pass


                newvals.append(vv)

            var=Variable(name,newvals)
            self.node_list.append(var)
            self.node_dict[name]=var
            
        lines=s.split('\n')
        
        reading_current=False
        results=[]
        current=[]
        for line in lines:
            if line.startswith("probability"):
                reading_current=True
                current.append(line.split("(")[1].split(")")[0])
                
            elif reading_current:
                current.append(line.strip())
                
            if line.startswith("}") and reading_current:
                reading_current=False
                results.append(current)
                current=[]
        
        for res in results:
        
            parts=res[0].split("|")
            name=parts[0].strip()
            node=self[name]
        
            if len(parts)==1:  # no dependancies
                part=res[1].replace("table ","")
                part=part.replace(";","")
                prob=[float(x) for x in part.split(",")]
                node.set_cpt(prob)
            else:  # parents
                names=[x.strip() for x in parts[1].split(",")]
                parents=[self[name] for name in names]
                node.add_parents(parents)
            
                p=[]
                for ll in res[1:-1]:
                    parts=ll.split(")")[0].split("(")[1].split(",")
                    key=[x.strip() for x in parts]
                    key=replace(key,"True",True)
                    key=replace(key,"False",False)
                    key=tuple(key)
                    
                    parts=ll.split(")")[1].replace(";","").split(",")
                    prob=[float(x) for x in parts]
                    
                    p.extend(prob)
                node.set_cpt(p)    
