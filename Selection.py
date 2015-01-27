
from array import array
from sys import stdout

def Selection(Bs_Mass, Ds_Mass):

   wp = WorkspacePreparer(Bs_Mass, Ds_Mass)
   wp.prepareWorkspace()
   wp.saveWorkspace()

   selectedFile = TFile.Open("data/data_selected.root")
   selectedTree = selectedFile.Get("DecayTree")
   cBsMass = TCanvas("cBsMass", "Bs mass")
   cBsMass.cd()
   selectedTree.Draw("lab0_MM")
   cBsMass.Update()
   cDsMass = TCanvas("cDsMass", "Ds mass")
   cDsMass.cd()
   selectedTree.Draw("lab2_MM")
   cDsMass.Update()
   raw_input("Press enter to continue.")
   selectedFile.Close()



class WorkspacePreparer:

    def __init__(self, Bs_Mass, Ds_Mass):
        self.Bs_Mass = Bs_Mass
        self.Ds_Mass = Ds_Mass

        self.massVar = RooRealVar("lab0_MM", "Bs mass", Bs_Mass[0], Bs_Mass[1], "MeV")
        self.decayVar = RooRealVar("lab0_TAU", "Bs decay time", 0., .02, "ns")
        self.tagDecision = RooRealVar("lab0_BsTaggingTool_TAGDECISION","Bs tag decision", -2, 2)
        self.tagOmega = RooRealVar("lab0_BsTaggingTool_TAGOMEGA","Bs tag omega", 0, 1)
        self.tagDecisionOS = RooRealVar("lab0_BsTaggingTool_TAGDECISION_OS","Bs tag decision OS", -2, 2)
        self.tagOmegaOS = RooRealVar("lab0_BsTaggingTool_TAGOMEGA_OS","Bs tag omega OS", 0, 1)
        self.varsVarList = []
        self.workspaceList = [self.tagDecision, self.tagOmega, self.tagDecisionOS, self.tagOmegaOS]

    def prepareWorkspace(self):
        f = TFile.Open("data/data.root")
        t = f.Get("DecayTree")
        self.obtainDataset(t)
        print

    def saveWorkspace(self):
        w = RooWorkspace('w', kTRUE)
        if not self.workspaceList:
            raise Exception("Trying to save workspace, but no items to be saved!")

        for item in self.workspaceList:
            getattr(w, "import")(item)

        fileName = "workspace.root"

        self.workspace = w
        self.workspaceList = []
        w.writeToFile(fileName)

    def obtainDataset(self, tree):
        dataSetName = "BsDsPi_data"
        lab0M_min = self.Bs_Mass[0]
        lab0M_max = self.Bs_Mass[1]
        lab2M_min = self.Ds_Mass[0]
        lab2M_max = self.Ds_Mass[1]

        # Tree to write to
        filetowrite = TFile("data/data_selected.root", "RECREATE")

        ## RooArgSet on which the data/dataset will be based
        varsSet = RooArgSet()
        varsSet.add(self.massVar)
        varsSet.add(self.decayVar)
        varsSet.add(self.tagDecision)
        varsSet.add(self.tagOmega)
        varsSet.add(self.tagDecisionOS)
        varsSet.add(self.tagOmegaOS)

        print "************************************"
        print "* Selecting data events for BsDsPi *"
        print "************************************"

        cuts = "(lab0_MM > %f) && (lab0_MM < %f) && (lab2_MM > %f) && (lab2_MM < %f)" % (lab0M_min, lab0M_max, lab2M_min, lab2M_max)
        newTree = tree.CopyTree(cuts)
        newEntries = newTree.GetEntries()

        print "Done selecting events. Selected %d out of %d total events (%.2f%%)" % (newEntries, tree.GetEntries(), (100. * newEntries) / tree.GetEntries())
        if newEntries < 10:
            raise Exception("Too few events %d!" % (newEntries))

        tree.Delete()

        dataSet = RooDataSet(dataSetName, dataSetName, newTree, varsSet)
        self.workspaceList.append(dataSet)

        # Create osc plot
        newTree.Draw("lab0_TAU>>tagPos(100,0,0.01)",   "(lab0_BsTaggingTool_TAGDECISION    ==  1)*(1-2*lab0_BsTaggingTool_TAGOMEGA   )")
        newTree.Draw("lab0_TAU>>tagNeg(100,0,0.01)",   "(lab0_BsTaggingTool_TAGDECISION    == -1)*(1-2*lab0_BsTaggingTool_TAGOMEGA   )")
        newTree.Draw("lab0_TAU>>tagPosOS(100,0,0.01)", "(lab0_BsTaggingTool_TAGDECISION_OS ==  1)*(1-2*lab0_BsTaggingTool_TAGOMEGA_OS)")
        newTree.Draw("lab0_TAU>>tagNegOS(100,0,0.01)", "(lab0_BsTaggingTool_TAGDECISION_OS == -1)*(1-2*lab0_BsTaggingTool_TAGOMEGA_OS)")
        tagPos   = gDirectory.Get("tagPos"  )
        tagNeg   = gDirectory.Get("tagNeg"  )
        tagPosOS = gDirectory.Get("tagPosOS")
        tagNegOS = gDirectory.Get("tagNegOS")
        tagPos.Add(tagPosOS)
        tagNeg.Add(tagNegOS)
        tagPos.Add(tagNeg, -1)
        oscHist = RooDataHist(dataSetName+"_oscPlot", dataSetName+"_oscPlot", RooArgList(self.decayVar), tagPos)
        self.workspaceList.append(oscHist)

        filetowrite.cd()
        filetowrite.Write()
        filetowrite.Close()

