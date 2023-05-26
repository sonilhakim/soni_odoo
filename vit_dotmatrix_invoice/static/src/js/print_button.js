//#############################################################################
//  @@@ web_print_printer_data custom JS @@@
//#############################################################################
odoo.define('vit_dotmatrix.print_button', function (require) {
    "use strict";

    var form_widget = require('web.form_widgets');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;

    form_widget.WidgetButton.include({
        on_click: function() {
            if(this.node.attrs.custom === "print" ){

                var url = "http://localhost:8000/dotmatrix/print";

                var view = this.getParent();
                var printer_data = view.datarecord.printer_data;
                if (!printer_data){
                    alert('No data to print. Please click Update Printer Data');
                    return;
                }
                console.log(printer_data);

                $.ajax({
                    type: "POST",
                    url: url,
                    data: {
                        printer_data : printer_data
                    },
                    success: function(data) {
                        alert('Success');
                        console.log(data);
                    },
                    error: function(data) {
                        alert('Failed');
                        console.log(data);
                    },
                });
            }
            else{
                this._super();
            }  
        },
    });
  
});