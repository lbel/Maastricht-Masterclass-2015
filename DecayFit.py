
def DecayFit(pid = "Bs", omegaCut = "0.49") :

   print "************************************"
   print "* Doing decay time fit             *"
   print "*  For omega < "+omegaCut+"0.49                *"
   print "************************************"

   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))



   if(pid=="Bs")     : tag =  "1"
   if(pid=="antiBs") : tag = "-1"
   cuts = "( (lab0_BsTaggingTool_TAGDECISION    == "+tag+" && lab0_BsTaggingTool_TAGOMEGA    < "+omegaCut+") || \
             (lab0_BsTaggingTool_TAGDECISION_OS == "+tag+" && lab0_BsTaggingTool_TAGOMEGA_OS < "+omegaCut+") )"

   data = w.data("BsDsPi_data")
   dataSub = data.reduce( cuts )
   decayTime = w.var("lab0_TAU")




   m_tshift = RooRealVar("m_tshift","m_tshift",0., -1., 1.)
   m_alpha  = RooRealVar("m_alpha" ,"m_alpha" ,1.0, 0., 1000)
   m_lifetime = RooRealVar("m_lifetime", "m_lifetime", 0.0012, 0.0008, 0.0025)
   model = RooGenericPdf("DecayModel","DecayModel","(1 - exp( -(lab0_TAU-m_tshift)/m_alpha )) * exp( - lab0_TAU/m_lifetime )",
         RooArgList(decayTime, m_tshift, m_alpha, m_lifetime) )

   m_tshift.setConstant()
   #m_alpha.setConstant()
   model.fitTo(dataSub)




   cDecay = TCanvas("cdecay"+pid,"cdecay"+pid)
   frame = decayTime.frame()
   frame.SetTitle("Decay Time ("+pid+"), TagOmega < " + omegaCut)
   dataSub.plotOn(frame)
   model.plotOn(frame)
   frame.Draw()
   cDecay.Update()
   cDecay.SaveAs("plots/decayTime_"+pid+".pdf")
  
   print "************************************"
   print "* --> Fitted decay time = " + str(m_lifetime.getVal()) + " +- " + str(m_lifetime.getError())

   raw_input("Press enter to continue.")
   f.Close()



