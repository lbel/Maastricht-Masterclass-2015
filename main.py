
##################################
#== IMPORTS ======================
##################################

from ROOT import *
execfile('./Selection.py')
execfile('./MassFit.py')
execfile('./DecayFit.py')
execfile('./TimeOscFit.py')

gROOT.SetStyle("Plain")
gStyle.SetFillColor(0)
gStyle.SetFillStyle(0)
gStyle.SetLineColor(0)

##################################
#== BODY ======================
##################################

#Bs_Mass      = (5200, 5600)
#Ds_Mass      = (1890, 2070) 
Bs_Mass      = (5330, 5400)
Ds_Mass      = (1955, 1985) 
Bs_Lifetime  = (0.  , 0.01)

#Selection(Bs_Mass, Ds_Mass, Bs_Lifetime)


##################################

#MassFit("Bs")
#MassFit("Ds")


##################################

omegaCut = "0.49"

#DecayFit("Bs"    , omegaCut)
#DecayFit("antiBs", omegaCut)


##################################

offset     = 0.0
amplitude  = 100.0
period     = 0.002
phase      = 0.0
lifetime   = 0.0017

TimeOscFit(offset, amplitude, period, phase, lifetime,
    omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime, useOmegaWeights = True )

##################################
#eof
