"""
NonCosmogenicProduction.py

* Copyright (c) 2006-2009, University of Colorado.
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the University of Colorado nor the
*       names of its contributors may be used to endorse or promote products
*       derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY OF COLORADO ''AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF COLORADO BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from ACE.Framework.Component import Component

class NonCosmogenicProduction(Component):
    def __init__(self, collections, workflow):
        super(NonCosmogenicProduction, self).__init__(collections, workflow)
        self.constants = collections.get("Constants")
        self.elements = collections.get("Elements")
        self.elemNames = ["O", "H", "C", "Na", "Mg", "Al", "Si", "P", "K", "Ca", "Ti", "Mn", "Fe", "Cl", "B", "Sm", "Gd", "U", "Th"]
        self.chemNames = ["CO2", "Na2O", "MgO", "Al2O3", "SiO2", "P2O5", "K2O", "CaO", "TiO2", "MnO", "Fe2O3", "Cl", "Cl uncertainty", "B", "Sm", "Gd", "U", "Th"]
        self.LAMBDA_36 = self.constants["lambda_36"]
        

    def init_sample(self, s):
        self.chemistry = []
        for name in self.chemNames:
            self.chemistry.append(s[name])
        self.compositions = []
        for name in self.elemNames:
            self.compositions.append(s[name + "Calc"])
        self.f_eth    = s["f_eth"]
        self.f_th     = s["f_th"]
        self.P_eth_ss = s["P_eth_ss"]

    def __call__(self, samples):
        for s in samples:
            # only perform calculations on the first time through the loop
            if s["age"] == self.experiment["timestep"]:
                self.init_sample(s)

                self.calculatePn_sf(s);
                self.calculateX(s);
                self.calculateY(s);
                self.calculatePn_an(s);
                self.calculatePeth_r(s);
                self.calculatePth_r(s);
                self.calculateInv_r(s);

        return (([self.get_connection()], samples),)

    def calculatePn_sf(self, s):
        # calculate 0.429*C_u
        s["Pn_sf"] = 0.429 * s["U"]

    def calculateX(self, s):
        # calculate SUMPRODUCT(Si,N_i,Ai,Yn_iu)/SUMPRODUCT(Si,N_i,Ai)

        numerator   = 0.0
        denominator = 0.0

        for i in range(len(self.elemNames)):
            comp = self.compositions[i];

            elem = self.elements[self.elemNames[i]]
            sPower = elem["Spower"]
            alpha  = elem["alpha"]
            YnIu   = elem["YnUranium"]

            product2 = comp * sPower * alpha
            product1 = product2 * YnIu

            numerator   += product1
            denominator += product2

        s["X"] = numerator / denominator

    def calculateY(self, s):

        # calculate SUMPRODUCT(Si,N_i,Ai,Yn_ith)/SUMPRODUCT(Si,N_i,Ai)

        numerator   = 0.0
        denominator = 0.0

        for i in range(len(self.elemNames)):
            comp = self.compositions[i];

            elem = self.elements[self.elemNames[i]]
            sPower = elem["Spower"]
            alpha  = elem["alpha"]
            YnTh   = elem["YnThorium"]

            product2 = comp * sPower * alpha
            product1 = product2 * YnTh

            numerator   += product1
            denominator += product2

        s["Y"] = numerator / denominator

    def calculatePn_an(self, s):
        # calculate X*C_u+Y*C_th
        s["Pn_an"] = (s["X"] * s["U"]) + (s["Y"] * s["Th"])

    def calculatePeth_r(self, s):
        # calculate (Pn_an+Pn_sf)*(1-P_eth_ss)
        s["Peth_r"] = (s["Pn_an"] + s["Pn_sf"]) * (1.0 - self.P_eth_ss)

    def calculatePth_r(self, s):
        # calculate (Pn_an+Pn_sf)*(P_eth_ss)
        s["Pth_r"] = (s["Pn_an"] + s["Pn_sf"]) * self.P_eth_ss

    def calculateInv_r(self, s):
        # calculate (Pth_r*f_th+Peth_r*feth)*(1/lambda_36)

        div   = 1.0 / self.LAMBDA_36

        prod1 = s["Pth_r"] * self.f_th
        prod2 = s["Peth_r"] * self.f_eth

        sum   = prod1 + prod2

        s["nucleogenic inventory"] = sum * div

# vim: ts=4:sw=4:et
