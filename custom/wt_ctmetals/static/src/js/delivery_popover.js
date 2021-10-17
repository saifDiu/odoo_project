odoo.define('wt_ctmetals.custom', function (require) {
'use strict';
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.wt_ctmetals_radio = publicWidget.Widget.extend({
    selector: '.radio_group_cl',
    events: {
        'change .goods#yes': '_onClickradio',
        'change .goods#no': '_onClickradiono',
    },

        _onClickradio: function (ev) {
            $('.annotation_cl').addClass('d-none')
        },

        _onClickradiono: function (ev) {
            $('.annotation_cl').removeClass('d-none')
        },
    });

    publicWidget.registry.credit_limit_error = publicWidget.Widget.extend({
        selector: '.credit_limit_error',
        events: {
            'click': '_onClickSignandPay',
        },

        start: function() {
            this._super.apply(this, arguments);
        },
        _onClickSignandPay: function (ev) {
            var content = $('<div>').html(_t("<p>credit limit has exceeded! You can not confirm this order.<p/>") );
            new Dialog(self, {
                    title: _t('Warning!'),
                    size: 'medium',
                    $content: content,
                    buttons: [
                    {text: _t('Ok'), close: true}]
            }).open();
        },
    });
});
