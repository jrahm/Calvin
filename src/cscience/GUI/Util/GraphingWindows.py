"""
Graphing.py

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
import wx
import sys

from wx.lib.agw import aui
from wx.lib.agw import foldpanelbar as fpb

from cscience import datastore
from cscience.GUI import icons, events
from cscience.GUI.Util import PlotOptions, PlotCanvas
from cscience.GUI.Util.CalWidgets import CalChoice, CalCollapsiblePane
            

class PlotWindow(wx.Frame):

    ''' Class which is a toolbar specific to the
    PlotWindow '''
    class Toolbar(aui.AuiToolBar): # {
        def __init__(self, parent, indattrs):
            aui.AuiToolBar.__init__(self, parent, wx.ID_ANY,
                                      agwStyle=aui.AUI_TB_HORZ_TEXT)
            self.icons = self.setup_art()
            
            # Checkbox's to tell which axis should be on the
            # bottom. {
            text = "Independent Axis:"
            self.AddLabel(wx.ID_ANY, text, width=self.GetTextExtent(text)[0])
        
            l_id = wx.NewId()
            self.AddRadioTool(l_id, '',
                              self.icons['y_axis'], 
                              self.icons['y_axis'])
    
            l_id = wx.NewId()
            self.AddRadioTool(l_id, '',
                              self.icons['x_axis'], 
                              self.icons['x_axis'])
            # }

            # The different choices for the data to plot {
            choice_arr = [(i,None) for i in indattrs]
            choice_dict = dict(choice_arr)
            invar_choice = CalChoice(self, choice_dict) 
            self.AddControl(invar_choice)

            choice_dict = dict(choice_arr + [('<Multiple>','')])
            depvar_choice = CalChoice(self, choice_dict) 
            self.AddControl(depvar_choice)
            # }

            self.AddStretchSpacer()
            self.AddSeparator()

            options_button_id = wx.NewId()
            self.AddSimpleTool(options_button_id, "", self.icons['graphing_options'])

            self.Realize()
            self.options_pressed_listeners = []
            self.Bind(wx.EVT_TOOL, self.__on_options_pressed, id=options_button_id)

        def on_options_pressed_do( self, func ):
            # do something when the options button is pressed 
            self.options_pressed_listeners.append( func )

        def __on_options_pressed(self, _):
            for f in self.options_pressed_listeners: f()

        def setup_art(self):
            # Setup the dictionary of artwork for easier and
            # more terse access to the database of icons
            art = [
                  ("radio_on",icons.ART_RADIO_ON)
                , ("radio_off", icons.ART_RADIO_OFF)
                , ("graphing_options", icons.ART_GRAPHING_OPTIONS)
                , ("x_axis", icons.ART_X_AXIS)
                , ("y_axis", icons.ART_Y_AXIS)
                ]
    
            art_dic = {}
            for (name, loc) in art:
                art_dic[name] = wx.ArtProvider.GetBitmap(
                    loc, wx.ART_TOOLBAR, (16, 16))
            return art_dic
    # }

    class OptionsPane(CalCollapsiblePane): # {
        def __init__(self, parent):
            CalCollapsiblePane.__init__(self, parent)
            fold_panel = fpb.FoldPanelBar(self.GetPane(), wx.ID_ANY, size=(150, -1),
                                    agwStyle=fpb.FPB_VERTICAL, pos=(-1, -1))
    
            cs = fpb.CaptionBarStyle()
            base_color = aui.aui_utilities.GetBaseColour()
            cs.SetFirstColour(aui.aui_utilities.StepColour(base_color, 180))
            cs.SetSecondColour(aui.aui_utilities.StepColour(base_color, 85))

            sizer = wx.GridSizer(1, 1)
            sizer.Add(fold_panel, 1, wx.EXPAND)
            self.GetPane().SetSizer(sizer)
    # }
    
    def __init__(self, parent, samples):
        start_pos = parent.GetPosition()
        start_pos.x += 50
        start_pos.y += 100
        # initialize the window as a frame
        super(PlotWindow, self).__init__(parent, wx.ID_ANY, samples[0]['core'],
                                         pos=start_pos)

        # choices in the first combo box
        independent_choices = [
            i.name for i in datastore.sample_attributes
                   if i.is_numeric() and i in parent.view ]

        sizer = wx.GridBagSizer()

        sizer.Add(self.build_toolbar(self, independent_choices ),
                    wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND)

        # self.plot_canvas = PlotCanvas(self, samples, [])
        # sizer.Add(self.plot_canvas, wx.GBPosition(1, 0),
        #             wx.GBSpan(1, 1), wx.EXPAND)

        sizer.Add(self.build_options_pane(self),
                    wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND)

        sizer.AddGrowableCol(0, 1)
        sizer.AddGrowableRow(0, 0)

        self.SetSizerAndFit(sizer)
        self.Layout()

    def build_options_pane(self, parent):
        return PlotWindow.OptionsPane(self) ;

    def build_toolbar(self, parent, independent_choice ):
        # The toolbar for the window
        ret = PlotWindow.Toolbar(parent, independent_choice)
        ret.on_options_pressed_do(lambda: sys.stdout.write("Hello, World!\n"))
        return ret
            
        


