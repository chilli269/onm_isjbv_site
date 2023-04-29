/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('website_pathology.website_pathology_mgmt', function (require) {

    "use strict";
    var ajax = require('web.ajax');
    var session = require('web.session');

    function get_today_date(){
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();
        if(dd<10) {
            dd = '0'+dd
        }
        if(mm<10) {
            mm = '0'+mm
        }
        today = yyyy + '-' + mm + '-' + dd;
        return today
    }

    $(document).ready(function(){

        $('tr.testreq_row').click(function() {
            var href = $(this).find("a").attr("href");
            if (href) {
                window.location = href;
          }
        });

        $('#testreq_date').attr('min', get_today_date());
        $('#testreq_date').attr('value', get_today_date());
        $('#patho_dob').attr('max', get_today_date());


        $('#testreq_date').on('input', function() {
        	var input=$(this);
        	var test_date=input.val();
        	if(test_date){input.removeClass("invalid").addClass("valid");
            }
        	else{input.removeClass("valid").addClass("invalid");}
        });
        $('#collect_centers').on('input', function() {
        	var input=$(this);
        	var collect_centers=input.val();
        	if(collect_centers){input.removeClass("invalid").addClass("valid");}
        	else{input.removeClass("valid").addClass("invalid");}
        });

        $('#wrap').on('click','[href="/shop/checkout?express=1"]',function(ev){
            // var test_date = $('#testreq_date').val().replace(/(\d\d)\/(\d\d)\/(\d{4})/, "$3-$1-$2");
            ev.preventDefault();
            if ($('#testreq_date').length == 0){
                window.location.href = window.location.origin+'/shop/checkout?express=1';
                return
            }
            $('#collect_centers').removeClass("invalid");
            $('#testreq_date').removeClass("invalid");
            $('#testreq_gender').removeClass('invalid');
            $('#blood_group').removeClass('invalid');
            $('#patho_dob').removeClass('invalid');
            $('#rh_factor').removeClass('invalid');
            var test_date = $('#testreq_date').val()
            var comment = $('#comment').val()
            var center_id =  parseInt($("select.collect_centers option:selected" ).val())
            var gender = $('#testreq_gender').val();
            var blood_group = $("#blood_group").val();
            var dob = $("#patho_dob").val();
            var rh_factor = $("#rh_factor").val();
            var error = false;
            if(gender == null){
                $('#testreq_gender').addClass('invalid');
                error = true;
            }
            if(dob == ''){
                $('#patho_dob').addClass('invalid');
                error = true;
            }
            if(blood_group == null){
                $('#blood_group').addClass('invalid');
                error = true;
            }
            
            if(rh_factor == null){
                $('#rh_factor').addClass('invalid');
                error = true;
            }
            if (test_date == '') {
                $('#testreq_date').addClass("invalid");
                error = true;
            }
            if (isNaN(center_id)){
                $('#collect_centers').addClass("invalid");
                error = true;
            }
            if(error)return;
            $('.patho_loader').show();
            ajax.jsonRpc('/get/test_date', 'call', {
                test_date: test_date,
                collect_center_id: center_id,
                comment:comment,
                gender,
                blood_group,
                dob,
                rh_factor
            }).then(function(data){
                if (isNaN(center_id) && (test_date == '')){
                    $('#collect_centers').addClass("invalid");
                    $('#testreq_date').addClass("invalid");
                }
                else if (test_date == '') {
                    $('#testreq_date').addClass("invalid");
                }
                else if (isNaN(center_id)){
                    $('#collect_centers').addClass("invalid");
                }
                else if(data == undefined){
                    $('#testreq_date').addClass("invalid").removeClass("valid");
                    bootbox.alert({
                        title: "Warning",
                        message:"Test Date should be today or later.",
                    })
                }
                else{
                    $('#testreq_date').removeClass("invalid").removeClass("valid");
                    $('#collect_centers').removeClass("invalid").removeClass("valid");
                // }
                // else{
                    window.location.href = window.location.origin+'/shop/checkout'
                }
            })
            $('.patho_loader').hide();
        })

    });
});
