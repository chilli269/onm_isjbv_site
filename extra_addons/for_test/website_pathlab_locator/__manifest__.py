# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
{
  "name"                 :  "Pathology Lab Center Locator",
  "summary"              :  """The module facilitates the customers to locate a pathology lab using Google maps. The location is available on the Odoo website for the customers.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Pathology-Lab-Center-Locator.html",
  "description"          :  """Odoo Pathology Lab Center Locator
Locate lab on Google Map
Add pathology lab address on Google Map
Integrate pathology lab with maps
Location of collection center on Google maps""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_pathlab_locator",
  "depends"              :  ['website_pathology'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'security/access_control_security.xml',
                             'views/patho_mgmt_config_view.xml',
                             'views/patho_lab_centers_view.xml',
                             'views/templates.xml',
                            ],
  "assets"               : {
                        'web.assets_frontend':[
                          'website_pathlab_locator/static/src/css/patho_lab_center_locator.css',
                          'website_pathlab_locator/static/src/js/patho_lab_center_locator.js',
                        ],
                          },
  "demo"                 :  ['data/patho_lab_center_locator_data.xml'],
  "images"               :  ['static/description/Banner.gif'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  64,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
