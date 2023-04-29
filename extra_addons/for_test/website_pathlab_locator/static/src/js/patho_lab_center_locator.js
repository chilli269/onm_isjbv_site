/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('website_pathlab_locator.patho_lab_center_locator', function(require) {
    "use strict";

    $(function() {
        var ajax = require('web.ajax');
        var core = require('web.core');
        var _t = core._t;
        var markers = [];
        var infowindows = [];
        var openinfo = null;
        var mapProp;
        var map;
        var vals = {};
        var show_locator;
        var initialize_data;
        var load_count = 0;
        var lab_count = 0;
        var bounds;
        var search_radius = 0;
        var tab_count = 0;

        show_locator = $('#show-lab-locator').data('show-lab-locator');

        if (show_locator === 'yes') {
            $('.lab_locator_loader').show();
            vals = {}
            lab_locator_call_json(vals); //fucntion call
            $('.reset-loc').on('click', function() {
                lab_reset_locator_data();
            });

            $('.search-lab').on('click', function() {
                lab_search_by_address_init();
            });

            $('#search-input').on('input', function() {
                lab_search_by_address_init();
            });

            $('#search-input').keypress(function(e) {
                if (e.which == 13) {
                    lab_search_by_address_init();
                }
            });
        }

        function lab_search_by_address_init() {
            var addr_dict = {};
            var search_string = ($('#search-input').val()).toLowerCase();
            $('.lab-not-found').hide();
            $('.extra-information').hide();
            hide_info_window();
            search_by_address(search_string);
        }

        function search_by_address(search_string) {
            var main_addr = '';
            var count = 0;
            var not_have_cat = 0;
            bounds = new google.maps.LatLngBounds();
            $.each(initialize_data.map_lab_data, function(key, value) {
                main_addr = get_search_main_address(value);
                if (!main_addr) {
                    main_addr = ''
                }
                var match = main_addr.indexOf(search_string);
                if (match >= 0) {
                    show_marker_and_lab(parseInt(key));
                    count++;
                } else {
                    hide_marker_and_lab(parseInt(key));
                }
            });
            if (count >= 1) {
                if(search_string == ''){
                    map.setZoom(5);
                }
                else{
                    map.fitBounds(bounds);
                    map.setZoom(11);
                }
            } else {
                get_lab_nearest_address(search_string);
            }
            $(".lab-lable").text("" + count + _t(" Lab(s)"));
        }

        function get_lab_nearest_address(search_string) {
            var latitude = 0;
            var longitude = 0;
            var geocoder = new google.maps.Geocoder();
            var count = 0;
            $('.lab_locator_loader').show();
            bounds = new google.maps.LatLngBounds();
            geocoder.geocode({
                'address': search_string
            }, function(results, status) {
                $('.lab_locator_loader').hide();
                if (status == google.maps.GeocoderStatus.OK) {
                    latitude = results[0].geometry.location.lat();
                    longitude = results[0].geometry.location.lng();
                    $.each(initialize_data.map_lab_data, function(key, value) {
                        var d = distance_between_points(latitude, longitude, value.lab_lat, value.lab_lng);
                        if (d <= search_radius) {
                            show_marker_and_lab(parseInt(key));
                            count++;
                        } else {
                            hide_marker_and_lab(parseInt(key));
                        }
                    });
                    if (count == 0) {
                        $('.lab-not-found').show();
                    } else {
                        map.fitBounds(bounds);
                        map.setZoom(11);
                        $('.extra-information.alert-info').html("Result not found for zip <b><i style='color: #ff0000;'>" + search_string + "</i></b>, showing results for nearest lab form your serach.");
                        $('.extra-information').show();
                    }
                    $(".lab-lable").text("" + count + _t(" Lab(s)"));
                } else {
                    $('.lab-not-found').show();
                }
            });
        }

        function distance_between_points(lat1, lon1, lat2, lon2) {
            var R = 6371; // Radius of the earth in km
            var dLat = deg2rad(lat2 - lat1); // deg2rad below
            var dLon = deg2rad(lon2 - lon1);
            var a =
                Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            var d = R * c * 1000; // Distance in meter
            return d;
        }

        function deg2rad(deg) {
            return deg * (Math.PI / 180)
        }

        function get_search_main_address(lab) {
            var main_addr = lab.lab_name.toLowerCase();
            if (lab.lab_address[0])
                main_addr += lab.lab_address[0].toLowerCase() + ' ';
            if (lab.lab_address[1])
                main_addr += lab.lab_address[1].toLowerCase() + ' ';
            if (lab.lab_address[2])
                main_addr += lab.lab_address[2].toLowerCase() + ' ';
            if (lab.lab_address[3])
                main_addr += lab.lab_address[3].toLowerCase() + ' ';
            if (lab.lab_address[4])
                main_addr += lab.lab_address[4].toLowerCase() + ' ';
            return main_addr
        }

        function lab_locator_call_json(vals) {
            $('.lab_locator_loader').show();
            ajax.jsonRpc('/lab/locator/vals', 'call', vals)
                .then(function(data) {
                    if (data) {
                        if (load_count == 0) {
                            initialize_data = data;
                            search_radius = data.map_search_radius;
                        }
                        initialize_lab_locator(initialize_data); //fucntion call
                        load_count++;
                    } else {
                        alert(_t("No lab Found."));
                    }
                    $('.lab_locator_loader').hide();
                });
        }

        function hide_info_window() {
            if (openinfo != null) {
                infowindows[openinfo].close(map, markers[openinfo]);
                $('#' + (openinfo + 1) + '').find('.lab-list').removeClass('selected');
                openinfo = null;
            }
        }

        function initialize_lab_locator(initialize_data) {
            var mapProp = {
                center: new google.maps.LatLng(initialize_data.map_init_data.map_center_lat, initialize_data.map_init_data.map_center_lng),
                zoom: initialize_data.map_init_data.map_zoom,
                mapTypeId: initialize_data.map_init_data.map_type
            };
            map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
            draw_marker_and_info_map(map, initialize_data.map_lab_data); //function call
            $('.lab-menu ul').append("<li class='lab-not-found' style='display:none;'>No Result Found.</li>");
        }

        function draw_marker_and_info_map(map, map_lab_data) {
            $(".lab-lable").text("" + Object.keys(initialize_data.map_lab_data).length + _t(" Lab(s)"));
            lab_count = ((Object.keys(initialize_data.map_lab_data).length) - 1);
            $.each(map_lab_data, function(key, values) {
                markers.push(new google.maps.Marker({
                    position: new google.maps.LatLng(values.lab_lat, values.lab_lng),
                    title: values.lab_name,
                    map: map,
                    icon: '/website_pathlab_locator/static/src/img/location_marker_icon.png',
                    animation: google.maps.Animation.DROP
                }));
                key = parseInt(key);
                var info = get_lab_info_html(values);
                infowindows.push(new google.maps.InfoWindow({
                    content: info
                }));
                load_lab_list(key, values, info);
                markers[key].addListener('click', function() {
                    if (openinfo != null) {
                        infowindows[openinfo].close(map, markers[openinfo]);
                        $('#' + (openinfo + 1) + '').find('.lab-list').removeClass('selected');
                        openinfo = null;
                    }
                    infowindows[key].open(map, markers[key]);
                    if (!markers[key].getVisible()) {
                        markers[key].setVisible(true);
                    }
                    $('#' + (key + 1) + '').find('.lab-list').addClass('selected');
                    openinfo = key;
                    var temp = $(".lab-menu").offset().top;
                    $(".lab-menu").animate({
                        scrollTop: 0
                    }, 1, function() {
                        $(".lab-menu").animate({
                            scrollTop: $('#' + (key + 1) + '').offset().top - temp
                        }, 1);
                    });
                });
            });
        }

        function get_lab_info_html(lab) {
            var addr = '';
            if (lab.lab_image) {
                addr += '<div class="row ml0 mr0"><div class="col-md-3 col-sm-3 col-xs-3"><div class="lab-image"><a href='+lab.profile_url+' target="new"><img style="width: 60px;height: 60px;margin-left:-10px;border-radius: 8%;" src="' + lab.lab_image + '"/><a></div></div>';
            }
            if (lab.lab_name) {
                addr += '<div class="col-md-9 col-sm-12 col-xs-12">' + '<a target="_new" href="/pathology/lab/info/' + lab.lab_id + '">' +
                '<div class="lab-marker-content text-primary" style="font-weight:bold; font-size:14px;font-family:OpenSans-Semibold;">' + lab.lab_name + '</div></a> <div class="lab-marker-content" style="font-weight:400;">';
            }
            if (lab.lab_address[0]) {
                addr += lab.lab_address[0] + '<br/>';
            }
            if (lab.lab_address[1]) {
                addr += lab.lab_address[1] + ', ';
            }
            if (lab.lab_address[2]) {
                addr += lab.lab_address[2] + ', ';
            }
            if (lab.lab_address[3]) {
                addr += lab.lab_address[3] + '<br/>';
            }
            if (lab.lab_address[4]) {
                addr += lab.lab_address[4] + '<br/>';
            }
            if (lab.lab_address[5]) {
                addr += '<div class="divtel lab-contact lab-marker-content"> <b>Tel: </b>' + lab.lab_address[5] + '</div>'
            }
            if (lab.lab_address[6]) {
                addr += '<div class="divmail lab-contact lab-marker-content"><b>Email: </b><a href="mailto:' + lab.lab_address[6] + '">' + lab.lab_address[6] + '</a></div>';
            }
            addr += '</div></div>'
            // addr += '<a target="_new" href="/pathology/lab/info/"' + lab.lab_id +  '">View Details</a>'
            return addr;
        }

        function load_lab_list(key, lab, info) {
            $('.lab-menu ul').append("<li style='width:100%' id=" + (key + 1) + " class=''>\
            <div class='lab-list'>\
              <span id='map-lat' data-map-lat=" + lab.lab_lat + "/>\
              <span id='map-lng' data-map-lng=" + lab.lab_lng + "/>\
              <input type='hidden' name='lab-id' value=" + lab.lab_id + "></input>\

              <div class='lab-info row ml0 mr0' style='font-weight: bold;font-family: OpenSans-Semibold;font-size: 14px;display:flex;'>" + info + "</div>\
            </div></li>");
            //  <div class='list-image col-md-3 col-sm-4 col-xs-4'>\
            //     <img style='width: 75px;height: 75px;border-radius: 50%;;' src='" + lab.lab_image + "'/>\
            //   </div>\
            // $('li#' + key + '').find('.lab-info img').remove();
            $('li#' + (key + 1) + '').find('.lab-info .lab-image a').removeAttr("href");
            $('li#' + (key + 1) + '').find('.lab-info .divtel').remove();
            // $('li#' + (key + 1) + '').find('.lab-info .divfax').remove();
            $('li#' + (key + 1) + '').find('.lab-info .divmail').remove();
            $('li#' + (key + 1) + '').find('.lab-info .divwww').remove();

            $('#' + (key + 1) + '').on('click', function() {
                if (openinfo != null) {
                    infowindows[openinfo].close(map, markers[openinfo]);
                    $('#' + (openinfo + 1) + '').find('.lab-list').removeClass('selected');
                    openinfo = null;
                }
                $('#' + (key + 1) + '').find('.lab-list').addClass('selected');
                // map.setZoom(11);
                markers[key].setVisible(true);
                map.setCenter(markers[key].getPosition());
                infowindows[key].open(map, markers[key]);
                openinfo = key;
            });

        }

        function lab_reset_locator_data() {
            $('.lab-not-found').hide();
            $('#search-input').val('');
            $('.extra-information').hide();
            map.setZoom(initialize_data.map_init_data.map_zoom);
            map.setCenter(new google.maps.LatLng(initialize_data.map_init_data.map_center_lat, initialize_data.map_init_data.map_center_lng));
            if (openinfo != null) {
                infowindows[openinfo].close(map, markers[openinfo]);
                $('#' + (openinfo + 1) + '').find('.lab-list').removeClass('selected');
                openinfo = null;
            }
            show_all_initial_marker(); //function call
            show_all_lab_list(); //function call
        }

        function show_all_initial_marker() {
            $.each(markers, function(index, value) {
                if (!value.getVisible()) {
                    value.setVisible(true);
                }
            });
        }

        function show_all_lab_list() {
            $('.lab-menu ul li').removeClass('lab-hidden');
            $(".lab-lable").text("" + Object.keys(initialize_data.map_lab_data).length + _t(" lab(s)"));
            lab_count = ((Object.keys(initialize_data.map_lab_data).length) - 1);
        }

        function show_marker_and_lab(key) {
            if (!markers[key].getVisible()) {
                markers[key].setVisible(true);
            }
            bounds.extend(markers[key].getPosition());
            $('#' + (key + 1) + '').removeClass('lab-hidden');
        }

        function hide_marker_and_lab(key) {
            if (markers[key].getVisible()) {
                markers[key].setVisible(false);
            }
            $('#' + (key + 1) + '').addClass('lab-hidden');
        }

    });
});
