odoo.define('vit_dashboard_ninja_inherit.ks_dashboard', function (require){
    "use strict";

    // require original module JS
    var dashboard = require('ks_dashboard_ninja.ks_dashboard');

    // Extend widget
    dashboard.include({
        ksNumFormatter: function (num, digits) {
                var si = [{
                        value: 1,
                        symbol: ""
                    },
                    {
                        value: 1E3,
                        symbol: "Rb"
                    },
                    {
                        value: 1E6,
                        symbol: "Jt"
                    },
                    {
                        value: 1E9,
                        symbol: "M"
                    },
                    {
                        value: 1E12,
                        symbol: "T"
                    },
                    {
                        value: 1E15,
                        symbol: "P"
                    },
                    {
                        value: 1E18,
                        symbol: "E"
                    }
                ];
                var rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
                var i;
                for (i = si.length - 1; i > 0; i--) {
                    if (num >= si[i].value) {
                        break;
                    }
                }
                return "Rp " + (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
            },
    });
})