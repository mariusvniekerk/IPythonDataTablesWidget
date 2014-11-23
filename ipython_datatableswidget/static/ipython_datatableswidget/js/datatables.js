;(function(IPython, require){
  'use strict';
   /**
    * The browser-side counterpart to DataTablesView
    *
    * @author Marius van Niekerk
    * @copyright Marius van Niekerk 2014
    * @version 0.1.0
    * @license BSD
    */

  require.config({
    paths: {
      'datatables': "//cdn.datatables.net/1.10.3/js/jquery.dataTables.min"
    },
    shim : {
      'datatables' : {
        "deps" : ['jquery']
      }
    }
  });


  require(
    ['jquery', 'underscore', 'widgets/js/widget', 'datatables'],
    function($, _, WidgetManager){
      var DataTablesView = IPython.DOMWidgetView.extend({
        // namespace your css so that you don't break other people's stuff
        className: 'DataTablesView',

        // Initialize DOM, etc. called once per view creation,
        // i.e. `display(widget)`
        render: function(){

          var that = this;
          // Create the date picker control.
          var header = this.model.get('_header');
          var div = $('<div style="width:100%"><style scoped>' + this.model.get("_datatable_css") + '</style></div>');

          var table = $(header);
          table.css('width', '100%');
          div.append(table);
          this.$dt = table.DataTable({
              "columns": JSON.parse(this.model.get("_columns"))
              "serverSide": true,
              "ajax": this.server_side,
          });

          this.$el.append(div);

          //_.defer(_.bind(this.update, this));

          // returning `this` makes your view chainable
          return this;
        },

        server_side: function(data, callback, settings) {
            this.model.set("_data_request", JSON.stringify(data));
            var data = JSON.parse(this.model.get("_data_response"));
            callback(data);
        }

        // Do things that are updated every time `this.model` is changed...
        // on the front-end or backend.
        // update: function(){

        //   var data = JSON.parse(this.model.get('_content'));

        //   this.$dt.rows.add(data);
        //   this.$dt.draw();

        //   // call __super__.update to handle housekeeping
        //   return DataTablesView.__super__.update.apply(this);
        // }, // update


        // Tell Backbone to listen to the change event of input controls (which
        // the HTML date picker is)
        events: {
          //'change input': 'dateChange'
        }

        // Callback for when the date is changed.

      }); // /extend

      // Register the DataTablesView with the widget manager.
      WidgetManager.register_widget_view(
        'DataTablesView',
        DataTablesView
      );
    });
}).call(this, IPython, require);