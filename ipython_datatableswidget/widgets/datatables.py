# -*- coding: utf-8 -*-

import os

# Import widgets, provisioners and traitlets
from IPython.html import widgets
from IPython.utils import traitlets
import json
from .mixins import InstallerMixin

_VIEW_STATIC = os.path.join(
    os.path.dirname(__file__), '..', 'static', 'ipython_datatableswidget'
)


class DataTablesWidget(InstallerMixin, widgets.DOMWidget):
    '''
    A widget for representing a DataFrame as a DataTable.

    This widget makes heavy use of a bunch of traitlets for sending state for DataTables.
    '''

    # the name of the Backbone.View subclass to be used
    _view_name = traitlets.Unicode('DataTablesView', sync=True)
    _view_static = traitlets.Unicode(_VIEW_STATIC, sync=True)

    # an actual value, used in the front-end
    #_content = traitlets.Unicode(sync=True)
    _header = traitlets.Unicode(sync=True)
    _columns = traitlets.Unicode(sync=True)
    _data_request = traitlets.Unicode(sync=True)
    _data_response = traitlets.Unicode(sync=True)

    _dataframe = traitlets.Any()

    _sortorder = traitlets.Any()
    _searchval = traitlets.Any()

    _view_module = 'js/datatables'
    _view_style = 'css/datatables'

    _datatable_css = traitlets.Unicode(sync=True,
                                       default_value=open(os.path.join(_VIEW_STATIC, 'css', 'theme.css')).read())

    def __init__(self, dataframe, index=False):
        super(DataTablesWidget, self).__init__()
        self._dataframe = dataframe
        if index:
            self._dataframe = dataframe.reset_index()
        self._header = self.dataframe[:0].to_html(index=False)
        self._columns = json.dumps([{'data': x, 'name': x} for x in self.dataframe.columns])
        self.search_indexes = self.dataframe.index
        self.invalidate_subset()
        self.set_css({'width': '100%', 'background-color': '#FFF', 'padding': 10})

        self.on_trait_change(self.on_request_change, '_data_request')

    def invalidate_subset(self):
        self._subset = self.dataframe.loc[self.search_indexes]

    def on_request_change(self):
        req = json.loads(self._data_request)

        start_idx = req['start']
        draw = req['draw']
        length = req['length']

        searchval = req['search']['value']

        orders = req['order']
        column_names = [c['name'] for c in req['columns']]

        df = self._dataframe

        # Sort
        if orders != self._sortorder:
            sort_columns = [column_names[c['column']] for c in orders]
            sort_dir = [True if c['dir'] == 'asc' else False for c in orders]

            df.sort(sort_columns, ascending=sort_dir, inplace=True)
            self._sortorder = orders
            self._searchval = None

        if searchval != self._searchval:
            if (searchval == '') or (searchval is None):
                self.search_indexes = df.index
            else:
                o = []
                for c in self.dataframe.columns:
                    o.append(df[c].astype(str).str.contains(searchval))
                self.search_indexes = reduce(lambda x, y: x | y, o)
            self._searchval = searchval
            self.invalidate_subset()

        # set up return structure
        subset = self._subset
        display_window = subset.iloc[start_idx:start_idx+length]

        return_str = {
            'draw': draw,
            'recordsTotal': self.dataframe.shape[0],
            'recordsFiltered': self.subset.shape[0],
            'data': json.loads(
                display_window.to_json(orient='records')
                )
            }

        self._data_response = json.dumps(return_str)


def show_df(df):
    widget = DataTablesWidget(df)
    #widget.dataframe = df

    #widget._content = df.to_json(orient='records')
    #widget._header = df[:0].to_html(index=False)
    #widget._columns = json.dumps([{'data': x} for x in df.columns])

    #widget.set_css({'width': '100%', 'background-color': '#FFF', 'padding': 10})

    return widget
