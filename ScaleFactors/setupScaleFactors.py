# Setup ScaleFactor objects to be "registered" with ROOT,
# allowing them to be called from TTree.Draw(), for example.
# Currently used for lepton scale factors and pileup weights.
#
# Modified from N. Smith, U. Wisconsin
# 

#!/usr/bin/env python
import ROOT
import argparse
import os
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def float2double(hist):
    if hist.ClassName() == 'TH1D' or hist.ClassName() == 'TH2D':
        return hist
    elif hist.ClassName() == 'TH1F':
        new = ROOT.TH1D()
        hist.Copy(new)
    elif hist.ClassName() == 'TH2F':
        new = ROOT.TH2D()
        hist.Copy(new)
    else:
        raise Exception("Bad hist, dummy")
    return new

def invert2DHist(hist):
    new_hist = hist.Clone()
    ROOT.SetOwnership(new_hist, False)
    for x in range(hist.GetNbinsX()+1):
        for y in range(hist.GetNbinsY()+1):
            value = hist.GetBinContent(x, y)
            new_hist.SetBinContent(y, x, value)
    new_hist.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    new_hist.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    return new_hist

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tightfr_file", type=str,
        default='data/fakeRate18Apr2017-3LooseLeptons-TightMuons.root')
parser.add_argument("-m", "--medfr_file", type=str,
        default='data/fakeRate18Apr2017-3LooseLeptons-MediumMuons.root')
args = parser.parse_args()
output_file = 'data/scaleFactors.root'
fScales = ROOT.TFile(output_file, 'recreate')

# For nTruePU reweighting
pileupSF = ROOT.ScaleFactor("pileupSF", "Run2016B-H 36.8/fb Pileup profile over RunIISpring16 MC Scale Factor, x=NTruePU")
pileupFile = ROOT.TFile.Open('PileupWeights/PU_Central.root')
pileupFileUp = ROOT.TFile.Open('PileupWeights/PU_minBiasUP.root')
pileupFileDown = ROOT.TFile.Open('PileupWeights/PU_minBiasDOWN.root')
pileupSF.Set1DHist(pileupFile.Get('pileup'), pileupFileUp.Get('pileup'), pileupFileDown.Get('pileup'))
fScales.cd()
pileupSF.Write()

electronTightIdSF = ROOT.ScaleFactor("electronTightIdSF", "Moriond '17 Electron Tight WP ID SF, x=Eta, y=Pt")
eidFile = ROOT.TFile.Open('data/moriond17ElectronTightSF.root')
electronTightIdSF.Set2DHist(float2double(eidFile.Get('EGamma_SF2D')))
fScales.cd()
electronTightIdSF.Write()
electronGsfSF = ROOT.ScaleFactor("electronGsfSF", "Moriond '17 Electron GSF track reco SF, x=Eta, y=Pt")
eleGsfFile = ROOT.TFile.Open('data/moriond17ElectronRecoSF.root')
electronGsfSF.Set2DHist(float2double(eleGsfFile.Get('EGamma_SF2D')))
fScales.cd()
electronGsfSF.Write()

