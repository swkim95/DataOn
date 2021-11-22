#!/usr/bin/env python
from ROOT import *

gROOT.ProcessLine(".x setTDRStyle.C")

gObjects = []

def makeMode():
    mode = [
        "cktpt",
        "eta",
        "trackerLayers",
        "pixelHits",
        "RelIso",
        "dxyVTX",
        "dzVTX",
        "muonHits",
        "nMatches",
        "cktptReso",
    ]
    return mode

def DrawHist(hdata, hmc, higgsName, dyName, muCharge, mode):
    hdata.SetLineColor(kBlue);
    hdata.SetLineWidth(2);
    hmc.SetLineColor(kRed);
    hmc.SetLineWidth(2);
    
    # Normalize to the number of data
    hmc.Scale(hdata.Integral()/hmc.Integral());
    
    c1 = TCanvas("c1", "c1", 1000, 1000);
    gObjects.append(c1)
    c1.cd();
    c1.SetLogy();
    c1_1 = TPad("padc1_1","padc1_1",0.01,0.05,0.99,0.99);
    gObjects.append(c1_1)
    c1_1.Draw();
    c1_1.cd();
    c1_1.SetTopMargin(0.01);
    c1_1.SetBottomMargin(0.3);
    c1_1.SetRightMargin(0.1);
    c1_1.SetLeftMargin(0.109);
    c1_1.SetFillStyle(0);
    
    if (higgsName == "Higgs2mumu_Run2012_MuPlus_cktpt" or higgsName == "Higgs2mumu_Run2012_MuMinus_cktpt"):
      hmc.SetTitle("CMS Preliminary at #sqrt{s} = 8 TeV, " + muCharge + mode);
      hmc.Draw("hist");
      hmc.SetLabelSize(0.0);
      hmc.GetYaxis().SetTitleOffset(1.5);
      hmc.GetYaxis().SetTitle("Events");
      hmc.Draw("histsame");
      hdata.Draw("histsame");
    else:
      hdata.SetTitle("CMS Preliminary at #sqrt{s} = 8 TeV, " + muCharge + mode);
      hdata.Draw("hist");
      hdata.SetLabelSize(0.0);
      hdata.GetYaxis().SetTitleOffset(1.5);
      hdata.GetYaxis().SetTitle("Events");
      hmc.Draw("histsame");
      hdata.Draw("histsame");
    
    legend = TLegend(0.80, 0.80, 0.90, 0.90);
    gObjects.append(legend)
    legend.AddEntry(hdata, "Higgs", "l");
    legend.AddEntry(hmc, "DY", "l");
    legend.SetFillColor(0);
    legend.Draw("0");
    
    c1_2 = TPad("padc1_2","padc1_2",0.01,0.05,0.99,0.32);
    gObjects.append(legend)
    c1_2.Draw();
    c1_2.cd();
    c1_2.SetTopMargin(0.1);
    c1_2.SetBottomMargin(0.30);
    c1_2.SetRightMargin(0.091);
    c1_2.SetFillStyle(0);
    c1_2.SetGrid();
    hratio = hdata.Clone();
    gObjects.append(hratio)
    hdata.Sumw2();
    hmc.Sumw2();
    hratio.Divide(hdata, hmc);
    hratio.GetXaxis().SetTitle(mode);
    hratio.SetTitle("");
    hratio.GetXaxis().SetMoreLogLabels();
    hratio.GetXaxis().SetNoExponent();
    hratio.GetYaxis().SetTitle("data/MC");
    hratio.GetXaxis().SetTitleSize(0.13);
    hratio.GetYaxis().SetTitleSize(0.09);
    hratio.GetYaxis().SetTitleOffset(0.4);
    hratio.GetXaxis().SetLabelSize(0.11);
    hratio.GetYaxis().SetLabelSize(0.07);
    
    gStyle.SetOptFit(0);
    hratio.SetMaximum(2.0);
    hratio.SetMinimum(0.0);
    hratio.SetMarkerSize(0.5);
    hratio.Draw("e1p");
    hratio.Fit("pol0");
    c1.SaveAs("hist_plots/Histogram_"+ muCharge + mode + ".png");

    c1.Clear();

def drawPlots():
    gStyle.SetOptStat(0);

    # Directory of ROOT file containing histograms
    f1 = TFile("/home/sjws5411/workspace/MyFiles/variableSpec_mumu_pt30.root");
    gObjects.append(f1)
    f1.cd();

    mode = makeMode();
    print(mode[0])

    higgs = "Higgs2mumu_Run2012_";
    dy = "DYJets_";
    muPlus = "MuPlus_";
    muMinus = "MuMinus_";
    
    higgsPlusName = higgs + muPlus;
    higgsMinusName = higgs + muMinus;
    dyPlusName = dy + muPlus;
    dyMinusName = dy + muMinus;
    
    hdata = f1.Get("Higgs2mumu_Run2012_diMuonMass");
    hmc = f1.Get("DYJets_diMuonMass");
    print("nevents = (Higgs2mumu): ", hdata.Integral(), ";; (DY2mumu): ", hmc.Integral())

    #HiggsDimuonMass = "Higgs2mumu_Run2012_diMuonMass";
    #DYDimuonMass = "DYJets_diMuonMass";
    #dimuonCharge = " ";
    #dimuonMode = "diMuonMass";

    #DrawHist(hdata, hmc, HiggsDimuonMass, DYDimuonMass, dimuonCharge, dimuonMode);

    DrawHist(hdata, hmc, "Higgs2mumu_Run2012_diMuonMass", "DYJets_diMuonMass", " ", "diMuonMass")

    for i in range(len(mode)):
      
      higgsHistNamePlus = higgsPlusName + mode[i]; 
      higgsHistNameMinus = higgsMinusName + mode[i];

      dyHistNamePlus = dyPlusName + mode[i];
      dyHistNameMinus = dyMinusName + mode[i];

      hdata_plus = f1.Get(higgsHistNamePlus);
      hmc_plus = f1.Get(dyHistNamePlus);
      print("nevents = (data): ", hdata_plus.Integral(), ";; (DY MC): ", hmc_plus.Integral())
      DrawHist(hdata_plus, hmc_plus, higgsHistNamePlus, dyHistNamePlus, muPlus, mode[i]);
      
      hdata_minus = f1.Get(higgsHistNameMinus);
      hmc_minus = f1.Get(dyHistNameMinus);
      print("nevents = (data): ", hdata_minus.Integral(), ";; (DY MC): ", hmc_minus.Integral())
      DrawHist(hdata_minus, hmc_minus, higgsHistNameMinus, dyHistNameMinus, muMinus, mode[i]);

    f1.Close();

drawPlots()