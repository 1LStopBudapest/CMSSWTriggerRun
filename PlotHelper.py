import os, sys
import ROOT
sys.path.append('../')
from Helper.CosmeticCode import *

def PlotNumDen(hist, trig, i, xtitle, ytitle, plotDir, sample, folder, filename):
    
    for k in range(hist[i+1].GetNbinsX()+1):
        newcontent = hist[i+1].GetBinContent(k)/hist[i+1].GetBinWidth(k)
        hist[i+1].SetBinContent(k, newcontent)
    
    ymin=hist[i].GetMinimum()*0.9
    ymax=hist[i+1].GetMaximum()*1.2
    if hist[i].GetMinimum() < hist[i+1].GetMaximum()/10: ymin=0
    hist[i+1].GetYaxis().SetRangeUser(ymin , ymax)
    hist[i+1].GetYaxis().SetTitle(ytitle)
    hist[i+1].GetXaxis().SetTitle(xtitle)
    c = ROOT.TCanvas('c', '', 600, 800)
    hist[i+1].SetLineColor(ROOT.kBlue)
    hist[i+1].Draw()
    ROOT.gPad.SetGrid()
                
    for k in range(hist[i].GetNbinsX()+1):
        newcontent = hist[i].GetBinContent(k)/hist[i].GetBinWidth(k)
        hist[i].SetBinContent(k, newcontent)
                  
    hist[i].SetLineColor(ROOT.kRed)
    hist[i].Draw("SAME")
    if 'NoMu' in trig:
        outPath=(plotDir+sample+"_AltMET/"+folder+"/")
    else:
        outPath=(plotDir+sample+"/"+folder+"/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+trig+"_"+filename+"_"+sample+".png")
    c.Close()
    
def NumDen2D(hist, trig, i, xtitle, ytitle, plotDir, sample, folder, filename):

    hist[i].GetYaxis().SetTitle(ytitle)
    hist[i].GetXaxis().SetTitle(xtitle)
    c = ROOT.TCanvas('c', '', 800, 800)
    hist[i].Draw("COLZ")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_AltMET/"+folder+"/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+trig+"_"+filename+"_num_"+sample+".png")
        
    hist[i+1].GetYaxis().SetTitle(ytitle)
    hist[i+1].GetXaxis().SetTitle(xtitle)
    c = ROOT.TCanvas('c', '', 800, 800)
    hist[i+1].Draw("COLZ")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_AltMET/"+folder+"/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+trig+"_"+filename+"_den_"+sample+".png")
    c.Close()
    
