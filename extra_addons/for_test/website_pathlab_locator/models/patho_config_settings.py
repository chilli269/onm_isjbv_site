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

from odoo import models,fields,api,tools,_
import json
import requests
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

def patho_map_geo_find(addr, apikey=False):
    if not addr:
        return None

    if not apikey:
        raise UserError(_('''API key for GeoCoding (Places) required.\n
                          Save this key in System Parameters with key: google.api_key_geocode, value: <your api key>
                          Visit https://developers.google.com/maps/documentation/geocoding/get-api-key for more information.
                          '''))

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    try:
        result = requests.get(url, params={'sensor': 'false', 'address': addr, 'key': apikey}).json()
    except Exception as e:
        raise UserError(_('Cannot contact geolocation servers. Please make sure that your Internet connection is up and running (%s).') % e)

    if result['status'] != 'OK':
        if result.get('error_message'):
            _logger.error(result['error_message'])
        return None

    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def patho_map_geo_query_address(street=None, street2=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(
        field for field in [street, street2, ("%s %s" % (zip or '', city or '')).strip(), state, country]
        if field
    ))


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    map_center = fields.Selection([('auto', 'Auto'),
                                   ('manually', 'Manually')
                                   ], string="Map Center", default="auto", required=True)

    map_zoom = fields.Integer(string="Map Zoom", default=5)
    map_type = fields.Selection([('roadmap', 'ROADMAP'),
                     ('satellite', 'SATELLITE'),
                     ('hybrid', 'HYBRID'),
                     ('terrain', 'TERRAIN')], string="Map Type", default="roadmap")
    search_radius = fields.Integer(string="Search Radius", default=5000)
    # google_api_key = fields.Char(string="Google Map API Key")

    manually_option = fields.Selection([('address', 'Address'),
                                        ('coordinate', 'Coordinate')
                                        ], string="Address Option", default='address')

    map_lat = fields.Float(string="Center Latitude")
    map_long = fields.Float(string="Center Longitude")
    street1 = fields.Char(string='Street 1')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='city')
    state = fields.Many2one('res.country.state', string="State Name")
    zipcode = fields.Char(string='zip code')
    country = fields.Many2one('res.country', string='Country Name', related="state.country_id")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set('res.config.settings', 'map_center', self.map_center)
        self.env['ir.default'].sudo().set('res.config.settings', 'map_zoom', self.map_zoom)
        self.env['ir.default'].sudo().set('res.config.settings', 'map_type', self.map_type)
        self.env['ir.default'].sudo().set('res.config.settings', 'search_radius', self.search_radius)
        self.env['ir.default'].sudo().set('res.config.settings', 'manually_option', self.manually_option)
        apikey = self.env['ir.config_parameter'].sudo().get_param("google.api_key_geocode") if self.env['ir.config_parameter'].sudo().get_param("google.api_key_geocode") else False
        if self.map_center == 'manually' and self.manually_option == 'address':
            coord = patho_map_geo_find(patho_map_geo_query_address(street=self.street1,
                                                        street2=self.street2,
                                                        zip=self.zipcode,
                                                        city=self.city,
                                                        state=self.state.name,
                                                        country=self.country.name), apikey)
            if coord:
                self.env['ir.default'].sudo().set('res.config.settings', 'map_lat', coord[0])
                self.env['ir.default'].sudo().set('res.config.settings', 'map_long', coord[1])
        else:
            self.env['ir.default'].sudo().set('res.config.settings', 'map_lat', self.map_lat)
            self.env['ir.default'].sudo().set('res.config.settings', 'map_long', self.map_long)
        self.env['ir.default'].sudo().set('res.config.settings', 'street1', self.street1)
        self.env['ir.default'].sudo().set('res.config.settings', 'street2', self.street2)
        self.env['ir.default'].sudo().set('res.config.settings', 'city', self.city)
        self.env['ir.default'].sudo().set('res.config.settings', 'state', self.state.id)
        self.env['ir.default'].sudo().set('res.config.settings', 'zipcode', self.zipcode)
        self.env['ir.default'].sudo().set('res.config.settings', 'country', self.country.id)
        return True

    @api.model
    def get_values(self, fields=None):
        res = super(ResConfigSettings, self).get_values()
        map_center = self.env['ir.default'].sudo().get('res.config.settings', 'map_center')
        map_zoom = self.env['ir.default'].sudo().get('res.config.settings', 'map_zoom')
        map_type = self.env['ir.default'].sudo().get('res.config.settings', 'map_type')
        search_radius = self.env['ir.default'].sudo().get('res.config.settings', 'search_radius')
        manually_option = self.env['ir.default'].sudo().get('res.config.settings', 'manually_option')
        map_lat = self.env['ir.default'].sudo().get('res.config.settings', 'map_lat')
        map_long = self.env['ir.default'].sudo().get('res.config.settings', 'map_long')
        street1 = self.env['ir.default'].sudo().get('res.config.settings', 'street1')
        street2 = self.env['ir.default'].sudo().get('res.config.settings', 'street2')
        city = self.env['ir.default'].sudo().get('res.config.settings', 'city')
        state = self.env['ir.default'].sudo().get('res.config.settings', 'state')
        zipcode = self.env['ir.default'].sudo().get('res.config.settings', 'zipcode')
        country = self.env['ir.default'].sudo().get('res.config.settings', 'country')
        res.update(
            {
                'map_center'     :   map_center,
                'map_zoom'       :   map_zoom,
                'map_type'       :   map_type,
                'search_radius'  :   search_radius,
                'manually_option':   manually_option,
                'map_lat'        :   map_lat,
                'map_long'       :   map_long,
                'street1'        :   street1,
                'street2'        :   street2,
                'city'           :   city,
                'state'          :   state,
                'zipcode'        :   zipcode,
                'country'        :   country,
            }
        )
        return res
