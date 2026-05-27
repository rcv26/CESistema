odoo.define('/ks_chat_edit_and_delete/static/src/js/ks_mail_extended.js', function (require) {
'use strict';
 const component = {

        Message : require('mail/static/src/models/message/message.js'),
    };
    const {
    registerClassPatchModel,
    registerFieldPatchModel,
    registerInstancePatchModel,
} = require('mail/static/src/model/model_core.js');
const { attr } = require('mail/static/src/model/model_field.js');

registerClassPatchModel('mail.message', 'ks_chat_edit_and_delete/static/src/js/ks_mail_extended.js', {
    //----------------------------------------------------------------------
    // Public
    //----------------------------------------------------------------------

    /**
     * @override
     */
    convertData(data) {
        const data2 = this._super(data);
        if ('ks_msg_edit' in data) {
            data2.ks_msg_edit = data.ks_msg_edit;
        }
        return data2;
    },
});

registerInstancePatchModel('mail.message', 'ks_chat_edit_and_delete/static/src/js/ks_mail_extended.js', {
    //----------------------------------------------------------------------
    // Public
    //----------------------------------------------------------------------

    /**
     * @override
     */
    async toggleStar() {
        await this.async(() => this.env.services.rpc({
            model: 'mail.message',
            method: 'toggle_message_starred',
            args: [[this.id]]
        }));
        window.location.reload();
    }
});

registerFieldPatchModel('mail.message', 'ks_chat_edit_and_delete/static/src/js/ks_mail_extended.js', {
     ks_msg_edit: attr({
            default: false,
        }),
});


    const components = {
    Message: require('mail/static/src/components/message/message.js'),
    Thread: require('mail/static/src/models/thread/thread.js'),
    Emoj: require('mail/static/src/components/emojis_popover/emojis_popover.js'),
    };
    const { patch } = require('web.utils');
    const useStore = require('mail/static/src/component_hooks/use_store/use_store.js');
    var core = require('web.core');
    var ks_emojis = require('mail.emojis');
    var ks_session = require('web.session');
    var ks_rpc = require('web.rpc');
    var check_chat_enable = false;
    var ks_is_edit =  false;
    var time;
    var ks_thread = require('mail/static/src/models/thread/thread.js');
    var ks_qweb = core.qweb;
    var show_icon = true;
    var ks_message_div;
    var ks_message;
    var ks_thread_messages
    var ks_global_id = 0;
    var container;

    if (ks_session.ks_chat_enable){
        check_chat_enable = true;
}
    if(ks_session.is_admin && ks_session.ks_admin_delete_access){
        time = (48*60);
    }else{
        time = 15;
    }

    patch(components.Message, '/ks_chat_edit_and_delete/static/src/js/ks_mail_extended.js', {

        render: function (thread) {
           var ks_self = this;
           $('.o_MessageList').find('.ks_edit_icon').addClass('ks_hide')
           $('.o_MessageList').find('.ks_delete_icon').addClass('ks_hide')
           $('.o_MessageList').find('.fa-star-o').parent().addClass('ks_hide')
           Object.values(document.querySelectorAll(".o_Message")).map((item) => { item.addEventListener('mouseover', this.onMessageThreadHover.bind(this)) });
           Object.values(document.querySelectorAll(".o_Message")).map((item) => { item.addEventListener('mouseout', this.onMessageThreadUnHover.bind(this)) });
        },

        //    Hover discussion thread onchange
         onMessageThreadHover : function(e){
             if ($(e.currentTarget)[0].className != "o_Message o-discussion o-squashed o_MessageList_item o_MessageList_message"){
                 $(e.currentTarget).find('.ks_edit_icon').removeClass('ks_hide');
                 $(e.currentTarget).find('.ks_delete_icon').removeClass('ks_hide');
                 $(e.currentTarget).find('.fa-star-o').parent().removeClass('ks_hide');
                 $(e.currentTarget).find('.ks_check_edited').addClass('ks_hide');
             }
             else{
                 $(e.currentTarget).find('.ks_edit_icon').removeClass('ks_hide');
                 $(e.currentTarget).find('.ks_delete_icon').removeClass('ks_hide');
                 $(e.currentTarget).find('.fa-star-o').removeClass('ks_hide');
                 $(e.currentTarget).find('.fa-star-o').parent().removeClass('ks_hide');
                 $(e.currentTarget).find('.o_Message_date').removeClass('ks_hide');
                 $(e.currentTarget).find('.ks_check_edited').addClass('ks_hide');
             }
         },

//         //    UnHover discussion thread onchange
         onMessageThreadUnHover : function(e){
             if ($(e.currentTarget)[0].className != "o_Message o-discussion o-squashed o_MessageList_item o_MessageList_message"){
                 $(e.currentTarget).find('.ks_edit_icon').addClass('ks_hide');
                 $(e.currentTarget).find('.ks_delete_icon').addClass('ks_hide');
                 $(e.currentTarget).find('.fa-star-o').parent().addClass('ks_hide');
                 $(e.currentTarget).find('.ks_check_edited').removeClass('ks_hide');
             }
             else{
                 $(e.currentTarget).find('.ks_edit_icon').addClass('ks_hide');
                 $(e.currentTarget).find('.ks_delete_icon').addClass('ks_hide');
                 $(e.currentTarget).find('.fa-star-o').addClass('ks_hide');
                 $(e.currentTarget).find('.fa-star-o').parent().addClass('ks_hide');
                 $(e.currentTarget).find('.o_Message_date').addClass('ks_hide');
                 $(e.currentTarget).find('.ks_check_edited').removeClass('ks_hide');
             }
         },

        async _onClickEditMsg(ev) {
            var ks_self = this;
            var ks_messageID = this.message.id;
            var ks_input = document.createElement("div");
            $(ks_self.el).find('.o_thread_edit').attr('data-message-local-id', ks_self.message.localId)
            $(ks_self.el).find('.o_thread_message_delete').attr('data-message-local-id', ks_self.message.localId)
            $(ks_self.el).find('.o_Message_commandStar').attr('data-message-local-id', ks_self.message.localId)
            var ks_icons = $("[data-message-local-id='" + "mail.message_" + ks_messageID + "']");
            $(ks_icons[1]).hide();
            $(ks_icons[3]).hide();
            $(ev.currentTarget).hide();

            ks_input.id = "div_input_"+ks_messageID;
            $(ks_input).addClass("div_input");
            ks_input.innerHTML = "<div><textarea type='text' class='o_input_chat' id='input_"+ks_messageID+"'> </textarea>  <button class=' btn btn-secondary fa o_thread_smile fa-smile-o' type='button' data-toggle='popover' title='Emojis' id='emoji_"+ks_messageID+"' ></button><i class='fa o_thread_update fa-check fa-lg' title='Update' id='update_"+ks_messageID+"' ></i> <i class='fa o_thread_cancel fa-times fa-lg' title='Cancel' id='cancel_"+ks_messageID+"' ></i></div>";
            var ks_msg = 'mail.message_'+ks_messageID;
            if ($("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0].querySelector(".ks_edit_icon")){
                $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0].querySelector(".ks_edit_icon").style.display="none";
                $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0].querySelector(".ks_delete_icon").style.display="none";
                $($("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0]).find(".ks_check_edited").children().remove();
            }
            else{
                $("[data-message-local-id='" + ks_msg + "']")[0].children[0].querySelector(".ks_edit_icon").style.display="none";
                $("[data-message-local-id='" + ks_msg + "']")[0].children[0].querySelector(".ks_delete_icon").style.display="none";
                $($("[data-message-local-id='" + ks_msg + "']")[0].children[0]).find(".ks_check_edited").children().remove();
            }
            if ($("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[1]){
                ks_message_div = $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[1];
                ks_message = $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[1].innerText;
            }
            else{
                ks_message_div = $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0];
                ks_message = $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0].innerText;
            }
            ks_message_div.replaceWith(ks_input);
            $('#input_'+ks_messageID).val(ks_message);

            var ks_textarea = document.getElementById("input_"+ks_messageID);
            ks_textarea.style.cssText = 'height:auto; padding:0';
            ks_textarea.style.cssText = 'height:' + ks_textarea.scrollHeight + 'px';
            $(ks_textarea).scrollTop(ks_textarea.scrollHeight);

            document.getElementById("update_"+ks_messageID).onclick = function() {ks_update_click(ks_message,false,ks_self)};
            document.getElementById("cancel_"+ks_messageID).onclick = function() {ks_update_click(ks_message,true,ks_self)};
            document.getElementById("emoji_"+ks_messageID).onclick = function() {ks_emoji_btn_click(ks_self,ks_messageID)};

            $('#input_'+ks_messageID).on("keyup", function(e) {
                if (e.keyCode == 13 && !e.shiftKey) {
                    ks_update_click(ks_message,false,ks_self);
                }
            });

            $('#input_'+ks_messageID).on("keydown", function(e) {
                var ks_el = this;
                setTimeout(function(){
                    ks_el.style.cssText = 'height:auto; padding:0';
                    ks_el.style.cssText = 'height:' + ks_el.scrollHeight + 'px';
                    $(ks_el).scrollTop(ks_el.scrollHeight);
                  },0);

            });

            /*
             * Function to handle the emoji button.
             */

            function ks_emoji_btn_click(ks_self,ks_messageID)
            {
                ks_global_id = ks_messageID;
                if (!ks_self._$emojisContainer) {
                       container = $(ks_qweb.render('mail.legacy.Composer.emojis2', {
                        emojis: ks_emojis,
                }));
                }

                if (container.parent().length) {
                    ks_self._$emojisContainer.remove();
                }

                if (!$('#div_input_'+ks_messageID+' .o_mail_emoji_container').length)
                {
                    container.appendTo($('#div_input_'+ks_messageID));
                }
                else{
                    $('#div_input_'+ks_messageID).find('.o_mail_emoji_container').remove();
                }

                 $('.o_EmojisPopover_emoji').click(function(event){
                 let textArea = $('.o_input_chat').val();
                 let TextData = textArea+event.currentTarget.innerText;
                 $('.o_input_chat').val(TextData)
                })
            }

            /*
             * Function to Handle the update click button to update the message.
             */

            function ks_update_click(ks_message,ks_undo,ks_self) {
                var ks_input_val = document.getElementById("input_"+ks_messageID).value;

                if(ks_self._$emojisContainer != undefined){
                    ks_self._$emojisContainer.remove();
                }

                if(ks_input_val === "" || ks_undo === true){
                   ks_input_val = ks_message;
                }

                if(ev.target.className === "fa o_thread_icon o_thread_edit fa-pencil fa-lg o_Activity_toolButton"){
                    if($("[data-message-local-id='" + "mail.message_" + ks_messageID + "']")[0].children[1].children[1]){
                        ks_message_div = $("[data-message-local-id='" + "mail.message_" + ks_messageID + "']")[0].children[1].children[1];
                        var ks_msg_span = $("[data-message-local-id='" + "mail.message_" + ks_messageID + "']")[0].children[1].children[0].children[5];
                    }
                    else{
                        ks_message_div = $("[data-message-local-id='" + "mail.message_" + ks_messageID + "']")[0].children[1].children[0];
                        var ks_msg_span = $("[data-message-local-id='" + "mail.message_" + ks_messageID + "']")[0].children[0].children[4];
                    }
                }
                else{
                    ks_message_div = $("[data-message-local-id='" + "mail.message_" + ks_messageID + "']")[0].children[1].children[0].children[0];
                    var ks_msg_span = $("[data-message-local-id='" + "mail.message_" + ks_messageID + "']")[0].children[1].children[0].children[5];
                }

                if(ks_input_val != ks_message){
                    var ks_data = ks_rpc.query({
                                model: 'mail.message',
                                method: 'ks_edit_message',
                                args: [ks_messageID, true],
                            });
                    ks_msg_span.innerHTML = "<span>(Edited)</span>";
                    $(ks_self.message).attr('ks_is_edit', true)
                    ks_self.message.ks_edit = true;

                    _.map(ks_thread_messages, function(ks_thread_message, ks_message_div){
                       if(ks_thread_message._id === ks_messageID){
                            ks_thread_message.ks_msg_edit = true;
                            ks_thread_message._body = $("#input_"+ks_messageID)[0].value;
                       }
                   });
                }

                var ks_para = document.createElement("P");
                var ks_text = document.createTextNode(ks_input_val);
                ks_para.appendChild(ks_text);
                $(ks_message_div.replaceWith(ks_para));

                ks_input_val = "<p>"+ks_input_val+"</p>";
                var messages = ks_rpc.query({
                model: 'mail.message',
                method: 'write',
                args:  [[ks_messageID],{'id': ks_messageID,
                                        'body': ks_input_val, }],
                });
                $(ks_icons[1]).show();
                $(ks_icons[2]).show();
                $(ks_icons[3]).show();
                window.location.reload();

            }
         },

        async _onClickDeleteMsg(ev){
                var ks_result = confirm("Are you sure, you want to delete this message permanently ?");
             if (ks_result) {
               var ks_self = this;
               var ks_messageID = this.message.id;
               var ks_data = this.env.services.rpc({
                                model: 'mail.message',
                                method: 'ks_delete_message',
                                args: [ks_messageID],
                            }).then (function(value){
                                    return value;
                       });

               var ks_msg_edited = ks_rpc.query({
                                model: 'mail.message',
                                method: 'ks_edit_message',
                                args: [ks_messageID, false],
                            });
               var ks_msg = 'mail.message_'+ks_messageID;
               if(ev.target.className === "fa fa-lg fa-trash-o o_thread_icon o_thread_message_delete o_Activity_toolButton"){
                    if($("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[1]){
                        $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[1].innerHTML = "<p><i>This message was deleted.</i></p>";
                    }
                    else{
                        $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0].innerHTML = "<p><i>This message was deleted.</i></p>";
                    }
                }
               else{
                    if($("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[1]){
                        $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[1].innerHTML = "<p><i>This message was deleted.</i></p>";
                    }
                    else{
                        $("[data-message-local-id='" + ks_msg + "']")[0].children[1].children[0].innerHTML = "<p><i>This message was deleted.</i></p>";
                    }
                }
               var ks_notif_div = document.createElement("div");
               ks_notif_div.id = "snackbar";
               var ks_textnode = document.createTextNode("Message deleted successfully");
               ks_notif_div.appendChild(ks_textnode);

               var ks_body = document.getElementsByTagName("body");
               $(ks_body[0]).append(ks_notif_div);

               var ks_snackbar = document.getElementById("snackbar");
               ks_snackbar.className = "show";
               setTimeout(function(){ ks_snackbar.className = ks_snackbar.className.replace("show", ""); }, 3000);
               window.location.reload();
             }
        },

        _renderEdit(ev){
            if ($('.o_Discuss_thread').length == 1){
                if (check_chat_enable && ks_session.is_admin){
                    if (moment.locale() === 'es'){
                        if(moment().diff(moment(this.datetime, 'DD/MM/YYYY HH:mm:ss'),"minutes")< 15){
                            if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                return true;
                            }
                        }
                        else{
                            return false;
                        }
                    }else{
                        if(moment().diff(this.datetime,"minutes")< 15){
                            if(this.message.body =="<p><i>Admin has deleted this message.</i></p>"){
                                return false;
                            }
                            else if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                return true;
                            }
                        }
                        else{
                            return false;
                        }
                    }
                }
                else if(check_chat_enable && ks_session.is_admin == false){
                     if(moment().diff(this.datetime,"minutes")< 15){
                        if (this.message.author.user){
                            if(this.message.author.user.id == ks_session.user_id){
                                if(this.message.body =="<p><i>Admin has deleted this message.</i></p>"){
                                    return false;
                                }
                                else if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                    return true;
                                }
                            }else{
                                if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                    return false;
                                }
                            }
                        }else{
                            return false;
                        }
                     }
                     else{
                        return false;
                     }
                }
            }
        },

        _renderDelete(ev){
            if (check_chat_enable)
            {
                    return true;
            }
            else{
                return false;
            }

        },

//          _renderCheckEdited: async function(ev){
//            var message_edit_id = this.message.id;
//            const ks_data = await this.rpc({
//                                model: 'mail.message',
//                                method: 'ks_edit_message',
//                                args: [message_edit_id],
//                            });
//                if(check_chat_enable && ks_data){
//                    return true;
//
//            }
//            else{
//                $($("[data-message-local-id='" + 'mail.message_'+this.message.id + "']")[0].children[1].children[0]).find(".ks_check_edited").remove()
//            }
//        },

        _renderCheckEdited(ev){
            if (check_chat_enable)
            {
                if(this.message.ks_msg_edit){
                    return true;
                }
            }
            else{
                return false;
            }

        },

        _ks_edit_time_elapsed_delete(ev){
            if($('.o_Discuss_thread').length == 1){
                if (check_chat_enable && ks_session.ks_admin_delete_access && ks_session.is_admin){
                    if (moment.locale() === 'es'){
                        if(moment().diff(moment(this.datetime, 'DD/MM/YYYY HH:mm:ss'),"minutes")< 2880){
                            if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                return true;
                            }
                        }
                        else{
                            return false;
                        }
                    }
                    else{
                        if(moment().diff(this.datetime,"minutes")< 2880){
                            if(this.message.body =="<p><i>Admin has deleted this message.</i></p>"){
                                    return false;
                            }
                            else if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                return true;
                            }
                        }
                        else{
                            return false;
                        }
                    }
                }
                else if(check_chat_enable && ks_session.is_admin && ks_session.ks_admin_delete_access == false){
                       return false;
                }
                else if(check_chat_enable && ks_session.is_admin == false){
                   if(moment().diff(this.datetime,"minutes")< 15){
                        if(this.message.author.user){
                            if(this.message.author.user.id == ks_session.user_id){
                                if(this.message.body =="<p><i>Admin has deleted this message.</i></p>"){
                                        return false;
                                    }
                                else if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                    return true;
                                }
                            }else{
                                if(this.message.body !="<p><i>This message was deleted.</i></p>"){
                                    return false;
                                }
                            }
                        }else{
                            return false;
                        }
                    }else{
                        return false;
                    }
                }
            }
        },


});
});