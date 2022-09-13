import os, sys
import ROOT
import copy
from os import listdir
from PlotHelper import *
from TriggerList import *
sys.path.append('../')
from Helper.CosmeticCode import *

def get_parser():
    ''' Argument parser.                                                                                                                                                
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--infile',           action='store',                     type=str,            default='rootfiles/TrigHist_SingleElectron_Data2016_all.root',                    help="Which input root file?" )
    argParser.add_argument('--sample',           action='store',                     type=str,            default='SingleElectron_Data2016',                    help="Which sample?" )
    return argParser

options = get_parser().parse_args()

f = options.infile
sample = options.sample

lepOpt = 'Ele' if 'Ele' in sample else 'Mu'

if '2016' in sample : trigger = MET120Triggers
else: trigger = MET120Triggers

numTrigHist = dict((trigger[i], 'hMET_'+trigger[i]) for i in range(len(trigger)))

if os.path.exists(f):
    hfile = ROOT.TFile.Open(f)
else:
    print 'Trigger histogram file does not exist'

plotDir= os.getcwd()+"/Plots/"

trigDict = {}

for i in range(len(trigger)):
    trig=trigger[i]
    hist=numTrigHist[trig]
    if 'NoMu' in trig:
        trigDict[trig] = [hfile.Get(hist+'_MET_pt_num_'+sample), hfile.Get(hist+'_MET_pt_den_'+sample), hfile.Get(hist+'_HT_num_'+sample), hfile.Get(hist+'_HT_den_'+sample), hfile.Get(hist+'_jet1_pt_num_'+sample), hfile.Get(hist+'_jet1_pt_den_'+sample), hfile.Get(hist+'_MET_phi_num_'+sample), hfile.Get(hist+'_MET_phi_den_'+sample), hfile.Get(hist+'_Muon_pt_num_'+sample), hfile.Get(hist+'_Muon_pt_den_'+sample), hfile.Get(hist+'_Electron_pt_num_'+sample), hfile.Get(hist+'_Electron_pt_den_'+sample), hfile.Get(hist+'_LowPtEle_pt_num_'+sample), hfile.Get(hist+'_LowPtEle_pt_den_'+sample), hfile.Get(hist+'_LowPtEle1_pt_num_'+sample), hfile.Get(hist+'_LowPtEle1_pt_den_'+sample), hfile.Get(hist+'_deltaMET_pt_num_'+sample), hfile.Get(hist+'_deltaMET_pt_den_'+sample), hfile.Get(hist+'_deltaMET_rel_pt_num_'+sample), hfile.Get(hist+'_deltaMET_rel_pt_den_'+sample), hfile.Get(hist+'_AltMET_pt_num_'+sample), hfile.Get(hist+'_AltMET_pt_den_'+sample), hfile.Get(hist+'_MET_pt_Muon_pt_num_'+sample), hfile.Get(hist+'_MET_pt_Muon_pt_den_'+sample), hfile.Get(hist+'_MET_pt_AltMET_pt_num_'+sample), hfile.Get(hist+'_MET_pt_AltMET_pt_den_'+sample), hfile.Get(hist+'_AltMET_pt_Muon_pt_num_'+sample), hfile.Get(hist+'_AltMET_pt_Muon_pt_den_'+sample), hfile.Get(hist+'_deltaMET_pt_Muon_pt_num_'+sample), hfile.Get(hist+'_deltaMET_pt_Muon_pt_den_'+sample)]
    else:
        trigDict[trig] = [hfile.Get(hist+'_MET_pt_num_'+sample), hfile.Get(hist+'_MET_pt_den_'+sample), hfile.Get(hist+'_HT_num_'+sample), hfile.Get(hist+'_HT_den_'+sample), hfile.Get(hist+'_jet1_pt_num_'+sample), hfile.Get(hist+'_jet1_pt_den_'+sample), hfile.Get(hist+'_MET_phi_num_'+sample), hfile.Get(hist+'_MET_phi_den_'+sample), hfile.Get(hist+'_Muon_pt_num_'+sample), hfile.Get(hist+'_Muon_pt_den_'+sample), hfile.Get(hist+'_Electron_pt_num_'+sample), hfile.Get(hist+'_Electron_pt_den_'+sample), hfile.Get(hist+'_LowPtEle_pt_num_'+sample), hfile.Get(hist+'_LowPtEle_pt_den_'+sample), hfile.Get(hist+'_LowPtEle1_pt_num_'+sample), hfile.Get(hist+'_LowPtEle1_pt_den_'+sample)]

mg_MET_pt = ROOT.TMultiGraph()
mg_HT = ROOT.TMultiGraph()
mg_jet1_pt = ROOT.TMultiGraph()
mg_MET_phi = ROOT.TMultiGraph()
mg_Muon_pt = ROOT.TMultiGraph()
mg_Electron_pt = ROOT.TMultiGraph()
mg_LowPtEle_pt = ROOT.TMultiGraph()
mg_LowPtEle1_pt = ROOT.TMultiGraph()
mg_MET_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_MET_pt_leg.SetTextSize(0.03)
mg_HT_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_HT_leg.SetTextSize(0.03)
mg_jet1_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_jet1_pt_leg.SetTextSize(0.03)
mg_MET_phi_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_MET_phi_leg.SetTextSize(0.03)
mg_Muon_pt_leg = ROOT.TLegend(0.1, 0.67, 0.9, 0.9)
mg_Muon_pt_leg.SetTextSize(0.03)
mg_Electron_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_Electron_pt_leg.SetTextSize(0.03)
mg_LowPtEle_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_LowPtEle_pt_leg.SetTextSize(0.03)
mg_LowPtEle1_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_LowPtEle1_pt_leg.SetTextSize(0.03)

mg_AMET_pt = ROOT.TMultiGraph()
mg_AMET_phi = ROOT.TMultiGraph()
mg_AMuon_pt = ROOT.TMultiGraph()
mg_AElectron_pt = ROOT.TMultiGraph()
mg_AMET_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_AMET_pt_leg.SetTextSize(0.025)
mg_AMET_phi_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_AMET_phi_leg.SetTextSize(0.025)
mg_AMuon_pt_leg = ROOT.TLegend(0.1, 0.67, 0.9, 0.9)
mg_AMuon_pt_leg.SetTextSize(0.025)
mg_AElectron_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_AElectron_pt_leg.SetTextSize(0.025)
mg_AltMET_pt = ROOT.TMultiGraph()
mg_deltaMET_pt = ROOT.TMultiGraph()
mg_deltaMET_rel_pt = ROOT.TMultiGraph()
mg_AltMET_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_AltMET_pt_leg.SetTextSize(0.025)
mg_deltaMET_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_deltaMET_pt_leg.SetTextSize(0.025)
mg_deltaMET_rel_pt_leg = ROOT.TLegend(0.1, 0.68, 0.9, 0.9)
mg_deltaMET_rel_pt_leg.SetTextSize(0.025)

legends=[mg_MET_pt_leg, mg_HT_leg, mg_jet1_pt_leg, mg_MET_phi_leg, mg_Muon_pt_leg, mg_Electron_pt_leg, mg_LowPtEle_pt_leg, mg_LowPtEle1_pt_leg, mg_AMET_pt_leg, mg_AMET_phi_leg, mg_AMuon_pt_leg, mg_AElectron_pt_leg, mg_AltMET_pt_leg, mg_deltaMET_pt_leg, mg_deltaMET_rel_pt_leg]

for i in range(len(trigger)):
    trig=trigger[i]
    hist=trigDict[trig]
        #efficiencies
    heff_MET_pt = ROOT.TGraphAsymmErrors()
    heff_MET_pt.BayesDivide(hist[0],hist[1])
    leg_MET_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    heff_HT = ROOT.TGraphAsymmErrors()
    heff_HT.BayesDivide(hist[2],hist[3])
    leg_HT = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    heff_jet1_pt = ROOT.TGraphAsymmErrors()
    heff_jet1_pt.BayesDivide(hist[4],hist[5])
    leg_jet1_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    heff_MET_phi = ROOT.TGraphAsymmErrors()
    heff_MET_phi.BayesDivide(hist[6],hist[7])
    leg_MET_phi = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    heff_Muon_pt = ROOT.TGraphAsymmErrors()
    heff_Muon_pt.BayesDivide(hist[8],hist[9])
    leg_Muon_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    heff_Electron_pt = ROOT.TGraphAsymmErrors()
    heff_Electron_pt.BayesDivide(hist[10],hist[11])
    leg_Electron_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    heff_LowPtEle_pt = ROOT.TGraphAsymmErrors()
    heff_LowPtEle_pt.BayesDivide(hist[12],hist[13])
    leg_LowPtEle_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    heff_LowPtEle1_pt = ROOT.TGraphAsymmErrors()
    heff_LowPtEle1_pt.BayesDivide(hist[14],hist[15])
    leg_LowPtEle1_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
    if 'NoMu' in trig:
        heff_AltMET_pt = ROOT.TGraphAsymmErrors()
        heff_AltMET_pt.BayesDivide(hist[16],hist[17])
        leg_AltMET_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
        heff_deltaMET_pt = ROOT.TGraphAsymmErrors()
        heff_deltaMET_pt.BayesDivide(hist[18],hist[19])
        leg_deltaMET_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
        heff_deltaMET_rel_pt = ROOT.TGraphAsymmErrors()
        heff_deltaMET_rel_pt.BayesDivide(hist[20],hist[21])
        leg_deltaMET_rel_pt = ROOT.TLegend(0.3, 0.8, 0.9, 0.9)
        #num&den 1D plots
    PlotNumDen(hist, trig, 0, "MET (GeV)", "Entries/Bin width", plotDir, sample, "MET_Pt", "MET_pt_numden")
    '''PlotNumDen(hist, trig, 2, "HT (GeV)", "Entries/Bin width", plotDir, sample, "HT", "HT_numden")
    PlotNumDen(hist, trig, 4, "Leading jet pt (GeV)", "Entries/Bin width", plotDir, sample, "Jet1", "Jet1_pt_numden")
    PlotNumDen(hist, trig, 6, "MET phi", "Entries/Bin width", plotDir, sample, "MET_Phi", "MET_phi_numden")
    PlotNumDen(hist, trig, 8, "Muon Pt (GeV)", "Entries/Bin width", plotDir, sample, "Muon_Pt", "Muon_pt_numden")
    PlotNumDen(hist, trig, 10, "Electron Pt (GeV)", "Entries/Bin width", plotDir, sample, "Electron_Pt", "Electron_pt_numden")
    PlotNumDen(hist, trig, 12, "Low Pt Electron Pt (GeV)", "Entries/Bin width", plotDir, sample, "LowPtEle_Pt", "Electron_pt_numden")
    PlotNumDen(hist, trig, 14, "Leading Low Pt Electron Pt (GeV)", "Entries/Bin width", plotDir, sample, "LowPtEle1_Pt", "Electron1_pt_numden")
    if 'NoMu' in trig:
        PlotNumDen(hist, trig, 16, "delta MET Pt (GeV)", "Entries/Bin width", plotDir, sample, "deltaMET_Pt", "deltaMET_pt_numden")
        PlotNumDen(hist, trig, 18, "delta MET rel Pt (GeV)", "Entries/Bin width", plotDir, sample, "deltaMET_rel_Pt", "deltaMET_rel_pt_numden")
        PlotNumDen(hist, trig, 20, "AltMET Pt (GeV)", "Entries/Bin width", plotDir, sample, "AltMET_Pt", "AltMET_pt_numden")
        #num&den 2D plots
        NumDen2D(hist, trig, 22, "MET Pt (GeV)", "Muon Pt (GeV)", plotDir, sample, "MET_Pt-Muon_Pt", "MET_Pt_Muon_Pt")
        NumDen2D(hist, trig, 24, "MET Pt (GeV)", "Alt MET Pt (GeV)", plotDir, sample, "MET_Pt-AltMET_Pt", "MET_Pt_AltMET_Pt")
        NumDen2D(hist, trig, 26, "AltMET Pt (GeV)", "Muon Pt (GeV)", plotDir, sample, "AltMET_Pt-Muon_Pt", "AltMET_Pt_Muon_Pt")
        NumDen2D(hist, trig, 28, "deltaMET Pt (GeV)", "Muon Pt (GeV)", plotDir, sample, "deltaMET_Pt-Muon_Pt", "deltaMET_Pt_Muon_Pt")
    #efficiency plots
    if 'NoMu' in trig:
        EffPlot(mg_AMET_pt, mg_AMET_pt_leg, heff_MET_pt, leg_MET_pt, trig, "MET (GeV)", "Efficiency", plotDir, sample, "MET_Pt", lepOpt, True)
        EffPlot(mg_AMET_phi, mg_AMET_phi_leg, heff_MET_phi, leg_MET_phi, trig, "MET phi", "Efficiency", plotDir, sample, "MET_Phi", lepOpt)
        EffPlot(mg_AMuon_pt, mg_AMuon_pt_leg, heff_Muon_pt, leg_Muon_pt, trig, "Muon Pt (GeV)", "Efficiency", plotDir, sample, "Muon_Pt", lepOpt)
        EffPlot(mg_AElectron_pt, mg_AElectron_pt_leg, heff_Electron_pt, leg_Electron_pt, trig, "Electron Pt (GeV)", "Efficiency", plotDir, sample, "Electron_Pt", lepOpt)
        EffPlot(mg_AltMET_pt, mg_AltMET_pt_leg, heff_AltMET_pt, leg_AltMET_pt, trig, "AltMET (GeV)", "Efficiency", plotDir, sample, "AltMET_Pt", lepOpt)
        EffPlot(mg_deltaMET_pt, mg_deltaMET_pt_leg, heff_deltaMET_pt, leg_deltaMET_pt, trig, "delta MET (GeV)", "Efficiency", plotDir, sample, "deltaMET_Pt", lepOpt)
        EffPlot(mg_deltaMET_rel_pt, mg_deltaMET_rel_pt_leg, heff_deltaMET_rel_pt, leg_deltaMET_rel_pt, trig, "delta MET rel (GeV)", "Efficiency", plotDir, sample, "deltaMET_rel_Pt", lepOpt)'''

    EffPlot(mg_MET_pt, mg_MET_pt_leg, heff_MET_pt, leg_MET_pt, trig, "MET (GeV)", "Efficiency", plotDir, sample, "MET_Pt", lepOpt, True)
    '''EffPlot(mg_HT, mg_HT_leg, heff_HT, leg_HT, trig, "HT (GeV)", "Efficiency", plotDir, sample, "HT", lepOpt)
    EffPlot(mg_jet1_pt, mg_jet1_pt_leg, heff_jet1_pt, leg_jet1_pt, trig, "Leading jet pt (GeV)", "Efficiency", plotDir, sample, "Jet1", lepOpt)
    EffPlot(mg_MET_phi, mg_MET_phi_leg, heff_MET_phi, leg_MET_phi, trig, "MET phi", "Efficiency", plotDir, sample, "MET_Phi", lepOpt)
    EffPlot(mg_Muon_pt, mg_Muon_pt_leg, heff_Muon_pt, leg_Muon_pt, trig, "Leading Muon Pt (GeV)", "Efficiency", plotDir, sample, "Muon_Pt1", lepOpt)
    EffPlot(mg_Electron_pt, mg_Electron_pt_leg, heff_Electron_pt, leg_Electron_pt, trig, "Leading Electron Pt (GeV)", "Efficiency", plotDir, sample, "Electron_Pt1", lepOpt)
    EffPlot(mg_LowPtEle_pt, mg_LowPtEle_pt_leg, heff_LowPtEle_pt, leg_LowPtEle_pt, trig, "Low Pt Electron Pt (GeV)", "Efficiency", plotDir, sample, "LowPtEle_Pt", lepOpt)
    EffPlot(mg_LowPtEle1_pt, mg_LowPtEle1_pt_leg, heff_LowPtEle1_pt, leg_LowPtEle1_pt, trig, "Leading Low Pt Electron Pt (GeV)", "Efficiency", plotDir, sample, "LowPtEle1_Pt", lepOpt)'''
'''#together plots
if trigger==Triggers:
    TogetherPlot(mg_MET_pt, mg_MET_pt_leg, "MET (GeV)", "Efficiency", "MET_Pt", plotDir, sample, lepOpt)
    TogetherPlot(mg_MET_phi, mg_MET_phi_leg, "MET phi", "Efficiency", "MET_Phi", plotDir, sample, lepOpt)
    TogetherPlot(mg_Muon_pt, mg_Muon_pt_leg, "Muon Pt (GeV)", "Efficiency", "Muon_Pt", plotDir, sample, lepOpt)
    TogetherPlot(mg_Electron_pt, mg_Electron_pt_leg, "Electron pt (GeV)", "Efficiency", "Electron_Pt", plotDir, sample, lepOpt)
    TogetherAltPlot(mg_AMET_pt, mg_AMET_pt_leg, "MET (GeV)", "Efficiency", "MET_Pt", plotDir, sample, lepOpt)
    TogetherAltPlot(mg_AMET_phi, mg_AMET_phi_leg, "MET phi", "Efficiency", "MET_Phi", plotDir, sample, lepOpt)
    TogetherAltPlot(mg_AMuon_pt, mg_AMuon_pt_leg, "Muon Pt (GeV)", "Efficiency", "Muon_Pt", plotDir, sample, lepOpt)
    TogetherAltPlot(mg_AElectron_pt, mg_AElectron_pt_leg, "Electron pt (GeV)", "Efficiency", "Electron_Pt", plotDir, sample, lepOpt)
    TogetherAltPlot(mg_AltMET_pt, mg_AltMET_pt_leg, "AltMET (GeV)", "Efficiency", "AltMET_Pt", plotDir, sample, lepOpt)
    TogetherAltPlot(mg_deltaMET_pt, mg_deltaMET_pt_leg, "delta MET (GeV)", "Efficiency", "deltaMET_Pt", plotDir, sample, lepOpt)
    TogetherAltPlot(mg_deltaMET_rel_pt, mg_deltaMET_rel_pt_leg, "delta MET rel (GeV)", "Efficiency", "deltaMET_rel_Pt", plotDir, sample, lepOpt)'''
hfile.Close()
