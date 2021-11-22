#!/usr/bin/env python
from ROOT import TLorentzVector
import uproot
from math import sqrt
import numpy as np

class GoodMuonSelector():
    def __init__(self):
        self.ptCut = 30.0 # GeV
        self.etaCut = 2.4 # pseudorapidity
        self.MuMass = 0.105658 # muon mass in GeV
        self.trigName = "HLT_IsoMu24_eta2p1_v*" # HLT name
        
    def isFired(self, evtNum, hlt_ntrig, hlt_trigname, hlt_trigfired):
        Fired = False
        
        for trigNum in range(hlt_ntrig[evtNum]):
            if self.trigName == hlt_trigname[evtNum][trigNum]:
                if hlt_trigfired[evtNum][trigNum] == 1 :
                    Fired = True
                    break
        return Fired
    
    def fourVectorMass(self, fVector):
        px = fVector.Px()
        py = fVector.Py()
        pz = fVector.Pz()
        e  = fVector.E()
        vec = TLorentzVector()
        vec.SetPxPyPzE(px, py, pz, e)
        return vec.M()
    
    def goodMuon(self, charge, cktpT, eta, RelIso, pTReso, trackerLayers, muonHits, pixelHits, dxyVTX, dzVTX, nMatches, muonType, px, py, pz ):
        muPlus = []
        muMinus = []

        muPlusData = []
        muMinusData = []
        
        arr_cktpT = np.array([])
        arr_eta = np.array([])
        arr_RelIso = np.array([])
        arr_pTReso = np.array([])
        arr_muonHits = np.array([])
        arr_dimuonMass = np.array([])
            
        for muNum in range(len(charge)):
            e = sqrt(self.MuMass*self.MuMass + px[muNum]*px[muNum] + py[muNum]*py[muNum] + pz[muNum]*pz[muNum])
            tmpMuon = TLorentzVector()
            tmpMuon.SetPxPyPzE(px[muNum], py[muNum], pz[muNum], e)
            
            arr_cktpT = np.array([])
            arr_eta = np.array([])
            arr_RelIso = np.array([])
            arr_pTReso = np.array([])
            arr_muonHits = np.array([])
            arr_dimuonMass = np.array([])
            # Global muon만 사용
            if( muonType[muNum] != 0 and muonType[muNum] != 1): continue
            
            # Good muon selection
            if(cktpT[muNum] > self.ptCut 
               and abs(eta[muNum]) < self.etaCut
               and trackerLayers[muNum] > 5 
               and pixelHits[muNum] > 0
               and RelIso[muNum] < 0.10 
               and abs(dxyVTX[muNum]) < 0.2
               and abs(dzVTX[muNum]) < 0.5 
               and muonHits[muNum] > 0
               and nMatches[muNum] > 1
               and pTReso[muNum] < 0.3):     
                
                if(charge[muNum] > 0):
                    muPlus.append(tmpMuon)
                    muPlusData.append(cktpT[muNum])
                    muPlusData.append(eta[muNum])
                    muPlusData.append(RelIso[muNum])
                    muPlusData.append(pTReso[muNum])
                    muPlusData.append(muonHits[muNum])

                if(charge[muNum] < 0):
                    muMinus.append(tmpMuon)
                    muMinusData.append(cktpT[muNum])
                    muMinusData.append(eta[muNum])
                    muMinusData.append(RelIso[muNum])
                    muMinusData.append(pTReso[muNum])
                    muMinusData.append(muonHits[muNum])
                    
                recoMass = 0
                recoCand = []
                if (len(muPlus) == 1 and len(muMinus) == 1):
                    recoCand.append(muPlus[0]+muMinus[0])
                    recoMass = self.fourVectorMass(recoCand[0])
                    
                if (recoMass > 0):
                    arr_cktpT = np.array([muPlusData[0], muMinusData[0]])
                    arr_eta = np.array([muPlusData[1], muMinusData[1]])
                    arr_RelIso = np.array([muPlusData[2], muMinusData[2]])
                    arr_pTReso = np.array([muPlusData[3], muMinusData[3]])
                    arr_muonHits = np.array([muPlusData[4], muMinusData[4]])
                    arr_dimuonMass = np.array([recoMass])
        return arr_cktpT, arr_eta, arr_RelIso, arr_pTReso, arr_muonHits, arr_dimuonMass
    
    def getMuonData(self, directory):
        # 지정한 경로의 ROOT 파일 읽어오기
        ntuple = uproot.open(directory)
        if 'Higgs' in directory:
            tree = ntuple['recoTree']['DYTree;6']
        elif '50files' in directory:
            tree = ntuple['recoTree']['DYTree;26']
        elif '10files' in directory:
            tree = ntuple['recoTree']['DYTree;6']
        elif 'DY' in directory:
            tree = ntuple['recoTree']['DYTree;1']

        # 읽어온 루트 파일에서 필요한 정보 받아오기
        ## HLT (high level trigger) 정보
        hlt_ntrig = tree['HLT_ntrig'].array(library="np")
        hlt_trigname = tree['HLT_trigName'].array(library="np")
        hlt_trigfired = tree['HLT_trigFired'].array(library="np")

        ## Muon 관련 variables 정보
        charge = tree['Muon_charge'].array(library="np")
        cktpT = tree['Muon_cktpT'].array(library="np")
        eta = tree['Muon_eta'].array(library="np")
        RelIso = (tree['Muon_trkiso'].array(library="np") / cktpT)
        pTReso = (tree['Muon_cktpTError'].array(library="np") / cktpT)
        trackerLayers = tree['Muon_trackerLayers'].array(library="np")
        muonHits = tree['Muon_muonHits'].array(library="np")
        pixelHits = tree['Muon_pixelHits'].array(library="np")
        dxyVTX = tree['Muon_dxyVTX'].array(library="np")
        dzVTX = tree['Muon_dzVTX'].array(library="np")
        nMatches = tree['Muon_nMatches'].array(library="np")
        muonType = tree['Muon_muonType'].array(library="np")
        px = tree['Muon_Px'].array(library="np")
        py = tree['Muon_Py'].array(library="np")
        pz = tree['Muon_Pz'].array(library="np")

        # 이벤트 loop을 돌며 good muon 조건을 만족하는 뮤온 찾기
        ## Muon variable dictionary
        muonData = { 'cktpT':[], 'eta':[], 'RelIso':[], 'pTReso':[], 'muonHits':[], 'dimuonMass':[] }
  
        for evtNum in range(len(charge)):
            
            if( (evtNum%10000) == 0) : print("Processing %i evt..." %(evtNum))
        
            ## HLT check
            Fired = self.isFired(evtNum, hlt_ntrig, hlt_trigname, hlt_trigfired)
            if not Fired:
                continue
                
            ## Good muon selection
            selected_cktpT, selected_eta, selected_RelIso, selected_pTReso, selected_muonHits, selected_dimuonMass = self.goodMuon(charge[evtNum], cktpT[evtNum], eta[evtNum], RelIso[evtNum],
                                                            pTReso[evtNum], trackerLayers[evtNum], muonHits[evtNum], pixelHits[evtNum], dxyVTX[evtNum],
                                                            dzVTX[evtNum], nMatches[evtNum], muonType[evtNum], px[evtNum], py[evtNum], pz[evtNum] )
            
            if not (len(selected_cktpT) == 0): 
                muonData['cktpT'].append(selected_cktpT)
                muonData['eta'].append(selected_eta)
                muonData['RelIso'].append(selected_RelIso)
                muonData['pTReso'].append(selected_pTReso)
                muonData['muonHits'].append(selected_muonHits)
                muonData['dimuonMass'].append(selected_dimuonMass)

        # 학습에 사용할 variable dictionary 반환
        return muonData