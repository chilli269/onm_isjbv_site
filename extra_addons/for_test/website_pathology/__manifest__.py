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
  "name"                 :  "Website Pathology Lab Management System",
  "summary"              :  """The module allows you to manage your Pathology lab business in Odoo. The customers can schedule lab test directly from the Odoo website.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Website-Pathology-Lab-Management-System.html",
  "description"          :  """Odoo Website Pathology Lab Management System
Book labtests in Odoo
Run pathology lab in Odoo
Odoo pathology
Use website for lab test
Book Blood tests in Odoo""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_pathology&lifetime=60&lout=1&custom_url=/shop/test",
  "depends"              :  [
                             'wk_pathology_management',
                             'website_sale',
                             'website_payment',
                             'account_payment',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'security/access_control_security.xml',
                             'views/inherit_website_template.xml',
                             'views/inherit_patho_labtest_view.xml',
                             'views/inherit_website_cart_template.xml',
                             'views/patho_lab_test_category.xml',
                             'views/patho_my_account_menu_template.xml',
                             'data/website_pathology_data.xml',
                            ],
  "assets"               : {
          'web.assets_frontend': [
                          'website_pathology/static/src/css/website_patho.css',
                          'website_pathology/static/src/js/website_pathology_mgmt.js',
                          'website_pathology/static/src/js/bootbox.min.js',
                      ],},
  "demo"                 :  ['demo/website_patho_demo_data.xml'],
  "images"               :  ['static/description/Banner.gif'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  76,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
