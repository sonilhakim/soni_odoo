odoo.define('html_form_builder_snippets.editor', function (require) {
'use strict';

var Model = require('web.Model');
var base = require('web_editor.base');
var options = require('web_editor.snippets.options');
var session = require('web.session');
var website = require('website.website');

$("#popup_button").on('click', function () {
    $('#oe_generic_popup_modal').modal('show');
});


options.registry.popup_button = options.Class.extend({
/*
    start: function () {
		var self = this;
		self.$target.find("#popup_button").on('click', function () {
		    self.$target.find('#oe_generic_popup_modal').modal('show');
		});
    },
*/
    drop_and_build_snippet: function() {
		var self = this;
     //    var model = new Model('marketing.campaign');
	    // model.call('name_search', [], { context: base.get_context() }).then(function (campaign_ids) {
	        website.prompt({
			    window_title: "Create Popup",
			    select: "Submit Comment",
			    init: function (field) {

                    var $group = this.$dialog.find("div.form-group");
                    $group.removeClass("mb0");

                    var $add = $(
                    '<div class="form-group mb0">'+
                        '<label class="col-md-3">Return URL</label>'+
                        '<div class="col-md-9">'+
                        '    <input id="return_url" type="textbox" placeholder="http://vuente.com" class="form-control"/> '+
                        '</div>'+
                    '</div>');
                    $group.after($add);
			    },
			}).then(function (field, $dialog) {
				// self.$target.find("#popup_campaign_id").val(campaign_id);
				self.$target.find("#popup_return_url").val( $dialog.find("#return_url").val() );
			});
        });
    },


});


});