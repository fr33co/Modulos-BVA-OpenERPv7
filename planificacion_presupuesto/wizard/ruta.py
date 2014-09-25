# -*- coding: utf-8 -*-
import os,pwd
rutak =  os.getcwd()
print rutak
print ''
rutax = os.path.split(rutak+'planificacion_presupuesto')
print rutax[0]
print ''

rutay = os.path.dirname(rutak+'/ej1.py')
#print rutay

#print os.path.abspath(rutak)

rutad = os.path.abspath(rutak)
print rutad
 
