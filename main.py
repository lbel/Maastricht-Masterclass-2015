
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
Bs_Mass      = (5330, 5410)
Ds_Mass      = (1955, 1985) 
Bs_Lifetime  = (0.  , 0.01)

#Selection(Bs_Mass, Ds_Mass, Bs_Lifetime)


##################################

#MassFit("Bs")
#MassFit("Ds")


##################################

omegaCut = "0.49"

DecayFit("Bs"    , "Bs",     omegaCut)
DecayFit("Bs"    , "antiBs", omegaCut)
DecayFit("antiBs", "Bs",     omegaCut)
DecayFit("antiBs", "antiBs", omegaCut)


##################################

offset     = 0.0
amplitude  = 0.2
period     = 0.00178
phase      = 0.0

#TimeOscFit(offset, amplitude, period, phase,
#    omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime)

##################################
#eof
