import os, sys
import ROOT
import types

from TrigVarSel import TrigVarSel
from TriggerList import *

from SampleChain import SampleChain
from FileList_2016 import samples as samples_2016
from FileList_2017 import samples as samples_2017
from FileList_2018 import samples as samples_2018
sys.path.append('../')
from Helper.HistInfo import HistInfo
from Helper.VarCalc import AltMETCalc


def get_parser():
    ''' Argument parser.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--sample',           action='store',                     type=str,            default='SingleMuon_Data2018',                                help="Which sample?" )
    argParser.add_argument('--year',             action='store',                     type=int,            default=2018,                                             help="Which year?" )
    argParser.add_argument('--channel',             action='store',                  type=str,            default='SingleMuon',                                   help="Which dataset?" )
    argParser.add_argument('--startfile',        action='store',                     type=int,            default=330,                                                help="start from which root file like 0th or 10th etc?" )
    argParser.add_argument('--nfiles',           action='store',                     type=int,            default=1,                                               help="No of files to run. -1 means all files" )
    argParser.add_argument('--nevents',           action='store',                    type=int,            default=-1,                                               help="No of events to run. -1 means all events" )
    argParser.add_argument('--jtype',           action='store',                    type=str,              default='local',                                               help="if running in condor" )
    #argParser.add_argument('--trigger',           action='store',                    type=str,            default='AltMETTriggers',                                  help="Which triggers?")

    return argParser

options = get_parser().parse_args()


samples  = options.sample
channel = options.channel
nEvents = options.nevents
year = options.year
jtype = options.jtype

isData = True if ('Run' in samples or 'Data' in samples) else False
DataLumi=1.0

if year==2016:
    samplelist = samples_2016
    DataLumi = SampleChain.luminosity_2016
    SingleEleTrigger = SingleEleTrigger_2016
    pTthr = 30
elif year==2017:
    samplelist = samples_2017
    DataLumi = SampleChain.luminosity_2017
    SingleEleTrigger = SingleEleTrigger_2017
    pTthr = 40
else:
    samplelist = samples_2018
    DataLumi = SampleChain.luminosity_2018
    SingleEleTrigger = SingleEleTrigger_2018
    pTthr = 40

    
denTrig = SingleEleTrigger if 'Electron' in channel else SingleMuTrigger
lepOpt = 'Ele' if 'Electron' in channel else 'Mu'

numTrigHist = dict((key, 'hMET_'+key) for key in MET120Triggers)

fileExt = options.startfile/options.nfiles if 'condor' in jtype else options.startfile

if isinstance(samplelist[samples], types.ListType):
    for s in samplelist[samples]:
        sample = list(samplelist.keys())[list(samplelist.values()).index(s)]
        print 'running over: ', sample
        histext = sample
        hfile = ROOT.TFile('TrigHist_'+sample+'_%i'%(fileExt)+'.root', 'RECREATE')
        histos = {}
        for key in numTrigHist:
            histos[numTrigHist[key]+'_MET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_MET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_HT_den'] = HistInfo(hname = numTrigHist[key]+'_HT_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_HT_num'] = HistInfo(hname = numTrigHist[key]+'_HT_num', sample = histext,  binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_jet1_pt_num'] = HistInfo(hname = numTrigHist[key]+'_jet1_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_jet1_pt_den'] = HistInfo(hname = numTrigHist[key]+'_jet1_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_MET_phi_den'] = HistInfo(hname = numTrigHist[key]+'_MET_phi_den', sample = histext, binning=[-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_MET_phi_num'] = HistInfo(hname = numTrigHist[key]+'_MET_phi_num', sample = histext, binning=[-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_Muon_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_Muon_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_Electron_pt_den'] = HistInfo(hname = numTrigHist[key]+'_Electron_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_Electron_pt_num'] = HistInfo(hname = numTrigHist[key]+'_Electron_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_LowPtEle_pt_num'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_LowPtEle_pt_den'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_LowPtEle1_pt_num'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle1_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_LowPtEle1_pt_den'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle1_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
            if 'NoMu' in key:
                histos[numTrigHist[key]+'_AltMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
                histos[numTrigHist[key]+'_AltMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
                histos[numTrigHist[key]+'_deltaMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_den', sample = histext, binning=[0,20,40,60,80,100,120,140,160,200,300,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
                histos[numTrigHist[key]+'_deltaMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_num', sample = histext, binning=[0,20,40,60,80,100,120,140,160,200,300,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
                histos[numTrigHist[key]+'_deltaMET_rel_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_rel_pt_den', sample = histext, binning=[0,0.2,0.4,0.6,0.8,1], histclass = ROOT.TH1F, binopt='').make_hist()
                histos[numTrigHist[key]+'_deltaMET_rel_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_rel_pt_num', sample = histext, binning=[0,0.2,0.4,0.6,0.8,1], histclass = ROOT.TH1F, binopt='').make_hist()
                histos[numTrigHist[key]+'_MET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_Muon_pt_den', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
                histos[numTrigHist[key]+'_MET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_Muon_pt_num', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
                histos[numTrigHist[key]+'_MET_pt_AltMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_AltMET_pt_den', sample = histext, binning=[[15,0,500],[15,0,500]], histclass = ROOT.TH2F, binopt='').make_hist()
                histos[numTrigHist[key]+'_MET_pt_AltMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_AltMET_pt_num', sample = histext, binning=[[15,0,500],[15,0,500]], histclass = ROOT.TH2F, binopt='').make_hist()
                histos[numTrigHist[key]+'_AltMET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_Muon_pt_den', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
                histos[numTrigHist[key]+'_AltMET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_Muon_pt_num', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
                histos[numTrigHist[key]+'_deltaMET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_Muon_pt_den', sample = histext, binning=[[12,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
                histos[numTrigHist[key]+'_deltaMET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_Muon_pt_num', sample = histext, binning=[[12,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
        
        ch = SampleChain(sample, options.startfile, options.nfiles, year).getchain()
        print 'Total events of selected files of the', sample, 'sample: ', ch.GetEntries()
        n_entries = ch.GetEntries()
        nevtcut = n_entries -1 if nEvents == - 1 else nEvents - 1
        print 'Running over total events: ', nevtcut+1
        for ientry in range(n_entries):
            if ientry > nevtcut: break
            if ientry % (nevtcut/10)==0 : print 'processing ', ientry,'th event'
            ch.GetEntry(ientry)
            getTrig = TrigVarSel(ch, sample)
            presel = getTrig.ISRcut(100) and getTrig.HTcut(300)
            #Single lep Selection
            lepsel = getTrig.Lepcut(lepOpt, pTthr) and getTrig.XtraLepVeto(lepOpt)
            filtrsel = getTrig.passfilters()
            if presel and lepsel and filtrsel:
                for trig, hist in numTrigHist.items():
                    #den trig cut
                    if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                        histos[hist+'_MET_pt_den'].Fill(ch.MET_pt)
                        #AltMETTriggers
                        if 'NoMu' in trig:                            
                            for i in range(ch.nMuon):
                                altMET_pt = AltMETCalc(ch.Muon_pt[i], ch.Muon_eta[i], ch.Muon_phi[i],  ch.Muon_mass[i], ch.MET_pt, ch.MET_phi).Pt()
                                histos[hist+'_MET_pt_Muon_pt_den'].Fill(ch.MET_pt, ch.Muon_pt[i])
                                histos[hist+'_MET_pt_AltMET_pt_den'].Fill(ch.MET_pt, altMET_pt)
                                histos[hist+'_AltMET_pt_Muon_pt_den'].Fill(altMET_pt, ch.Muon_pt[i])
                                histos[hist+'_deltaMET_pt_Muon_pt_den'].Fill(altMET_pt-ch.MET_pt,  ch.Muon_pt[i])
                                histos[hist+'_AltMET_pt_den'].Fill(altMET_pt)
                                histos[hist+'_deltaMET_pt_den'].Fill(altMET_pt-ch.MET_pt)
                                histos[hist+'_deltaMET_rel_pt_den'].Fill((altMET_pt-ch.MET_pt)/ch.MET_pt)
                            #num trig cut
                        if(getTrig.passMETTrig(trig)):
                            histos[hist+'_MET_pt_num'].Fill(ch.MET_pt)
                            #AltMETTriggers
                            if 'NoMu' in trig:
                                histos[hist+'_MET_pt_num'].Fill(ch.MET_pt)
                                for i in range(ch.nMuon):
                                    altMET_pt = AltMETCalc(ch.Muon_pt[i], ch.Muon_eta[i], ch.Muon_phi[i], ch.Muon_mass[i], ch.MET_pt, ch.MET_phi).Pt()
                                    histos[hist+'_MET_pt_Muon_pt_num'].Fill(ch.MET_pt, ch.Muon_pt[i])
                                    histos[hist+'_MET_pt_AltMET_pt_num'].Fill(ch.MET_pt, altMET_pt)
                                    histos[hist+'_AltMET_pt_Muon_pt_num'].Fill(altMET_pt, ch.Muon_pt[i])
                                    histos[hist+'_deltaMET_pt_Muon_pt_num'].Fill(altMET_pt-ch.MET_pt, ch.Muon_pt[i])
                                    histos[hist+'_AltMET_pt_num'].Fill(altMET_pt)
                                    histos[hist+'_deltaMET_pt_num'].Fill(altMET_pt-ch.MET_pt)
                                    histos[hist+'_deltaMET_rel_pt_num'].Fill((altMET_pt-ch.MET_pt)/ch.MET_pt)
            
            # MET phi                        
            presel = getTrig.ISRcut(100) and getTrig.HTcut(300) and getTrig.METcut(200)
            if presel and lepsel and filtrsel:
                for trig, hist in numTrigHist.items():
                    #den trig cut
                    if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                        histos[hist+'_MET_phi_den'].Fill(ch.MET_phi)
                        #num trig cut
                        if(getTrig.passMETTrig(trig)):
                            histos[hist+'_MET_phi_num'].Fill(ch.MET_phi)
                            
            # lepton pt & low pt electron
            if presel and filtrsel:
                for trig, hist in numTrigHist.items():
                    #den trig cut
                    if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                        for i in range(ch.nElectron):
                            histos[hist+'_Electron_pt_den'].Fill(ch.Electron_pt[i])
                        if ch.Electron_pt:
                            histos[hist+'_Electron_pt_den'].Fill(ch.Electron_pt[0])
                        if ch.Muon_pt:
                            histos[hist+'_Muon_pt_den'].Fill(ch.Muon_pt[0])
                        if ch.LowPtElectron_pt:
                            histos[hist+'_LowPtEle_pt_den'].Fill(ch.LowPtElectron_pt[i])
                        for i in range(ch.nLowPtElectron):
                            histos[hist+'_LowPtEle1_pt_den'].Fill(max(ch.LowPtElectron_pt))
                        #num trig cut
                        if(getTrig.passMETTrig(trig)):
                            for i in range(ch.nElectron):
                                histos[hist+'_Electron_pt_num'].Fill(ch.Electron_pt[i])
                            if ch.Electron_pt:
                                histos[hist+'_Electron_pt_num'].Fill(ch.Electron_pt[0])
                            if ch.Muon_pt:
                                histos[hist+'_Muon_pt_num'].Fill(ch.Muon_pt[0])
                            if ch.LowPtElectron_pt:
                                histos[hist+'_LowPtEle1_pt_num'].Fill(max(ch.LowPtElectron_pt))
                            for i in range(ch.nLowPtElectron):
                                histos[hist+'_LowPtEle_pt_num'].Fill(ch.LowPtElectron_pt[i])
    
            # HT
            presel = getTrig.ISRcut(100) and getTrig.METcut(200)                    
            if lepsel and filtrsel and presel:
                for trig, hist in numTrigHist.items():
                    #den trig cut
                    if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                        histos[hist+'_HT_den'].Fill(getTrig.calHT())
                        #num trig cut
                        if(getTrig.passMETTrig(trig)):
                            histos[hist+'_HT_num'].Fill(getTrig.calHT())
                           
            # leading jet pt
            presel = getTrig.METcut(200) and getTrig.HTcut(300)
            if lepsel and filtrsel and presel:
                for trig, hist in numTrigHist.items():
                    #den trig cut
                    if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                        histos[hist+'_jet1_pt_den'].Fill(getTrig.leadingJet())
                        #num trig cut
                        if(getTrig.passMETTrig(trig)):
                            histos[hist+'_jet1_pt_num'].Fill(getTrig.leadingJet())
            

        hfile.Write()
            
else:
    for l in list(samplelist.values()):
        if samplelist[samples] in l: histext = list(samplelist.keys())[list(samplelist.values()).index(l)]
    sample = samples
    histext = sample
    print 'running over: ', sample
    hfile = ROOT.TFile('TrigHist_'+sample+'_%i'%(fileExt)+'.root', 'RECREATE')
    histos = {}
    for key in numTrigHist:
        histos[numTrigHist[key]+'_MET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_MET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_HT_den'] = HistInfo(hname = numTrigHist[key]+'_HT_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_HT_num'] = HistInfo(hname = numTrigHist[key]+'_HT_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_jet1_pt_num'] = HistInfo(hname = numTrigHist[key]+'_jet1_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_jet1_pt_den'] = HistInfo(hname = numTrigHist[key]+'_jet1_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_MET_phi_den'] = HistInfo(hname = numTrigHist[key]+'_MET_phi_den', sample = histext, binning=[-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_MET_phi_num'] = HistInfo(hname = numTrigHist[key]+'_MET_phi_num', sample = histext, binning=[-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_Muon_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_Muon_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_Electron_pt_den'] = HistInfo(hname = numTrigHist[key]+'_Electron_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_Electron_pt_num'] = HistInfo(hname = numTrigHist[key]+'_Electron_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_LowPtEle_pt_num'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_LowPtEle_pt_den'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_LowPtEle1_pt_num'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle1_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_LowPtEle1_pt_den'] = HistInfo(hname = numTrigHist[key]+'_LowPtEle1_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
        if 'NoMu' in key:
            histos[numTrigHist[key]+'_AltMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_AltMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_deltaMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_den', sample = histext, binning=[0,20,40,60,80,100,120,140,160,200,300,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_deltaMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_num', sample = histext, binning=[0,20,40,60,80,100,120,140,160,200,300,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_deltaMET_rel_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_rel_pt_den', sample = histext, binning=[0,0.2,0.4,0.6,0.8,1], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_deltaMET_rel_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_rel_pt_num', sample = histext, binning=[0,0.2,0.4,0.6,0.8,1], histclass = ROOT.TH1F, binopt='').make_hist()
            histos[numTrigHist[key]+'_MET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_Muon_pt_den', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
            histos[numTrigHist[key]+'_MET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_Muon_pt_num', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
            histos[numTrigHist[key]+'_MET_pt_AltMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_AltMET_pt_den', sample = histext, binning=[[15,0,500],[15,0,500]], histclass = ROOT.TH2F, binopt='').make_hist()
            histos[numTrigHist[key]+'_MET_pt_AltMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_AltMET_pt_num', sample = histext, binning=[[15,0,500],[15,0,500]], histclass = ROOT.TH2F, binopt='').make_hist()
            histos[numTrigHist[key]+'_AltMET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_Muon_pt_den', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
            histos[numTrigHist[key]+'_AltMET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_Muon_pt_num', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
            histos[numTrigHist[key]+'_deltaMET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_Muon_pt_den', sample = histext, binning=[[12,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
            histos[numTrigHist[key]+'_deltaMET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_Muon_pt_num', sample = histext, binning=[[12,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
    
    ch = SampleChain(sample, options.startfile, options.nfiles, year).getchain()
    print 'Total events of selected files of the', sample, 'sample: ', ch.GetEntries()
    n_entries = ch.GetEntries()
    nevtcut = n_entries -1 if nEvents == - 1 else nEvents - 1
    print 'Running over total events: ', nevtcut+1
    for ientry in range(n_entries):
        if ientry > nevtcut: break
        if nevtcut>10 and ientry % (nevtcut/10)==0 : print 'processing ', ientry,'th event'
        ch.GetEntry(ientry)
        getTrig = TrigVarSel(ch, sample)
        presel = getTrig.ISRcut(100) and getTrig.HTcut(300)
        #Single lep Selection
        lepsel = getTrig.Lepcut(lepOpt, pTthr) and getTrig.XtraLepVeto(lepOpt)
        filtrsel = getTrig.passfilters()
        
        #MET & AltMET & other yummy histos
        if presel and lepsel and filtrsel:
            for trig, hist in numTrigHist.items():
                   
                #den trig cut
                if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                    histos[hist+'_MET_pt_den'].Fill(ch.MET_pt)
                    #AltMETTriggers
                    if'NoMu' in trig:
                        histos[hist+'_MET_pt_den'].Fill(ch.MET_pt)    
                        for i in range(ch.nMuon):    
                            altMET_pt = AltMETCalc(ch.Muon_pt[i], ch.Muon_eta[i], ch.Muon_phi[i], ch.Muon_mass[i], ch.MET_pt, ch.MET_phi).Pt()
                            histos[hist+'_MET_pt_Muon_pt_den'].Fill(ch.MET_pt, ch.Muon_pt[i])
                            histos[hist+'_MET_pt_AltMET_pt_den'].Fill(ch.MET_pt, altMET_pt)
                            histos[hist+'_AltMET_pt_Muon_pt_den'].Fill(altMET_pt, ch.Muon_pt[i])
                            histos[hist+'_deltaMET_pt_Muon_pt_den'].Fill(altMET_pt-ch.MET_pt, ch.Muon_pt[i])
                            histos[hist+'_AltMET_pt_den'].Fill(altMET_pt)
                            histos[hist+'_deltaMET_pt_den'].Fill(altMET_pt-ch.MET_pt)
                            histos[hist+'_deltaMET_rel_pt_den'].Fill((altMET_pt-ch.MET_pt)/ch.MET_pt)
                    #num trig cut
                    if(getTrig.passMETTrig(trig)):
                        histos[hist+'_MET_pt_num'].Fill(ch.MET_pt)
                        #AltMETTriggers
                        if 'NoMu' in trig:
                            histos[hist+'_MET_pt_num'].Fill(ch.MET_pt)
                            for i in range(ch.nMuon):
                                altMET_pt = AltMETCalc(ch.Muon_pt[i], ch.Muon_eta[i], ch.Muon_phi[i], ch.Muon_mass[i], ch.MET_pt, ch.MET_phi).Pt()
                                histos[hist+'_MET_pt_Muon_pt_num'].Fill(ch.MET_pt, ch.Muon_pt[i])
                                histos[hist+'_MET_pt_AltMET_pt_num'].Fill(ch.MET_pt, altMET_pt)
                                histos[hist+'_AltMET_pt_Muon_pt_num'].Fill(altMET_pt, ch.Muon_pt[i])
                                histos[hist+'_deltaMET_pt_Muon_pt_num'].Fill(altMET_pt-ch.MET_pt, ch.Muon_pt[i])
                                histos[hist+'_AltMET_pt_num'].Fill(altMET_pt)
                                histos[hist+'_deltaMET_pt_num'].Fill(altMET_pt-ch.MET_pt)
                                histos[hist+'_deltaMET_rel_pt_num'].Fill((altMET_pt-ch.MET_pt)/ch.MET_pt)
                
        
        # MET phi                        
        presel = getTrig.ISRcut(100) and getTrig.HTcut(300) and getTrig.METcut(200)
        if presel and lepsel and filtrsel:
            for trig, hist in numTrigHist.items():
                #den trig cut
                if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                    histos[hist+'_MET_phi_den'].Fill(ch.MET_phi)
                    #num trig cut
                    if(getTrig.passMETTrig(trig)):
                        histos[hist+'_MET_phi_num'].Fill(ch.MET_phi)
                            
        # lepton pt & low pt electron
        if presel and filtrsel:
            for trig, hist in numTrigHist.items():
                #den trig cut
                if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                    for i in range(ch.nElectron):
                        histos[hist+'_Electron_pt_den'].Fill(ch.Electron_pt[i])
                    if ch.Electron_pt:
                        histos[hist+'_Electron_pt_den'].Fill(ch.Electron_pt[0])
                    if ch.Muon_pt:
                        histos[hist+'_Muon_pt_den'].Fill(ch.Muon_pt[0])
                    if ch.LowPtElectron_pt:
                        histos[hist+'_LowPtEle1_pt_den'].Fill(max(ch.LowPtElectron_pt))
                    for i in range(ch.nLowPtElectron):
                        histos[hist+'_LowPtEle_pt_den'].Fill(ch.LowPtElectron_pt[i])
                    #num trig cut
                    if(getTrig.passMETTrig(trig)):
                        for i in range(ch.nElectron):
                            histos[hist+'_Electron_pt_num'].Fill(ch.Electron_pt[i])
                        if ch.Electron_pt:
                            histos[hist+'_Electron_pt_num'].Fill(ch.Electron_pt[0])
                        if ch.Muon_pt:
                            histos[hist+'_Muon_pt_num'].Fill(ch.Muon_pt[0])
                        if ch.LowPtElectron_pt:
                            histos[hist+'_LowPtEle1_pt_num'].Fill(max(ch.LowPtElectron_pt))
                        for i in range(ch.nLowPtElectron):
                            histos[hist+'_LowPtEle_pt_num'].Fill(ch.LowPtElectron_pt[i])
                    
                    
        # HT            
        presel = getTrig.ISRcut(100) and getTrig.METcut(200)
        if lepsel and filtrsel and presel:
            for trig, hist in numTrigHist.items():
                #den trig cut
                if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                    histos[hist+'_HT_den'].Fill(getTrig.calHT())
                    #num trig cut
                    if(getTrig.passMETTrig(trig)):
                        histos[hist+'_HT_num'].Fill(getTrig.calHT())
        
        # leading jet pt
        presel = getTrig.METcut(200) and getTrig.HTcut(300)
        if lepsel and filtrsel and presel:
            for trig, hist in numTrigHist.items():
                #den trig cut
                if(getTrig.passLepTrig(denTrig, lepOpt, year)):
                    histos[hist+'_jet1_pt_den'].Fill(getTrig.leadingJet())
                    #num trig cut
                    if(getTrig.passMETTrig(trig)):
                        histos[hist+'_jet1_pt_num'].Fill(getTrig.leadingJet())
                        
        
        
    hfile.Write()
    
