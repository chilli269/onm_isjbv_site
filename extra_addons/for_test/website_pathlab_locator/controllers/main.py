# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class PathoLabCenterLocator(http.Controller):

    @http.route(["/lab/locator/vals"], type='json', auth="public", website=True)
    def lab_locator_vals(self):
        lab_obj = request.env['patho.lab.centers'].sudo()
        key, sum_lat, sum_lng, lab_center_dict, vals = 0, 0, 0, {}, {}
        lab_center_ids = lab_obj.search([('is_collection_center', '=', True)])
        if lab_center_ids:
            for lab in lab_center_ids:
                if lab.patho_latitude and lab.patho_longitude:
                    lab_center_dict.update(self.get_patho_lab_data_dict(lab, key))
                    sum_lat = sum_lat + float(lab.patho_latitude)
                    sum_lng = sum_lng + float(lab.patho_longitude)
                    key = key + 1
            if key != 0:
                cen_lat, cen_lng, value = sum_lat/key, sum_lng/key, self.get_patho_map_config()
                if not value.get('auto'):
                    cen_lat, cen_lng = value.get('cen_lat'), value.get('cen_lng')
                zoom, map_type = value.get('zoom'), value.get('type')
                vals.update({'map_init_data': {'map_center_lat': cen_lat,
                                               'map_center_lng': cen_lng,
                                               'map_zoom':  int(zoom),
                                               'map_type': str(map_type)
                                               },
                             'map_lab_data': lab_center_dict,
                             'map_search_radius': value.get('search_radius'),
                             })
                return vals
            else:
                return False

    @http.route('/lab/locator', type='http', website=True, auth='public')
    def patho_lab_locator(self, **kw):
        return request.render('website_pathlab_locator.patho_lab_locator_page', {})

    def get_patho_lab_locator_config_vals(self):
        res = {}
        lab_locator_config_vals = request.env['res.config.settings'].sudo().get_values()
        if lab_locator_config_vals:
            res = {
              'map_center' : lab_locator_config_vals['map_center'] if lab_locator_config_vals.get('map_center') else False,
              'manually_option' : lab_locator_config_vals['manually_option'] if lab_locator_config_vals.get('manually_option') else False,
              'map_lat' : lab_locator_config_vals['map_lat'] if lab_locator_config_vals.get('map_lat') else False,
              'map_long' : lab_locator_config_vals['map_long'] if lab_locator_config_vals.get('map_long') else False,
              'street1' : lab_locator_config_vals['street1'] if lab_locator_config_vals.get('street1') else False,
              'street2' : lab_locator_config_vals['street2'] if lab_locator_config_vals.get('street2') else False,
              'city' : lab_locator_config_vals['city'] if lab_locator_config_vals.get('city') else False,
              'state' : lab_locator_config_vals['state'] if lab_locator_config_vals.get('state') else False,
              'zipcode' : lab_locator_config_vals['zipcode'] if lab_locator_config_vals.get('zipcode') else False,
              'country' : lab_locator_config_vals['country'] if lab_locator_config_vals.get('country') else False,
              'map_zoom' :lab_locator_config_vals['map_zoom'] if lab_locator_config_vals.get('map_zoom') else False,
              'map_type' : lab_locator_config_vals['map_type'] if lab_locator_config_vals.get('map_type') else False,
              'search_radius' : lab_locator_config_vals['search_radius'] if lab_locator_config_vals.get('search_radius') else False,
              'google_api_key' : request.env['ir.config_parameter'].sudo().get_param('google_maps_api_key') or False,
            }
        return res

    def get_patho_map_config(self):
        vals = {'auto': True, 'zoom': 5, 'type': 'satellite'}
        res = self.get_patho_lab_locator_config_vals()
        if res.get('map_center') == 'manually' and res.get('map_lat') and res.get('map_long'):
            vals['auto'] = False
            vals.update({'cen_lat': res.get('map_lat'),
                         'cen_lng': res.get('map_long')})
        if res.get('map_zoom'):
            vals['zoom'] = res.get('map_zoom')
        if res.get('map_type'):
            vals['type'] = res.get('map_type')
        vals['search_radius'] = res.get(
            'search_radius') if res.get('search_radius') else 50
        return vals

    def get_patho_lab_data_dict(self, lab=None, key=None):
        street1 = (lab.street1 + ',') if lab.street1 else ""
        data = {key: {'lab_lat': lab.patho_latitude,
                      'lab_lng': lab.patho_longitude,
                      'lab_name': lab.name,
                      'lab_image': '/web/static/img/placeholder.png' if not lab.image else request.website.image_url(lab, 'image'),
                      'lab_address': [ street1 , lab.city, lab.state_id.name, lab.country_id.name, lab.zipcode, lab.phone, lab.email],
                      'lab_id': lab.id
                      }
                }
        return data

    @http.route('/pathology/lab/info/<int:lab_id>', type='http', website=True, auth='public')
    def patho_lab_locator_details(self, lab_id=0, **kw):
        lab_obj = request.env['patho.lab.centers'].browse(lab_id)
        if not lab_obj.exists():
            return request.render('website.404')
        return request.render('website_pathlab_locator.patho_lab_details_page', {'lab_obj': lab_obj,})
