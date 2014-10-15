# -*- coding: utf-8 -*-

import os

# Import widgets, provisioners and traitlets
from IPython.html import widgets
from IPython.utils import traitlets
import json
from .mixins import InstallerMixin

_view_static = os.path.join(
    os.path.dirname(__file__), '..', 'static', 'ipython_datatableswidget'
)

class DataTablesWidget(InstallerMixin, widgets.DOMWidget):
    '''
    A sample widget... with one "real" traitlet, and a bunch of housekeeping
    '''

    # the name of the Backbone.View subclass to be used
    _view_name = traitlets.Unicode('DataTablesView', sync=True)

    # an actual value, used in the front-end
    _content = traitlets.Unicode(sync=True)
    _header = traitlets.Unicode(sync=True)
    _columns = traitlets.Unicode(sync=True)

    dataframe = traitlets.Any()

    # provisioning and loading JS/CSS assets
    _view_static = os.path.join(
        os.path.dirname(__file__), '..', 'static', 'ipython_datatableswidget'
    )
    _view_module = 'js/datatables'
    _view_style = 'css/datatables'

    _datatable_css = traitlets.Unicode(sync=True,
                                       default_value=open(os.path.join(_view_static, 'css', 'theme.css')).read())


def show_df(df):
    widget = DataTablesWidget()
    widget.dataframe = df

    widget._content = df.to_json(orient='records')
    widget._header = df[:0].to_html(index=False)
    widget._columns = json.dumps([{'data': x} for x in df.columns])

    widget.set_css({'width': '100%', 'background-color': '#FFF', 'padding': 10})
    return widget