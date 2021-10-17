odoo.define('wt_theme_base.Menu', function (require) {
"use strict";

    const config = require("web.config");

    const Menu = require("web.Menu");
    var session = require("web.session")
    var WebClient = require('web.WebClient')
    const core = require('web.core');

    Menu.include({
        events: _.extend({}, Menu.prototype.events, {
        	"click .o_menu_apps a[data-toggle=dropdownsk]": "_onAppsMenuClick",
            "click .o_menu_sections [role=menuitem]": "_hideMobileSubmenus",
            "show.bs.dropdown .o_menu_systray, .o_menu_apps": "_hideMobileSubmenus",
        }),
        start() {
        	const res = this._super(...arguments);
            this.$menu_toggle = this.$(".mk_menu_sections_toggle");
            if (config.device.isMobile) {
                const menu_ids = _.keys(this.$menu_sections);
                for (let i = 0; i < menu_ids.length; i++) {
                	const $section = this.$menu_sections[menu_ids[i]];
                	$section.on('click', 'a[data-menu]', this, (ev) => {
                    	ev.stopPropagation();
                    });
                }
            } 
            return Promise.all([
            	res
            ]);
        },
        _hideMobileSubmenus(ev) {
            if (this.$menu_toggle.is(":visible") && $('.oe_wait').length === 0 && 
            		this.$section_placeholder.is(":visible")) {
                this.$section_placeholder.collapse("hide");
            }
        },
        _updateMenuBrand() {
            return !config.device.isMobile ? this._super(...arguments) : null;
        },
        _onAppsMenuClick(event, checkedCanBeRemoved) {
            event.stopPropagation();
            event.preventDefault();
        	const action_manager = this.getParent().action_manager;
            var company_id = session.company_id
        	const controller = action_manager.getCurrentController();
        	if (controller && !checkedCanBeRemoved) {
        		controller.widget.canBeRemoved().then(() => {
        			$(event.currentTarget).trigger('click', [true]);
                    $('body').toggleClass('o_home_background');
                    $(event.currentTarget).next().toggleClass('show');
                });
            	
            }
        },
    });
    WebClient.include({
        _on_app_clicked_done: function(ev) {
            return this._super(...arguments).then(function(d){
                if(ev.data.menu_id){
                    if($(ev.target.el).parent().hasClass('o_menu_apps')){
                        $('.o_menu_apps a[data-toggle=dropdownsk').next().toggleClass('show');
                        $('body').toggleClass('o_home_background');
                    }
                    
                    // if(!$('.o_menu_apps a[data-toggle=dropdownsk').next().hasClass('show')){
                    //     $('body').removeClass('o_home_background');
                    // }else{
                    //     $('body').addClass('o_home_background');
                    // }
                }
            });
            // core.bus.trigger('change_menu_section', ev.detail.menu_id);
            // this.toggleHomeMenu(false);
            // return Promise.resolve();
        },
        on_menu_clicked: async function (ev) {
            var res = await this._super(...arguments);
            if($(ev.target.el).parent().hasClass('o_menu_apps')){
                $('.o_menu_apps a[data-toggle=dropdownsk').next().toggleClass('show');
                $('body').toggleClass('o_home_background');
                // if(!$('.o_menu_apps a[data-toggle=dropdownsk').next().hasClass('show')){
                //     $('body').removeClass('o_home_background');
                // }else{
                //     $('body').addClass('o_home_background');
                // }

            }
        }
    });
});