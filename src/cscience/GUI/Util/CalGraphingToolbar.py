import wx
from wx.lib.agw import aui
from cscience.GUI import icons
from cscience.GUI.Util.graph import StylePanel

from cscience.GUI.Util.CalWidgets import CalChoice, CalCheckboxPanel

# class specific to a toolbar in the plot window
class Toolbar(aui.AuiToolBar): # {

    def __init__(self, parent, indattrs):
        # base class initialization
        aui.AuiToolBar.__init__(self, parent, wx.ID_ANY,
                                  agwStyle=aui.AUI_TB_HORZ_TEXT)
        self.icons = self.setup_art()

        self.invar_change_listener = None
        self.depvar_change_listener = None
        self.options_pressed_listener = None
        
        # The different choices for the data to plot {
        choice_arr = [(i,i) for i in indattrs]
        choice_dict = dict(choice_arr)
        self.invar_choice = CalChoice(self, choice_dict) 
        self.invar_choice.add_change_listener( lambda _,x: self.__on_invar_changed(x) )

        self.AddControl(self.invar_choice)

        choice_frame = wx.Frame(parent=None);
        choice_frame.Bind( wx.EVT_CLOSE, lambda _: choice_frame.Hide() )

        self._m_depvar_choices = StylePanel(choice_dict.keys(), choice_frame);
        self._m_depvar_choices.add_change_listener(self.__on_depvar_changed)

        self.depvar_choice = wx.Button(self, label="Dependent Variable") 
        self.depvar_choice.Bind( wx.EVT_BUTTON, lambda _: choice_frame.Show() )
        self.AddControl(self.depvar_choice)
        # }


        self.AddSeparator()

        options_button_id = wx.NewId()

        self.AddSimpleTool(options_button_id, "", self.icons['graphing_options'])

        self.Realize()
        self.Bind(wx.EVT_TOOL, self.__on_options_pressed, id=options_button_id)
    
    def __on_invar_changed( self, invar ):
        self.invar_change_listener(invar)
    def __on_depvar_changed( self, depvars ):
        self.depvar_change_listener(depvars)

    def on_invar_changed_do( self, func ):
        self.invar_change_listener = func

    def on_depvar_changed_do( self, func ):
        self.depvar_change_listener = func;

    def on_options_pressed_do( self, func ):
        # do something when the options button is pressed 
        self.options_pressed_listener = func

    def get_dependent_variables( self ):
        return self._m_depvar_choices.get_variables_and_options()

    def get_independent_variable( self ):
        return self.invar_choice.get_selected()

    def __on_options_pressed(self, _):
        self.options_pressed_listener()

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