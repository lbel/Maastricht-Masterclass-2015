
def DecayFit(Bs_Lifetime) :

   print "************************************"
   print "* Doing decay time fit             *"
   print "************************************"

   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))

   lab0TAU_min = Bs_Lifetime[0]
   lab0TAU_max = Bs_Lifetime[1]
   cuts = "(lab0_TAU > %f) && (lab0_TAU < %f) && " % (lab0TAU_min, lab0TAU_max)
   cuts += "((lab0_BsTaggingTool_TAGOMEGA    < 0.49 && lab0_BsTaggingTool_TAGDECISION    != 0) || \
             (lab0_BsTaggingTool_TAGOMEGA_OS < 0.49 && lab0_BsTaggingTool_TAGDECISION_OS != 0))"
   data = w.data("BsDsPi_data").reduce(cuts)
   decayTime = w.var("lab0_TAU")

   m_tshift = RooRealVar("m_tshift","m_tshift",0., -1., 1.)
   m_alpha  = RooRealVar("m_alpha" ,"m_alpha" ,1.0, 0., 1000)
   m_lifetime = RooRealVar("m_lifetime", "m_lifetime", 0.0012, 0.0008, 0.0025)
   model = RooGenericPdf("DecayModel","DecayModel","(1 - exp( -(lab0_TAU-m_tshift)/m_alpha )) * exp( - lab0_TAU/m_lifetime )",
         RooArgList(decayTime, m_tshift, m_alpha, m_lifetime) )

   m_tshift.setConstant()
   #m_alpha.setConstant()
   model.fitTo(data)

   cDecay = TCanvas("cdecay","cdecay")
   frame = decayTime.frame()
   data.plotOn(frame)
   model.plotOn(frame)#, LineColor(kBlue))
   frame.Draw()
   cDecay.Update()

   print "************************************"
   print "* --> Fitted decay time = " + str(m_lifetime.getVal()) + " +- " + str(m_lifetime.getError())

   raw_input("Press enter to continue.")
   f.Close()



