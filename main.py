#!/bin/env python

##################################
#== IMPORTS ======================
##################################

from ROOT import *

gROOT.ProcessLine(".x lhcbStyle.C")
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetLegendFont(132);
gROOT.ForceStyle();
TH1.SetDefaultSumw2(True)

execfile('./scripts/Selection.py')
execfile('./scripts/MassFit.py')
execfile('./scripts/DecayFit.py')
execfile('./scripts/TimeOscFit.py')

##################################
#== BODY =========================
##################################

# SELECTION ######################
Bs_Mass      = (4800, 6000)
Ds_Mass      = (1800, 2100)
Bs_Lifetime  = (0.0 , 0.01)

#Selection(Bs_Mass, Ds_Mass, Bs_Lifetime)

# MASS FITS ######################

#MassFit("Ds")
#MassFit("Bs")

# DECAY-TIME FITS ################

omegaCut = 0.5

#DecayFits(omegaCut, Bs_Lifetime)

# OSCILLATION FIT ################

offset     = 0.0
amplitude  = 0.45
period     = 0.001
phase      = 0.0

#TimeOscFit(offset, amplitude, period, phase, omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime)

##################################
