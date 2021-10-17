odoo.define('wt_theme_base.MenuExtended', function (require) {
'use strict';

    var core = require('web.core');

    var QWeb = core.qweb;
    var MenuExtended = require('web.Menu')

	MenuExtended.include({

    	init: function (parent, menu_data) {
            var self = this;
            this._super.apply(this, arguments);

            this.$menu_sections = {};
            this.menu_data = menu_data;
            this.navbar_bg_color_code = menu_data.navbar_bg_color;

            // Prepare navbar's menus
            var $menu_sections = $(QWeb.render(this.menusTemplate, {
                menu_data: this.menu_data,
            }));
            $menu_sections.filter('section').each(function () {
                self.$menu_sections[parseInt(this.className, 10)] = $(this).children('li');
            });

            // Bus event
            core.bus.on('change_menu_section', this, this.change_menu_section);
        },

		get_company_navbar_bg: function() {
            return this.navbar_bg_color_code;
        },
	})
});

