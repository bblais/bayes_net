"""Generic object pickler and compressor

This module saves and reloads compressed representations of generic Python
objects to and from the disk.
"""

__author__ = "Bill McNeill <billmcn@speakeasy.net>"
__version__ = "1.0"

import pickle
import gzip
import os

def Save(object, filename='_memory_.dat'):
	"""Saves an object to disk
    
    Example:  Save([1,2,3])
	"""
	file = gzip.GzipFile(filename, 'wb')
	file.write(pickle.dumps(object, 1))
	file.close()


def Load(filename='_memory_.dat'):
	"""Loads an object from disk

    Example:  a=Load()
	"""
	file = gzip.GzipFile(filename, 'rb')
	buffer = ""
	while 1:
		data = file.read()
		if data == "":
			break
		buffer += data
	object = pickle.loads(buffer)
	file.close()
	return object



def Remember(*args,**kwargs):

    try:
        filename=kwargs['filename']
    except KeyError:
        filename='_memory_.dat'

    if len(args)>0:
        Save(args,filename)
        return

    Q=Load(filename)
    if len(Q)==1:
        Q=Q[0]
        
    return Q
    




if __name__ == "__main__":
	import sys
	import os.path
	
	class Object:
		x = 7
		y = "This is an object."
	
	filename = sys.argv[1]
	if os.path.isfile(filename):
		o = load(filename)
		print("Loaded %s" % o)
	else:
		o = Object()
		save(o, filename)
		print("Saved %s" % o)

