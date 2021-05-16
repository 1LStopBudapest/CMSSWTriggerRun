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



def get_parser():
    ''' Argument parser.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--sample',           action='store',                     type=str,            default='SingleElectron_Run2016B',                                help="Which sample?" )
    argParser.add_argument('--year',             action='store',                     type=int,            default=2016,                                             help="Which year?" )
    argParser.add_argument('--channel',             action='store',                  type=str,            default='SingleElectron',                                   help="Which dataset?" )
    argParser.add_argument('--startfile',        action='store',                     type=int,            default=0,                                                help="start from which root file like 0th or 10th etc?" )
    argParser.add_argument('--nfiles',           action='store',                     type=int,            default=-1,                                               help="No of files to run. -1 means all files" )
    argParser.add_argument('--nevents',           action='store',                    type=int,            default=-1,                                               help="No of events to run. -1 means all events" )
    argParser.add_argument('--jtype',           action='store',                    type=str,              default='local',                                               help="if running in condor" )
    

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
elif year==2017:
    samplelist = samples_2017
    DataLumi = SampleChain.luminosity_2017
else:
    samplelist = samples_2018
    DataLumi = SampleChain.luminosity_2018

    
denTrig = SingleEleTrigger if 'Electron' in channel else SingleMuTrigger
lepOpt = 'Ele' if 'Electron' in channel else 'Mu'

numTrigHist = dict((key, 'hMET_'+key) for key in METTriggers)

fileExt = options.startfile/options.nfiles if 'condor' in jtype else options.startfile

if isinstance(samplelist[samples], types.ListType):
    histext = samples
    for s in samplelist[samples]:
        sample = list(samplelist.keys())[list(samplelist.values()).index(s)]
        print 'running over: ', sample
        hfile = ROOT.TFile( 'TrigHist_'+sample+'_%i'%(fileExt)+'.root', 'RECREATE')
        histos = {}
        for key in numTrigHist:
            histos[numTrigHist[key]+'_den'] = HistInfo(hname = numTrigHist[key]+'_den', sample = histext, binning=[100,0,500], histclass = ROOT.TH1F).make_hist()
            histos[numTrigHist[key]+'_num'] = HistInfo(hname = numTrigHist[key]+'_num', sample = histext, binning=[100,0,500], histclass = ROOT.TH1F).make_hist()
        
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
            presel = getTrig.ISRcut(100) and getTrig.HTcut(200)
            #Single lep Selection
            lepsel = getTrig.Lepcut(lepOpt) and getTrig.XtraLepVeto(lepOpt)
            filtrsel = getTrig.passfilters()
            if presel and lepsel and filtrsel:
                for trig, hist in numTrigHist.items():
                    #den trig cut
                    if(getTrig.passLepTrig(denTrig, lepOpt)):
                        histos[hist+'_den'].Fill(ch.MET_pt)
                        #num trig cut
                        if(getTrig.passMETTrig(trig)):
                            histos[hist+'_num'].Fill(ch.MET_pt)
            
        hfile.Write()
else:
    histext = samples
    for l in list(samplelist.values()):
        if samplelist[samples] in l: histext = list(samplelist.keys())[list(samplelist.values()).index(l)]
    sample = samples
    print 'running over: ', sample
    hfile = ROOT.TFile( 'TrigHist_'+sample+'_%i'%(fileExt)+'.root', 'RECREATE')
    histos = {}
    for key in numTrigHist:
        histos[numTrigHist[key]+'_den'] = HistInfo(hname = numTrigHist[key]+'_den', sample = histext, binning=[100,0,500], histclass = ROOT.TH1F).make_hist()
        histos[numTrigHist[key]+'_num'] = HistInfo(hname = numTrigHist[key]+'_num', sample = histext, binning=[100,0,500], histclass = ROOT.TH1F).make_hist()
    
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
        presel = getTrig.ISRcut(100) and getTrig.HTcut(200)
        #Single lep Selection
        lepsel = getTrig.Lepcut(lepOpt) and getTrig.XtraLepVeto(lepOpt)
        filtrsel = getTrig.passfilters()
        if presel and lepsel and filtrsel:
            for trig, hist in numTrigHist.items():
                #den trig cut
                if(getTrig.passLepTrig(denTrig, lepOpt)):
                    histos[hist+'_den'].Fill(ch.MET_pt)
                    #num trig cut
                    if(getTrig.passMETTrig(trig)):
                        histos[hist+'_num'].Fill(ch.MET_pt)
                    
    hfile.Write()
