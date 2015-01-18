
def TimeOscFit(offset = 0.0, amplitude = 40.0, period = 0.002, phase = 0.0, lifetime = 0.0015) :

   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))

   data = w.data("BsDsPi_data_oscPlot")
   decayTime = w.var("lab0_TAU")

   m_offset = RooRealVar("m_offset","m_offset",offset,0.0,100.0)
   m_amplitude = RooRealVar("m_amplitude","m_amplitude",amplitude,0.0,100.0)
   m_period = RooRealVar("m_period","m_period",period,0.0,100.0)
   m_phase = RooRealVar("m_phase","m_phase",phase,0.0,100.0)
   m_lifetime = RooRealVar("m_lifetime", "m_lifetime", lifetime, 0.0010, 0.0020)
   model = RooFormulaVar("OscModel","OscModel","m_offset + m_amplitude * sin(2 * 3.14 * (1/m_period) * lab0_TAU + m_phase) * exp(-lab0_TAU/m_lifetime)",
         RooArgList(decayTime, m_offset, m_amplitude, m_period, m_phase, m_lifetime) )
   #model = RooFormulaVar("OscModel","OscModel","m_offset + m_amplitude * sin(2 * 3.14 * (1/m_period) * lab0_TAU + m_phase)",
   #      RooArgList(decayTime, m_offset, m_amplitude, m_period, m_phase) )

   
   cOsc = TCanvas("cOsc","cOsc")
   frame = decayTime.frame()
   data.plotOn(frame)
   model.plotOn(frame)#, LineColor(kBlue))
   frame.Draw()
   cOsc.Update()
   raw_input("Press any key to continue.")
   f.Close()




