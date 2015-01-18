
def MassFit() :

   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))

   data = w.data("BsDsPi_data")
   mass = w.var("lab0_MM")
   mean  = RooRealVar("mean",  "B_{s}^{0} mass (MeV)",  5366., 5360., 5372.) ;
   width = RooRealVar("width", "B_{s}^{0} width (MeV)",   20.,   10.,   30.) ;

   model = RooGaussian("signal", "signal PDF", mass, mean, width) ;

   model.fitTo(data)

   cMass = TCanvas("cMass","cMass")
   frame = mass.frame()
   data.plotOn(frame)
   model.plotOn(frame)#, LineColor(kBlue))
   frame.Draw()
   cMass.Update()
   raw_input("Press any key to continue.")
   f.Close()

