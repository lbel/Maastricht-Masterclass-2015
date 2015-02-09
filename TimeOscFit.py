
def TimeOscFit(offset = 0.0, amplitude = 40.0, period = 0.002, phase = 0.0, lifetime = 0.0015, omegaCut = "0.49", 
               Bs_Mass = (5330,5400), Ds_Mass = (1955, 1985), Bs_Lifetime = (0, 0.01), useOmegaWeights = False) :
   
   print "************************************"
   print "* Doing time oscillation 'fit':    *"
   print "* offset    = " + str(offset)
   print "* amplitude = " + str(amplitude)
   print "* period    = " + str(period)
   print "* phase     = " + str(phase)
   print "* lifetime  = " + str(lifetime)
   print "************************************"
   print "* - Using selection:               *"
   print "* TAGOMEGA < " + str(omegaCut)
   print "*  Bs_Mass: " + str(Bs_Mass)
   print "*  Ds_Mass: " + str(Ds_Mass)
   print "*  Bs_Lifetime: " + str(Bs_Lifetime)
   if(useOmegaWeights) : 
     print "*  (and weighting by TAGOMEGA)"
   print "************************************"


   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))

   decayTime = w.var("lab0_TAU")

   # Not sure how to construct (formula)weighted histograms from the RooDataSet... So just recreate!
   f = TFile.Open("data/data.root")
   t = f.Get("DecayTree")
 
   
   cuts = "(lab0_MM > %f) && (lab0_MM < %f) && (lab2_MM > %f) && (lab2_MM < %f) && (lab0_TAU > %f) && (lab0_TAU < %f)\
       " % (Bs_Mass[0], Bs_Mass[1], Ds_Mass[0], Ds_Mass[1], Bs_Lifetime[0], Bs_Lifetime[1])
        
   if(useOmegaWeights) :
     weight_SS = "(1-2*lab0_BsTaggingTool_TAGOMEGA)"
     weight_OS = "(1-2*lab0_BsTaggingTool_TAGOMEGA_OS)"
   else :
     weight_SS = weight_OS = "(1.)"

   cuts_Bs_SS     =  "("+cuts+" && lab0_BsTaggingTool_TAGDECISION     ==  1 && lab0_BsTaggingTool_TAGOMEGA    < "+omegaCut+")*"+weight_SS
   cuts_Bs_OS     =  "("+cuts+" && lab0_BsTaggingTool_TAGDECISION_OS  ==  1 && lab0_BsTaggingTool_TAGOMEGA_OS < "+omegaCut+")*"+weight_OS
   cuts_antiBs_SS =  "("+cuts+" && lab0_BsTaggingTool_TAGDECISION     == -1 && lab0_BsTaggingTool_TAGOMEGA    < "+omegaCut+")*"+weight_SS
   cuts_antiBs_OS =  "("+cuts+" && lab0_BsTaggingTool_TAGDECISION_OS  == -1 && lab0_BsTaggingTool_TAGOMEGA_OS < "+omegaCut+")*"+weight_OS

  
   print "> Building time osc histogram..."
   cOsc = TCanvas("cOsc","cOsc")
   t.Draw("lab0_TAU>>tagPosSS(100,"+str(Bs_Lifetime[0])+","+str(Bs_Lifetime[1])+")", cuts_Bs_SS    )
   t.Draw("lab0_TAU>>tagPosOS(100,"+str(Bs_Lifetime[0])+","+str(Bs_Lifetime[1])+")", cuts_Bs_OS    )
   t.Draw("lab0_TAU>>tagNegSS(100,"+str(Bs_Lifetime[0])+","+str(Bs_Lifetime[1])+")", cuts_antiBs_SS)
   t.Draw("lab0_TAU>>tagNegOS(100,"+str(Bs_Lifetime[0])+","+str(Bs_Lifetime[1])+")", cuts_antiBs_OS)
   tagPosSS = gDirectory.Get("tagPosSS")
   tagNegSS = gDirectory.Get("tagNegSS")
   tagPosOS = gDirectory.Get("tagPosOS")
   tagNegOS = gDirectory.Get("tagNegOS")
   for hist in [tagPosSS, tagNegSS, tagPosOS, tagNegOS] :
     hist.Sumw2()
   tagPosSS.Add(tagPosOS)
   tagNegSS.Add(tagNegOS)
   tagPosSS.Add(tagNegSS, -1)
   oscHist = RooDataHist("oscHist", "oscHist", RooArgList(decayTime), tagPosSS)


   print "> Overlaying fit shape..."
   m_offset = RooRealVar("m_offset","m_offset",offset,0.0,100.0)
   m_amplitude = RooRealVar("m_amplitude","m_amplitude",amplitude,0.0,100.0)
   m_period = RooRealVar("m_period","m_period",period,0.0,100.0)
   m_phase = RooRealVar("m_phase","m_phase",phase,0.0,100.0)
   m_lifetime = RooRealVar("m_lifetime", "m_lifetime", lifetime, 0.0010, 0.0020)
   model = RooFormulaVar("OscModel","OscModel","m_offset + m_amplitude * sin(2 * 3.14 * (1/m_period) * lab0_TAU + m_phase) * exp(-lab0_TAU/m_lifetime)",
         RooArgList(decayTime, m_offset, m_amplitude, m_period, m_phase, m_lifetime) )

  
   cOsc.Clear()
   frame = decayTime.frame()
   frame.SetTitle("Bs-antiBs Time Oscillation")
   oscHist.plotOn(frame)
   model.plotOn(frame)
   frame.Draw()
   cOsc.Update()
   cOsc.SaveAs("plots/TimeOsc.pdf")
   raw_input("Press enter to continue.")
   f.Close()




