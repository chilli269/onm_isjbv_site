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
from odoo.http import request

class Website(models.Model):
    _inherit = 'website'

    @api.model
    def patho_get_map_api_url(self):
        map_api_url = '//maps.googleapis.com/maps/api/js?libraries=places'
        google_api_key = request.env['ir.config_parameter'].sudo().get_param('google_maps_api_key') or False
        if google_api_key:
            map_api_url = '//maps.googleapis.com/maps/api/js?libraries=places&key=' + str(google_api_key)
        return map_api_url