muonIdSF = ROOT.ScaleFactor("muonTightIdSF", "Moriond '17 Muon Tight WP ID SF, x=abs(Eta), y=Pt, z=run number")
midFile1 = ROOT.TFile.Open('data/moriond17MuonID_BCDEF.root')
midFile2 = ROOT.TFile.Open('data/moriond17MuonID_GH.root')
muon_ptetaratio1 = midFile1.Get('MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
muon_ptetaratio2 = midFile2.Get('MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
muon_allratio = float2double(muon_ptetaratio1.Clone("muon_allratio"))
for xbin in range(muon_ptetaratio1.GetNbinsX()+2):
    for ybin in range(muon_ptetaratio1.GetNbinsY()+2):
        runBFmean, runBFerr = muon_ptetaratio1.GetBinContent(xbin, ybin), muon_ptetaratio1.GetBinError(xbin, ybin)
        runGHmean, runGHerr = muon_ptetaratio2.GetBinContent(xbin, ybin), muon_ptetaratio2.GetBinError(xbin, ybin)
        allmean = (20.5*runBFmean + 16.3*runGHmean) / 36.8
        allerr = (20.5*runBFerr + 16.3*runGHerr) / 36.8
        muon_allratio.SetBinContent(xbin, ybin, allmean)
        muon_allratio.SetBinError(xbin, ybin, allerr)
muonIdSF.Set2DHist(muon_allratio)
fScales.cd()
muonIdSF.Write()
muonIsoSF = ROOT.ScaleFactor("muonIsoSF", "Moriond '17 Muon Tight Iso (0.15) WP ID SF, x=abs(Eta), y=Pt, z=run number")
misoFile1 = ROOT.TFile.Open('data/moriond17MuonIso_BCDEF.root')
misoFile2 = ROOT.TFile.Open('data/moriond17MuonIso_GH.root')
muIso_ptetaratio1 = misoFile1.Get('TightISO_TightID_pt_eta/abseta_pt_ratio')
muIso_ptetaratio2 = misoFile2.Get('TightISO_TightID_pt_eta/abseta_pt_ratio')
muIso_allratio = float2double(muon_ptetaratio1.Clone("muIso_allratio"))
for xbin in range(muIso_ptetaratio1.GetNbinsX()+2):
    for ybin in range(muIso_ptetaratio1.GetNbinsY()+2):
        runBFmean, runBFerr = muIso_ptetaratio1.GetBinContent(xbin, ybin), muIso_ptetaratio1.GetBinError(xbin, ybin)
        runGHmean, runGHerr = muIso_ptetaratio2.GetBinContent(xbin, ybin), muIso_ptetaratio2.GetBinError(xbin, ybin)
        allmean = (20.5*runBFmean + 16.3*runGHmean) / 36.8
        allerr = (20.5*runBFerr + 16.3*runGHerr) / 36.8
        muIso_allratio.SetBinContent(xbin, ybin, allmean)
        muIso_allratio.SetBinError(xbin, ybin, allerr)
muonIsoSF.Set2DHist(muIso_allratio)
fScales.cd()
muonIsoSF.Write()

# Used for tests on fake rate files from Jakob and Svenja
#efakeRateFile = ROOT.TFile.Open('/eos/user/k/kelong/WZAnalysisData/FakeRates/fromJakob/eFakeRates.root')
#jakob_etight = efakeRateFile.Get('eFakeRates')
#jakob_etight = invert2DHist(jakob_etight)
#mfakeRateFile = ROOT.TFile.Open('/eos/user/k/kelong/WZAnalysisData/FakeRates/fromJakob/muFakeRates.root')
#jakob_mtight = mfakeRateFile.Get('muFakeRates')
#jakob_mtight = invert2DHist(jakob_mtight)
#
#eCBTightFakeRate = ROOT.ScaleFactor("eCBTightFakeRate_Jakob", "Fake rate from dijet control, via Jakob")
#eCBTightFakeRate.Set2DHist(jakob_etight, 0, 0, ROOT.ScaleFactor.AsInHist)
#mCBTightFakeRate = ROOT.ScaleFactor("mCBTightFakeRate_Jakob", "Fake rate from dijet control, via Jakob")
#mCBTightFakeRate.Set2DHist(jakob_mtight, 0, 0, ROOT.ScaleFactor.AsInHist)
#fScales.cd()
#mCBTightFakeRate.Write()
#eCBTightFakeRate.Write()

#fakeRateFile = ROOT.TFile.Open('/eos/user/k/kelong/WZAnalysisData/FakeRates/CutBasedFakeRate_fromSvenja_final.root')
#eCBMedFakeRate = ROOT.ScaleFactor("eCBMedFakeRate_Svenja", "Fake rate from dijet control, by Svenja")
#eCBMedFakeRate.Set2DHist(float2double(fakeRateFile.Get('e/medium/fakeratePtEta')), 0, 0, ROOT.ScaleFactor.AsInHist)
#eCBTightFakeRate = ROOT.ScaleFactor("eCBTightFakeRate_Svenja", "Fake rate from dijet control, by Svenja")
#eCBTightFakeRate.Set2DHist(float2double(fakeRateFile.Get('e/tight/fakeratePtEta')), 0, 0, ROOT.ScaleFactor.AsInHist)
#mCBMedFakeRate = ROOT.ScaleFactor("mCBMedFakeRate_Svenja", "Fake rate from dijet control, by Svenja")
#mCBMedFakeRate.Set2DHist(float2double(fakeRateFile.Get('m/medium/fakeratePtEta')), 0, 0, ROOT.ScaleFactor.AsInHist)
#mCBTightFakeRate = ROOT.ScaleFactor("mCBTightFakeRate_Svenja", "Fake rate from dijet control, by Svenja")
#mCBTightFakeRate.Set2DHist(float2double(fakeRateFile.Get('m/tight/fakeratePtEta')), 0, 0, ROOT.ScaleFactor.AsInHist)
#fScales.cd()
#mCBMedFakeRate.Write()
#mCBTightFakeRate.Write()
#eCBMedFakeRate.Write()
#eCBTightFakeRate.Write()

if os.path.isfile(args.medfr_file):
    print "INFO: Adding medium fake rates to %s" % output_file
    fakeRateFile = ROOT.TFile.Open(args.medfr_file)
    eCBMedFakeRateZjets = ROOT.ScaleFactor("eCBMedFakeRate", "Fake rate from Z+jet")
    eCBMedFakeRateZjets.Set2DHist(fakeRateFile.Get('DataEWKCorrected/ratio2D_allE'), 0, 0, ROOT.ScaleFactor.AsInHist)
    mCBMedFakeRateZjets = ROOT.ScaleFactor("mCBMedFakeRate", "Fake rate from Z+jet")
    mCBMedFakeRateZjets.Set2DHist(fakeRateFile.Get('DataEWKCorrected/ratio2D_allMu'), 0, 0, ROOT.ScaleFactor.AsInHist)
    fScales.cd()
    mCBMedFakeRateZjets.Write()
    eCBMedFakeRateZjets.Write()

if os.path.isfile(args.tightfr_file):
    print "INFO: Adding tight fake rates to %s" % output_file
    fakeRateFile = ROOT.TFile.Open(args.tightfr_file)
    eCBTightFakeRateZjets = ROOT.ScaleFactor("eCBTightFakeRate", "Fake rate from Z+jet")
    eCBTightFakeRateZjets.Set2DHist(fakeRateFile.Get('DataEWKCorrected/ratio2D_allE'), 0, 0, ROOT.ScaleFactor.AsInHist)
    mCBTightFakeRateZjets = ROOT.ScaleFactor("mCBTightFakeRate", "Fake rate from Z+jet")
    mCBTightFakeRateZjets.Set2DHist(fakeRateFile.Get('DataEWKCorrected/ratio2D_allMu'), 0, 0, ROOT.ScaleFactor.AsInHist)
    fScales.cd()
    mCBTightFakeRateZjets.Write()
    eCBTightFakeRateZjets.Write()
