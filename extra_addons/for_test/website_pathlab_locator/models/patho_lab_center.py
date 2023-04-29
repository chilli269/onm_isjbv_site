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

from odoo import models, fields, api, tools,  _
import requests
from datetime import date
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

ADDRESS_FIELDS = ('street1', 'zipcode', 'city', 'state_id', 'country_id')

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


def patho_map_geo_query_address(street1=None, zipcode=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(
        field for field in [street1, ("%s %s" % (zipcode or '', city or '')).strip(), state, country]
        if field
    ))


class LabCenters(models.Model):
    _inherit = 'patho.lab.centers'

    coordinate_calc = fields.Selection([('by_addr', 'By Address'),('manual', 'Manually')],
        string="Center Co-ordinates", default="by_addr")
    patho_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    patho_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    patho_lab_timings = fields.One2many("patho.lab.timings", "lab_id", string="Lab Timings")
    lab_image_ids = fields.One2many('patho.lab.image', 'lab_center_id', string='Images')
    lab_facility_ids = fields.Many2many('patho.lab.facility',
        string='Facility Available'
    )
    contact_address = fields.Char(compute='_compute_patho_contact_address', string='Patho Complete Address')
    note = fields.Text("Note")

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return list(ADDRESS_FIELDS)

    def _display_address(self):
        address_format = "%(street1)s\n%(city)s %(state_code)s %(zipcode)s\n%(country_name)s"
        args = {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        return address_format % args

    def _patho_display_address_depends(self):
        # field dependencies of method _display_address()
        return self._address_fields() + [
            'country_id.address_format', 'country_id.code', 'country_id.name',
            'state_id.code', 'state_id.name',
        ]

    @api.depends(lambda self: self._patho_display_address_depends())
    def _compute_patho_contact_address(self):
        for partner in self:
            partner.contact_address = partner._display_address()

    def on_patho_address_change(self):
        values = {}
        lab_locator_config_vals = self.env['res.config.settings'].sudo().get_values()
        apikey = self.env['ir.config_parameter'].sudo().get_param('google.api_key_geocode') or False
        result = patho_map_geo_find(patho_map_geo_query_address(street1=self.street1,
                                                    zipcode=self.zipcode,
                                                    city=self.city,
                                                    state=self.state_id.name,
                                                    country=self.country_id.name), apikey=apikey)
        if result:
            values['patho_latitude'] = str(result[0])
            values['patho_longitude'] = str(result[1])
        
        return values

    @api.model
    def create(self, vals):
        res = super(LabCenters, self).create(vals)
        if res.coordinate_calc == 'by_addr':
            result = res.on_patho_address_change()
            res.write({'patho_latitude': result.get('patho_latitude'),
                       'patho_longitude': result.get('patho_longitude'),
                       })
        return res

    def write(self, vals):
        param = ('street1', 'zipcode', 'city', 'state_id', 'country_id')
        for rec in self:
            res = super(LabCenters, rec).write(vals)
            if (vals.get('coordinate_calc') == 'by_addr') or (rec.coordinate_calc == 'by_addr' and any(key in vals for key in param)):
                result = rec.on_patho_address_change()
                rec.write({'patho_latitude': result.get('patho_latitude'),
                           'patho_longitude': result.get('patho_longitude'),
                           })
            return res


class PathoLabTimings(models.Model):
    _name = "patho.lab.timings"
    _descripton = "Patho Lab Timings"

    lab_id = fields.Many2one("patho.lab.centers", string="Lab Center")
    days = fields.Selection(selection=[
        ('monday','Monday'),
        ('tuesday','Tuesday'),
        ('wednesday','Wednesday'),
        ('thursday','Thusday'),
        ('friday','Friday'),
        ('saturday','Saturday'),
        ('sunday','Sunday')
        ], string="Day")
    status = fields.Selection(selection=[('open','Open'),('closed','Closed')], default="open", string="Open/Closed Status")
    open_time = fields.Float(string="Opening Time",required =True)
    close_time = fields.Float(string="Closing Time",required =True)

    def _check_time_values(self, vals):
        open_time = vals.get('open_time') if vals.get('open_time') else self.open_time
        close_time = vals.get('close_time') if vals.get('close_time') else self.close_time
        days = vals.get('days') if vals.get('days') else self.days
        lab_id = vals.get('lab_id') if vals.get('lab_id') else self.lab_id.id
        status = vals.get('status') if vals.get('status') else self.status

        if days and lab_id:
            time_slot = self.search([('lab_id','=',lab_id),('days','=',days),])
            if time_slot and time_slot.id != self.id:
                raise UserError(_("A record for the same day is created more than one time."))
        if status == 'open':
            if open_time >= close_time:
                raise UserError(_("Please enter a valid opening and closing time."))
            if open_time >= 24 or open_time < 0:
                raise UserError(_("Please enter a valid hour between 00:00 and 24:00"))
            if close_time >= 24 or close_time < 0:
                raise UserError(_("Please enter a valid hour between 00:00 and 24:00"))

    @api.model
    def create(self, vals):
        self._check_time_values(vals)
        res = super(PathoLabTimings, self).create(vals)
        return res

    def write(self, vals):
        for rec in self:
            rec._check_time_values(vals)
        res = super(PathoLabTimings, self).write(vals)
        return res


class PathoLabImage(models.Model):
    _name = 'patho.lab.image'
    _description ="Patho Lab Image"

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
    lab_center_id = fields.Many2one('patho.lab.centers', 'Related Lab', copy=True)

class PathoLabFacility(models.Model):
    _name = 'patho.lab.facility'
    _description ="Patho Lab Facility"

    name = fields.Char('Name', required=True)
    icon = fields.Binary('Icon')
