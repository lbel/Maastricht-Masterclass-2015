from array import array
from ROOT import *
from sys import stdout

################################################################################
# This is where you input your selection criteria ##############################
################################################################################

Bs_Mass = (5330, 5400) #MeV
Ds_Mass = (1955, 1985) #MeV
Bs_Lifetime = (0, 0.02) #ps

################################################################################
# END ##########################################################################
################################################################################

class WorkspacePreparer:

    def __init__(self):
        self.massVar = RooRealVar("lab0_MM", "Bs mass (MeV)", Bs_Mass[0], Bs_Mass[1])
        self.varsVarList = []
        self.workspaceList = [] #items that should go into the workspace

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
        lab0M_min = Bs_Mass[0]
        lab0M_max = Bs_Mass[1]
        lab2M_min = Ds_Mass[0]
        lab2M_max = Ds_Mass[1]
        lab0TAU_min = Bs_Lifetime[0]
        lab0TAU_max = Bs_Lifetime[1]

        # Tree to write to
        filetowrite = TFile("data/data_selected.root", "RECREATE")

        ## RooArgSet on which the data/dataset will be based
        varsSet = RooArgSet()
        varsSet.add(self.massVar)

        print "************************************"
        print "* Selecting data events for BsDsPi *"
        print "************************************"

        cuts = "(lab0_MM > %f) && (lab0_MM < %f) && (lab2_MM > %f) && (lab2_MM < %f) && (lab0_TAU > %f) && (lab0_TAU < %f)" % (lab0M_min, lab0M_max, lab2M_min, lab2M_max, lab0TAU_min, lab0TAU_max)
        newTree = tree.CopyTree(cuts)
        newEntries = newTree.GetEntries()

        print "Done selecting events. Selected %d out of %d total events (%.2f%%)" % (newEntries, tree.GetEntries(), (100. * newEntries) / tree.GetEntries())
        if newEntries < 10:
            raise Exception("Too few events %d!" % (newEntries))

        tree.Delete()

        dataSet = RooDataSet(dataSetName, dataSetName, newTree, varsSet)

        self.workspaceList.append(dataSet)

        filetowrite.cd()
        filetowrite.Write()
        filetowrite.Close()

wp = WorkspacePreparer()
wp.prepareWorkspace()
wp.saveWorkspace()

selectedFile = TFile.Open("data/data_selected.root")
selectedTree = selectedFile.Get("DecayTree")
c1 = TCanvas("c1", "Bs mass")
c1.cd()
selectedTree.Draw("lab0_MM")
c2 = TCanvas("c2", "Ds mass")
c2.cd()
selectedTree.Draw("lab2_MM")
c3 = TCanvas("c3", "Bs lifetime")
c3.cd()
selectedTree.Draw("lab0_TAU")
raw_input("Press any key to continue.")
selectedFile.Close()

