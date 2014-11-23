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
    #_content = traitlets.Unicode(sync=True)
    _header = traitlets.Unicode(sync=True)
    _columns = traitlets.Unicode(sync=True)
    _data_request = traitlets.Unicode(sync=True)
    _data_response = traitlets.Unicode(sync=True)

    dataframe = traitlets.Any()

    _sortorder = traitlets.Any()
    _searchval = traitlets.Unicode() 

    _view_module = 'js/datatables'
    _view_style = 'css/datatables'

    _datatable_css = traitlets.Unicode(sync=True,
                                       default_value=open(os.path.join(_view_static, 'css', 'theme.css')).read())

    def __init__(self, dataframe):
        super(DataTablesWidget, self).__init__()
        self.on_trait_change(self.on_request_change, '_data_request')


    def invalidate_subset(self):
        self.subset = self.dataframe.loc[self.search_indexes]

    def on_request_change(self):
        req = json.loads(self._data_request)

        start_idx = req['start']
        draw = req['draw']
        length = req['length']

        searchval = req['search']['value']

        # to do search
        orders = zip(req['orders'])

        column_names = [c['name'] for c in req['columns']]

        # Sort
        if orders != self._sortorder 
            sort_columns = [column_names[c['column']] for c in orders]
            sort_dir = [True if c['dir'] == 'asc' else False for c in orders]

            self.dataframe.sort(sort_columns, ascending=sort_dir, inplace=True)
            self._sortorder = orders

        if searchval !=  self._searchval:
            if (searchval == '') or (searchval is None):
                self.search_indexes = self.dataframe.index

            o = []
            for c in df.columns:
                o.append(df[c].str.contains(searchval))
            self.search_indexes = reduce(lambda x, y: x | y, o)
            self.invalidate_subset()

        # set up return structure
        subset = self.subset
        display_window = subset.iloc[start_idx:start_idx+length]


        return_str = {
            'draw': draw,
            'recordsTotal': self.dataframe.shape[0],
            'recordsFiltered': self.subset.shape[0],
            'data': json.loads(
                display_window.to_json(orient='records')
                )

        self._data_response = json.dumps(return_str)


def show_df(df):
    widget = DataTablesWidget()
    widget.dataframe = df

    #widget._content = df.to_json(orient='records')
    widget._header = df[:0].to_html(index=False)
    widget._columns = json.dumps([{'data': x} for x in df.columns])

    widget.set_css({'width': '100%', 'background-color': '#FFF', 'padding': 10})

    return widget