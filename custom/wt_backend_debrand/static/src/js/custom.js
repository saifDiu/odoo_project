odoo.define('wt_backend_debrand.custom', function (require) {
"use strict";
	var abstractwebclient = require("web.AbstractWebClient");
    var rpc = require('web.rpc');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var formRendar = require('web.FormRenderer');
    abstractwebclient.include({
        init: function(parent) {
            this._super(parent);
            var self = this;
            rpc.query({
            	model: 'res.config.settings',
            	method: 'get_debranding_settings'
            }).then(debranding_settings => {
                odoo.debranding_settings = debranding_settings;
                self.set('title_part', {"zopenerp": debranding_settings.r_title && debranding_settings.r_title.trim() || ''});
            });
        },
    });
    Dialog.include({
        init: function (parent, options) {
            var self = this;
            var options = options || {};
            var r_text = '';
            if(odoo.debranding_settings && odoo.debranding_settings.r_text) 
                r_text = odoo.debranding_settings.r_text.trim();
            if (options.title && typeof(options.title) =='string'){
                var title = options.title.replace(/odoo/gi,r_text);
                options.title = title;
            } else
                options.title = r_text;
           
            if (options.$content){
                var $content = $(options.$content)
                var content_text = $content.html();
                content_text = content_text.replace(/odoo/gi,r_text);
                $content.html(content_text);
            }
            self._super(parent, options);
        },
    });
    formRendar.include({
        _updateView: function ($newContent) {
            var self = this;
            _.each($newContent, function(el){
                $(el).find('.o_doc_link').remove();
                self.recusing_child(el);
            });
            this._super($newContent)
        },
        recusing_child: function(el){
            for (var i= el.childNodes.length; i-->0;) {
                var child= el.childNodes[i];
                if (child.nodeType==1){
                    var tag= child.nodeName.toLowerCase();
                    if (tag==='input'){
                        var ple = child.getAttribute('placeHolder');
                        if(ple){
                           var new_text = ple.replace(/odoo/g, odoo.debranding_settings.r_text);
                           child.setAttribute('placeHolder', new_text);
                        }
                    }else{
                        this.recusing_child(child);
                    }
                }
            }
        }
    });
});