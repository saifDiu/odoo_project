odoo.define('wt_ctmetals.wt_signature', function (require) {
'use strict';
	var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require("web.Widget");
    var rpc = require("web.rpc");
    var qweb = core.qweb;
	var WtSignatureForm = Widget.extend({
        template: 'wt_ctmetals.wt_signature',
        events: {
            'click #o_portal_sign_clear': 'clearSign',
            'click .o_portal_sign_submit': 'submitSign',
            'init #o_portal_sign_accept': 'initSign',
        },


        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.options = _.extend(options || {}, {
                csrf_token: odoo.csrf_token,
            });
        },

        willStart: function() {
            return this._loadTemplates();
        },

        start: function() {
            this.initSign();
        },

        // Signature
        initSign: function () {
            this.$("#o_portal_signature").jSignature({
            'decor-color': '#D1D0CE',
            'color': '#000',
            'background-color': '#fff',
            'height': '200px',
            'width': '100%', // prevent the signature from being too big
            });
            this.$("#o_portal_signature1").jSignature({
            'decor-color': '#D1D0CE',
            'color': '#000',
            'background-color': '#fff',
            'height': '200px',
            'width': '100%', // prevent the signature from being too big
            });
            this.empty_sign_0 = this.$("#o_portal_signature").jSignature('getData', 'image');
            this.empty_sign_1 = this.$("#o_portal_signature1").jSignature('getData', 'image');
              
        },

        clearSign: function (ev) {
            $(ev.currentTarget).closest('.card').find('.card-body').jSignature('reset');
        },
        submitSign: function (ev) {
            ev.preventDefault();

            // extract data
            var self = this;
            var $confirm_btn = self.$el.find('button[type="submit"]');

            // process : display errors, or submit
            var signature = false;
            var signature1 = false;
            var is_empty = true;
            var is_empty1 = true;
            
                
                var signature = this.$("#o_portal_signature").jSignature('getData', 'image');
                var is_empty = signature ? this.empty_sign_0[1] === signature[1] : true;
                $('#signature').val(signature[1])
                

            this.$('#o_portal_sign_draw').toggleClass('bg-danger text-white', is_empty);

            if (is_empty || is_empty1 || !agencies_name || !client_name) {
                return false;
            }

            $confirm_btn.prepend('<i class="fa fa-spinner fa-spin"></i> ');
            $confirm_btn.attr('disabled', true);
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         * @returns {Deferred}
         */
        _loadTemplates: function () {
            return ajax.loadXML('/wt_ctmetals/static/src/xml/wt_signature.xml', qweb);
        },
    });

    $( document ).ready(function() {
        $('.wt_signature_form').each(function () {
            var hasBeenReset = false;
            var $elem = $(this);
            var form = new WtSignatureForm(null, $elem.data());
            form.appendTo($elem);
            // Make the signature responsive when it is displayed in bootstrap modal.
            // More precisely it is too small if this code is not here.
            $elem.parents('.modal').on('shown.bs.modal', function (ev) {
                $elem.trigger('resize');
                if (!hasBeenReset) {
                    // Reset it only the first time it is open to get correct
                    // size. After we want to keep its content on reopen.
                    hasBeenReset = true;
                    form.initSign();
                }
            });
        });
    });

    return {
        WtSignatureForm: WtSignatureForm,
    };
});