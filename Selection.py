
from array import array
from sys import stdout

def Selection(Bs_Mass = (5330,5400), 
              Ds_Mass = (1955, 1985), 
              Bs_Lifetime = (0, 0.01) ) :

   wp = WorkspacePreparer(Bs_Mass, Ds_Mass, Bs_Lifetime)
   wp.prepareWorkspace()
   wp.saveWorkspace()

   selectedFile = TFile.Open("data/data_selected.root")
   selectedTree = selectedFile.Get("DecayTree")
   c1 = TCanvas("c1", "Bs mass")
   c1.cd()
   selectedTree.Draw("lab0_MM")
   c1.Update()
   c2 = TCanvas("c2", "Ds mass")
   c2.cd()
   selectedTree.Draw("lab2_MM")
   c2.Update()
   c3 = TCanvas("c3", "Bs lifetime")
   c3.cd()
   selectedTree.Draw("lab0_TAU")
   c3.Update()
   raw_input("Press enter to continue.")
   selectedFile.Close()




class WorkspacePreparer:

    def __init__(self, Bs_Mass, Ds_Mass, Bs_Lifetime):
        self.Bs_Mass = Bs_Mass
        self.Ds_Mass = Ds_Mass
        self.Bs_Lifetime = Bs_Lifetime

        self.massBsVar = RooRealVar("lab0_MM", "Bs mass", Bs_Mass[0], Bs_Mass[1], "MeV")
        self.massDsVar = RooRealVar("lab2_MM", "Ds mass", Ds_Mass[0], Ds_Mass[1], "MeV")
        self.decayVar = RooRealVar("lab0_TAU", "Bs decay time", Bs_Lifetime[0], Bs_Lifetime[1], "ns")
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
        lab0TAU_min = self.Bs_Lifetime[0]
        lab0TAU_max = self.Bs_Lifetime[1]

        # Tree to write to
        filetowrite = TFile("data/data_selected.root", "RECREATE")

        ## RooArgSet on which the data/dataset will be based
        varsSet = RooArgSet()
        varsSet.add(self.massBsVar)
        varsSet.add(self.massDsVar)
        varsSet.add(self.decayVar)
        varsSet.add(self.tagDecision)   
        varsSet.add(self.tagOmega)      
        varsSet.add(self.tagDecisionOS)
        varsSet.add(self.tagOmegaOS)    

        print "************************************"
        print "* Selecting data events for BsDsPi *"
        print "************************************"

        cuts = "(lab0_MM > %f) && (lab0_MM < %f) && (lab2_MM > %f) && (lab2_MM < %f) && (lab0_TAU > %f) && (lab0_TAU < %f)\
            " % (lab0M_min, lab0M_max, lab2M_min, lab2M_max, lab0TAU_min, lab0TAU_max)
        newTree = tree.CopyTree(cuts)
        newEntries = newTree.GetEntries()

        print "Done selecting events. Selected %d out of %d total events (%.2f%%)\
            " % (newEntries, tree.GetEntries(), (100. * newEntries) / tree.GetEntries())
        if newEntries < 10:
            raise Exception("Too few events %d!" % (newEntries))

        tree.Delete()

        dataSet = RooDataSet(dataSetName, dataSetName, newTree, varsSet)
        self.workspaceList.append(dataSet)

        filetowrite.cd()
        filetowrite.Write()
        filetowrite.Close()

