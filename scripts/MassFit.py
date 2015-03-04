def MassFit(particle) :

   if raw_input("Do %s mass fit? [y/N] " % (particle)) not in ["y", "Y"]:
       return

   print "************************************"
   print "* Doing mass fit                   *"
   print "************************************"

   f = TFile.Open("workspace.root")
   w = f.Get("w")
   assert(isinstance(w, RooWorkspace))

   data = w.data("BsDsPi_data")

   if (particle == "Bs"):
     varName = "lab0_MM"
     meanRange = [5366., 5360., 5372.]
   if (particle == "Ds"):
     varName = "lab2_MM"
     meanRange = [1970., 1965., 1975.]

   mass = w.var(varName)
   mean  = RooRealVar("mean",  "mass (MeV)",  meanRange[0], meanRange[1], meanRange[2]) ;
   width = RooRealVar("width", "width (MeV)",   15.,   5.,   50.) ;
   const = RooRealVar("const", "bg const", -0.005, -0.1, 0.1);

   sigModel = RooGaussian(   "sigModel", "signal PDF", mass, mean, width) ;
   bkgModel = RooExponential("bkgModel", "bkgrnd PDF", mass, const) ;

   Nsig = RooRealVar("Nsig", "signal Yield", 10000., 0., 10000000.);
   Nbkg = RooRealVar("Nbkg", "bkgrnd Yield", 10000., 0., 10000000.);
   model = RooAddPdf("model", "full PDF", RooArgList(sigModel, bkgModel), RooArgList(Nsig, Nbkg));

   model.fitTo(data)

   cMass = TCanvas("cMass_"+particle, "cMass"+particle)
   frame = mass.frame()
   frame.SetStats(False)
   frame.SetTitle("Fit to the %s mass" % (particle))
   data.plotOn(frame, RooFit.DataError(RooAbsData.SumW2))
   model.plotOn(frame, RooFit.LineColor(4 ) ) #9
   model.plotOn(frame, RooFit.LineColor(8 ), RooFit.LineStyle(2), RooFit.Components("sigModel"), RooFit.Name("sig") )
   model.plotOn(frame, RooFit.LineColor(46), RooFit.LineStyle(2), RooFit.Components("bkgModel"), RooFit.Name("bkg") )

   frame.Draw()

   leg = TLegend(0.64, 0.77, 0.89, 0.89)
   leg.AddEntry(frame.findObject("sig"), "Signal ("+particle+")", "l")
   leg.AddEntry(frame.findObject("bkg"), "Background", "l")
   leg.Draw("same")

   cMass.Update()
   cMass.SaveAs("plots/MassFit"+particle+".pdf")
   print " > Showing mass fit for %s" % (particle)
   print " > Signal events:     %d +- %d" % (Nsig.getVal(), Nsig.getError())
   print " > Background events: %d +- %d" % (Nbkg.getVal(), Nbkg.getError())
   raw_input("Press enter to continue.")
   f.Close()