def EffPlot(t, tLeg, heff, hLeg, trig, xtitle, ytitle, plotDir, sample, folder, lepOpt, fit=False):

    t.Add(heff)
    tLeg.AddEntry(heff, trig ,"p")
    tLeg.SetTextSize(0.02)
    
    y=heff.GetY()
    ymin=min(y)*0.9
    ymax=max(y)*1.2
    if min(y) < max(y)/4 : ymin=0
    if (1-max(y)) < (max(y)-min(y))/5 : ymax=1.5
    heff.GetYaxis().SetRangeUser(0.0 , 1.5)
    heff.GetYaxis().SetTitle(ytitle)
    heff.GetXaxis().SetTitle(xtitle)
    heff.GetYaxis().SetTitleSize(0.05)
    heff.GetYaxis().SetTitleOffset(0.7)
    heff.GetYaxis().SetLabelSize(0.03)
    heff.GetXaxis().SetTitleSize(0.04)
    heff.GetXaxis().SetTitleOffset(0.8)
    heff.GetXaxis().SetLabelSize(0.04)
    heff.SetLineColor(ROOT.kBlack)
    heff.SetLineWidth(2)
    heff.SetMarkerSize(0.8)
    if 'Inclusive' in trig: heff.SetMarkerStyle(24)
    else: heff.SetMarkerStyle(20)
    heff.SetMarkerColor(ROOT.kBlack)
    hLeg.AddEntry(heff, trig ,"p")
    hLeg.SetTextSize(0.02)
    
    c = ROOT.TCanvas('c', '', 600, 800)
    heff.Draw("AP")
    hLeg.Draw("same")
    
    if fit==True:
        fitting = ROOT.TF1('fitting','(1-TMath::Erf(-(x - [0])/[1]))/[2]')
        fitting.SetParameters(160, 50, 2)
        #fitting.SetParLimits(1, 45, 45)
        #fitting.SetParLimits(0, 100, 100)
        fit = heff.Fit(fitting, 'S')
        #fit.SetLineColor(ROOT.kBlue)
        hLeg.AddEntry(fitting, 'Fitting', "l")
        fit.Draw("SAME")
        eff=2/fitting.GetParameter(2)
        text = ROOT.TText(350, 0.82, 'Eff: {:.3f}'.format(eff))
        text.SetTextColor(ROOT.kBlack)
        text.SetTextFont(43)
        text.SetTextSize(30)
        text.Draw("SAME")
    
    ROOT.gPad.SetGrid()
    if 'NoMu' in trig:
        outPath=(plotDir+sample+"_AltMET/"+folder+"/")
    else:
        outPath=(plotDir+sample+"/"+folder+"/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_"+folder+"_"+trig+"_"+lepOpt+".png")
    c.Close()

def TogetherPlot(t, tLeg, xtitle, ytitle, folder, plotDir, sample, lepOpt):
    
    ymin=t.GetHistogram().GetMinimum()*0.9
    ymax=t.GetHistogram().GetMaximum()*1.5
    if ymin < ymax/4 : ymin=0
    if (1-t.GetHistogram().GetMaximum()) < (t.GetHistogram().GetMaximum()-t.GetHistogram().GetMinimum())/5 : ymax=1.5
    t.GetYaxis().SetRangeUser(ymin , ymax)
    t.GetYaxis().SetTitle(ytitle)
    t.GetXaxis().SetTitle(xtitle)
    t.GetYaxis().SetTitleSize(0.05)
    t.GetYaxis().SetTitleOffset(0.7)
    t.GetYaxis().SetLabelSize(0.03)
    t.GetXaxis().SetTitleSize(0.04)
    t.GetXaxis().SetTitleOffset(0.8)
    t.GetXaxis().SetLabelSize(0.04)
    tLeg.SetTextSize(0.03)
    c = ROOT.TCanvas('c', '', 600, 800)
    t.Draw("AP")
    tLeg.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"/"+folder+"/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_"+folder+"_together_"+lepOpt+".png")
    c.Close()

def TogetherAltPlot(t, tLeg, xtitle, ytitle, folder, plotDir, sample, lepOpt):
    
    ymin=t.GetHistogram().GetMinimum()*0.9
    ymax=t.GetHistogram().GetMaximum()*1.5
    if ymin < ymax/4 : ymin=0
    if (1-t.GetHistogram().GetMaximum()) < (t.GetHistogram().GetMaximum()-t.GetHistogram().GetMinimum())/5 : ymax=1.5
    t.GetYaxis().SetRangeUser(ymin , ymax)
    t.GetYaxis().SetTitle(ytitle)
    t.GetXaxis().SetTitle(xtitle)
    t.GetYaxis().SetTitleSize(0.05)
    t.GetYaxis().SetTitleOffset(0.7)
    t.GetYaxis().SetLabelSize(0.03)
    t.GetXaxis().SetTitleSize(0.04)
    t.GetXaxis().SetTitleOffset(0.8)
    t.GetXaxis().SetLabelSize(0.04)
    tLeg.SetTextSize(0.03)
    c = ROOT.TCanvas('c', '', 600, 800)
    t.Draw("AP")
    tLeg.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_AltMET/"+folder+"/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_"+folder+"_together_"+lepOpt+".png")
    c.Close()
