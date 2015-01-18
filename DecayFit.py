
def DecayFit() :

   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))

   data = w.data("BsDsPi_data")
   decayTime = w.var("lab0_TAU")

   m_tshift = RooRealVar("m_tshift","m_tshift",0., -1., 1.)
   m_alpha  = RooRealVar("m_alpha" ,"m_alpha" ,1.0, 0., 1000)
   m_lifetime = RooRealVar("m_lifetime", "m_lifetime", 0.0015, 0.0010, 0.0020)
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
   raw_input("Press any key to continue.")
   f.Close()



