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

from odoo import http,fields
from odoo.http import request
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)

class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(max(p.website_size_x, 1), ppr)
            y = min(max(p.website_size_y, 1), ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1

            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:   # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                'product': p, 'x': x, 'y': y,
                'ribbon': p.website_ribbon_id,
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows

class WebsitePathology(http.Controller):
    @http.route(["/get/test_date"], type="json", auth="public", website=True)
    def _update_test_date(self, test_date=False, collect_center_id=False, comment=False,**kwargs):

        if test_date:
            dt = test_date
            d1 = datetime.strptime(dt,"%Y-%m-%d").date()
            d2 = date.today()
            rd = relativedelta(d2,d1)
            if rd.days > 0 or rd.months > 0 or rd.years > 0:
                return
        dob = kwargs.get('dob')
        request.session.update({'test_date': test_date,
            'collect_center_id': collect_center_id,
            'comment':comment,
            'gender':kwargs.get('gender'),
            'blood_group':kwargs.get('blood_group'),
            'dob':dob,
            'rh_factor':kwargs.get('rh_factor')})
        return True

    def _get_pricelist_context(self):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        return pricelist_context, pricelist


    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        order = post.get('order') or 'website_sequence ASC'
        return 'is_published desc, %s, id desc' % order

    def _get_search_domain(self, search, package, category, attrib_values, search_in_description=True):
        domains = [request.website.sale_product_domain()]
        if package:
            domains[0] += [('is_test', '=', False), ('is_test_package', '=', True)]
        else:
            domains[0] += [ '|', ('is_test', '=', True), ('is_test_package', '=', True)]

        if search:
            for srch in search.split(" "):
                subdomains = [
                    [('name', 'ilike', srch)],
                    [('product_variant_ids.default_code', 'ilike', srch)]
                ]
                if search_in_description:
                    subdomains.append([('description', 'ilike', srch)])
                    subdomains.append([('description_sale', 'ilike', srch)])
                domains.append(expression.OR(subdomains))

        if category:
            domains.append([('public_categ_ids', 'child_of', int(category))])

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domains.append([('attribute_line_ids.value_ids', 'in', ids)])
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domains.append([('attribute_line_ids.value_ids', 'in', ids)])

        return expression.AND(domains)

    def sitemap_shop(env, rule, qs):
        if not qs or qs.lower() in '/shop/test':
            yield {'loc': '/shop/test'}

        Category = env['product.public.category']
        dom = sitemap_qs2dom(qs, '/shop/test/category', Category._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for cat in Category.search(dom):
            loc = '/shop/test/category/%s' % slug(cat)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}


    @http.route([
        '''/shop/test''',
        '''/shop/test/page/<int:page>''',
        '''/shop/test/category/<model("product.public.category"):category>''',
        '''/shop/test/category/<model("product.public.category"):category>/page/<int:page>''',
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop_test(self, package=None, page=0, category=None, search='', ppg=False, **post):

        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, package, category, attrib_values)

        keep = QueryURL('/shop/test', package=package, category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

        # compute_currency, pricelist_context, pricelist = self._get_compute_currency_and_context()
        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop/test"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        # categs = request.env['product.public.category'].search([('pathology', '=', True),('parent_id', '=', False)])
        Product = request.env['product.template'].with_context(bin_size=True)

        search_product = Product.search(domain)
        website_domain = request.website.website_domain()
        categs_domain = [('pathology', '=', True),('parent_id', '=', False)] + website_domain

        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/test/category/%s" % slug(category)


        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
            'package':package,
        }
        if category:
            values['main_object'] = category
        return request.render("website_pathology.tests", values)


    @http.route(['/shop/test/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, package=None, category='', search='', **kwargs):
        if not product.can_access_from_current_website():
            raise NotFound()

        return request.render("website_pathology.test_page", self._prepare_product_values(product,package, category, search, **kwargs))

    def _prepare_product_values(self, product, package, category, search, **kwargs):
        add_qty = int(kwargs.get('add_qty', 1))

        product_context = dict(request.env.context, quantity=add_qty,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop/test', package=package, category=category and category.id, search=search, attrib=attrib_list)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        # Needed to trigger the recently viewed product rpc
        view_track = request.website.viewref("website_pathology.test_page").track

        return {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            'add_qty': add_qty,
            'view_track': view_track,
        }

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True)

    def checkout(self, **post):
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.redirect('/shop/address')

        for f in self._get_mandatory_fields_billing():
            if not order.partner_id[f]:
                return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)

        values = self.checkout_values(**post)

        if post.get('express'):
            return request.redirect('/shop/confirm_order')

        values.update({'website_sale_order': order})

        # Avoid useless rendering if called in ajax
        if post.get('xhr'):
            return 'ok'
        return request.render("website_sale.checkout", values)


    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        domains = [request.website.sale_product_domain()]
        domains[0] += [('is_test', '=', False), ('is_test_package', '=', False)]

        if search:
            for srch in search.split(" "):
                subdomains = [
                    [('name', 'ilike', srch)],
                    [('product_variant_ids.default_code', 'ilike', srch)]
                ]
                if search_in_description:
                    subdomains.append([('description', 'ilike', srch)])
                    subdomains.append([('description_sale', 'ilike', srch)])
                domains.append(expression.OR(subdomains))

        if category:
            domains.append([('public_categ_ids', 'child_of', int(category))])

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domains.append([('attribute_line_ids.value_ids', 'in', ids)])
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domains.append([('attribute_line_ids.value_ids', 'in', ids)])

        return expression.AND(domains)


    def sitemap_shop(env, rule, qs):
        if not qs or qs.lower() in '/shop':
            yield {'loc': '/shop'}

        Category = env['product.public.category']
        dom = sitemap_qs2dom(qs, '/shop/category', Category._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for cat in Category.search(dom):
            loc = '/shop/category/%s' % slug(cat)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}
        domain = self._get_search_domain(search, category, attrib_values)
        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if category:
            category = request.env['product.public.category'].browse(int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        search_product = Product.search(domain)
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False),('pathology', '=', False)] + website_domain
        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)


    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def shop_payment_confirmation(self, **post):
        """ End of checkout process controller. Confirmation is basically seing
        the status of a sale.order. State at this point :

         - should not have any context / session info: clean them
         - take a sale.order id, because we request a sale.order and are not
           session dependant anymore
        """
        sale_order_id = request.session.get('sale_last_order_id')
        if request.session.get('collect_center_id') and sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            order.write({'patho': True, })
            order.write({'note': request.session.get('comment'), })
            order.write({'test_date': fields.Date.to_date(request.session.get('test_date'))})
            order.write({'collection_center_id': request.session.get('collect_center_id')})
            gender = request.session.get('gender')
            blood_group = request.session.get('blood_group')
            dob = fields.Date.to_date(request.session.get('dob'))
            rh_factor = request.session.get('rh_factor')
            order.partner_id.write({
                'gender':gender,
                'blood_group':blood_group,
                'patient_dob':dob,
                'rh_factor':rh_factor,
                'patient':True
            })
        return super().shop_payment_confirmation(**post)
