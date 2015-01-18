
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

#Bs_Mass      = (5330, 5400)
#Ds_Mass      = (1955, 1985) 
#Bs_Lifetime  = (0   , 0.01)

#Selection(Bs_Mass, Ds_Mass, Bs_Lifetime)

##################################

#MassFit()

##################################

#DecayFit()

##################################

offset     = 0.0
amplitude  = 40.0
period     = 0.002
phase      = 0.0
lifetime   = 0.0015

TimeOscFit(offset, amplitude, period, phase, lifetime)


##################################
#eof
