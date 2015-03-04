def DecayFits(omegaCut, Bs_Lifetime):
    if raw_input("Execute decay time fits? [y/N] ") not in ["y", "Y"]:
        return

    from ROOT import RooFit

    DecayFit("Bs"    , "Bs",     omegaCut, Bs_Lifetime)
    DecayFit("Bs"    , "antiBs", omegaCut, Bs_Lifetime)
    DecayFit("antiBs", "Bs",     omegaCut, Bs_Lifetime)
    DecayFit("antiBs", "antiBs", omegaCut, Bs_Lifetime)

def DecayFit(prodID, decayID, omegaCut, Bs_Lifetime):

   print "************************************"
   print "* Showing tagged decay time for "+prodID+ " -> "+decayID
   print "*  using omega < "+str(omegaCut)
   print "************************************"

   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))



   if(prodID=="Bs")      : tag =  "1"
   if(prodID=="antiBs")  : tag = "-1"
   if(decayID=="Bs")     : piID = ">1" # Bs0 -> Ds- pi+
   if(decayID=="antiBs") : piID = "<1" # Bs0 -> Ds- pi+
   cuts = "( ( (lab0_BsTaggingTool_TAGDECISION    == "+tag+" && lab0_BsTaggingTool_TAGOMEGA    < "+str(omegaCut)+")   || \
               (lab0_BsTaggingTool_TAGDECISION_OS == "+tag+" && lab0_BsTaggingTool_TAGOMEGA_OS < "+str(omegaCut)+") \
             ) && lab1_ID"+piID + ")"

   data = w.data("BsDsPi_data")
   dataSub = data.reduce( cuts )
   decayTime = w.var("lab0_TAU")
   decayTime.setRange(Bs_Lifetime[0], Bs_Lifetime[1])

   if( prodID == decayID ) : phaseFix = 0.
   else : phaseFix = 3.14 / 2.

   m_tshift = RooRealVar("m_tshift","m_tshift",0.0002, -1., 1.)
   m_alpha  = RooRealVar("m_alpha" ,"m_alpha" ,0.0025, 0., 1000)
   m_lifetime = RooRealVar("m_lifetime", "m_lifetime", 0.0015, 0.0008, 0.0025)
   m_cosAmp = RooRealVar("m_cosAmp","m_cosAmp", 0.2, 0., 100.)
   m_phase = RooRealVar("m_phase", "m_phase", phaseFix)
   mean = RooRealVar("mean","mean",0.)
   width = RooRealVar("width","width",0.0017, 0.0001, 0.01)

   """
   modelSig = RooGenericPdf("DecayModel","DecayModel",
                         "(1 - exp( -(lab0_TAU-m_tshift)/m_alpha )) * \
                          exp( - lab0_TAU/m_lifetime ) + \
                          m_cosAmp * cos(0.0017*m_lifetime + m_phase)",
         RooArgList(decayTime, m_tshift, m_alpha, m_lifetime, m_cosAmp, m_phase) )
   modelErr = RooGaussian("gauss","gauss",decayTime, mean, width)
   #frac = RooRealVar("frac","frac",0.6,0.,1.)
   #model = RooAddPdf("model","model",RooArgList(modelSig, modelErr), RooArgList(frac) )
   #model = RooProdPdf("model","model",RooArgList(modelSig, modelErr) )

   #m_tshift.setConstant()
   #model.fitTo(dataSub)
   """

   cDecay = TCanvas("cdecay","cdecay")
   frame = decayTime.frame()
   frame.SetTitle("Decay Time ("+prodID+" -> "+decayID+"), TagOmega < " + str(omegaCut))
   dataSub.plotOn(frame)
   #model.plotOn(frame)
   frame.Draw()
   cDecay.Update()
   cDecay.SaveAs("plots/decayTime_"+prodID+"_to_"+decayID+".pdf")

   #print "************************************"
   #print "* Showing tagged decay-time distribution for " + prodID + " -> " + decayID
   #print "* --> Fitted lifetime = %.6f +- %.6f ns" % (m_lifetime.getVal(), m_lifetime.getError())
   #print "************************************"


   raw_input("Press enter to continue.")
   f.Close()



