odoo.define('wt_ctmetals.webcam', function (require) {
'use strict';
	var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    

    publicWidget.registry.wt_ctmetals_webcam = publicWidget.Widget.extend({
    selector: '#web_cam_block',
    events: {
        'click .button_cl': '_onClicOkButton',
        'click #btAddPicture': '_addCamPicture',
        'click #cancel': '_OnClickCancel'
    },
        start: function(){
            Webcam.set({
                width: 220,
                height: 190,
                image_format: 'jpeg',
                jpeg_quality: 100
            });
            Webcam.attach('#camera');
            this._super.apply(this, arguments);
        },
        _onClicOkButton: function (ev) {
            var a = $(ev.currentTarget).val()
            $('#camBox').removeClass('d-none');
            $('#camBox').addClass('d-block');
			$('#rowid').val(a)
        },
         _addCamPicture: function () {
            var rowid = $('#rowid').val();
            Webcam.snap(function (data_uri) {
                var ddd = '<img src="' + data_uri + '" id="' + rowid + '" width="70px" height="50px" />';
    			$('#div_' + rowid).append(ddd);
    			var eee = '<input type="text" name="' + rowid + '" value="' + data_uri + '" id="' + rowid + '" />';
    			$('#image_div_' + rowid).append(eee); 
    			
			});

	        $('#rowid').value = '';
            $('#camBox').removeClass('d-block');
            $('#camBox').addClass('d-none');
        },

        _OnClickCancel: function () {
            $('#camBox').removeClass('d-block');
            $('#camBox').addClass('d-none');
        },
    });
});
