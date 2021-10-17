odoo.define('wt_theme_base.AppsMenuExtended', function (require) {
'use strict';

	var AppsMenuExtended = require('web.AppsMenu')

	AppsMenuExtended.include({

    	init: function (parent, menuData) {
            this._super.apply(this, arguments);
            this.Color_code = menuData.company_color;
            this.bg_image = menuData.company_bg_image;
            this.bg_selection = menuData.background_selection;
        },
		get_company_code: function() {
        	return this.Color_code;
    	},

        get_company_bg_image: function() {
            return this.bg_image;
        },

        get_company_bg_selection: function() {
            return this.bg_selection;
        },
	})
});

