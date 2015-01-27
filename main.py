#!/bin/env python

##################################
#== IMPORTS ======================
##################################

from ROOT import *
execfile('./Selection.py')
execfile('./MassFit.py')
execfile('./DecayFit.py')
execfile('./TimeOscFit.py')

##################################
#== BODY ======================
##################################

Bs_Mass      = (5350, 5450)#(4000, 6000)
Ds_Mass      = (1950, 1990)#(1800, 2200)

Selection(Bs_Mass, Ds_Mass)

##################################

#MassFit()

##################################

Bs_Lifetime  = (0, 0.01)

DecayFit(Bs_Lifetime)

##################################

offset     = 0.0
amplitude  = 40.0
period     = 0.002
phase      = 0.0
lifetime   = 0.0015

#TimeOscFit(offset, amplitude, period, phase, lifetime)


##################################
#eof
