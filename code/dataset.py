#!/usr/bin/env python

from torch.utils.data import Dataset
import pandas as pd
import torch

class muonDataset(Dataset):
    def __init__(self):
        super(muonDataset, self).__init__()
        self.data = pd.DataFrame(columns=["charge", "cktpT", "eta", "RelIso", "pTReso", "muonHits", "dimuonMass"])
        self.label = pd.DataFrame(columns=["label"])
        
    def __getitem__(self, idx):        
        data = torch.FloatTensor([ self.data["charge"][idx], self.data["cktpT"][idx], self.data["eta"][idx], self.data["RelIso"][idx], self.data["pTReso"][idx], self.data["muonHits"][idx], self.data["dimuonMass"][idx] ])
        label = torch.FloatTensor([ self.label["label"][idx] ])
        
        return data, label
    
    def __len__(self):
        return(len(self.data))
    
    def load(self, muons, l):
        for i in range( len(muons['cktpT']) ):
            if( i > 25000 ) : break
            if( (i%10000) == 0) : print("Loading %i evt..." %(i))
            self.data = self.data.append( pd.DataFrame( [[1., muons['cktpT'][i][0], muons['eta'][i][0], muons['RelIso'][i][0], muons['pTReso'][i][0], muons['muonHits'][i][0], muons['dimuonMass'][i][0] ]], columns=["charge", "cktpT", "eta", "RelIso", "pTReso", "muonHits", "dimuonMass"]) )
            self.label = self.label.append( pd.DataFrame( [[l]], columns=["label"] ))
            self.data = self.data.append( pd.DataFrame( [[-1., muons['cktpT'][i][1], muons['eta'][i][1], muons['RelIso'][i][1], muons['pTReso'][i][1], muons['muonHits'][i][1], muons['dimuonMass'][i][0] ]], columns=["charge", "cktpT", "eta", "RelIso", "pTReso", "muonHits", "dimuonMass"]) )
            self.label = self.label.append( pd.DataFrame( [[l]], columns=["label"] ))
        self.data = self.data.reset_index(drop=True)
        self.label = self.label.reset_index(drop=True)