# Copyright 2017-2018 Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import werkzeug

from odoo import http, _
from odoo.http import request


class FormControllerMixin(object):

    # default template
    template = 'cms_form.form_wrapper'

    def get_template(self, form, **kw):
        """Retrieve rendering template.

        Defaults to `template` attribute.
        Can be overridden straight in the form
        using the attribute `form_wrapper_template`.
        """
        template = self.template

        if getattr(form, 'form_wrapper_template', None):
            template = form.form_wrapper_template

        if not template:
            raise NotImplementedError("You must provide a template!")
        return template

    def get_render_values(self, form, **kw):
        """Retrieve rendering values.

        You can override this to inject more values.
        """
        main_object = form.main_object
        parent = None
        if getattr(main_object, 'parent_id', None):
            # get the parent if any
            parent = main_object.parent_id

        kw.update({
            'form': form,
            'main_object': main_object,
            'parent': parent,
            'controller': self,
        })
        return kw

    def form_model_key(self, model, **kw):
        """Return a valid form model."""
        return 'cms.form.' + model

    def get_form(self, model, model_id=None, **kw):
        """Retrieve form for given model and initialize it."""
        form_model_key = kw.pop('form_model_key', None)
        if not form_model_key:
            form_model_key = self.form_model_key(model, **kw)
        if form_model_key in request.env:
            if model:
                main_object = request.env[model]
                if model_id:
                    main_object = request.env[model].browse(model_id)
            else:
                # HACK: odoo requires a stupid `main_object` to stay there
                # See https://github.com/odoo/odoo/pull/22384
                # So here we mock main_object to the form model recordset
                main_object = request.env[form_model_key]
            form = request.env[form_model_key].form_init(
                request, main_object=main_object, **kw)
        else:
            # TODO: enable form by default?
            # How? with a flag on ir.model.model?
            # And which fields to include automatically?
            raise NotImplementedError(
                _('%s model has no CMS form registered.') % model
            )
        return form

    def make_response(self, model, model_id=None, **kw):
        """Prepare and return form response.

        :param model: an odoo model's name
        :param model_id: an odoo record's id
        :param page: current page if any (mostly for search forms)
        :param kw: extra parameters

        How it works:
        * retrieve current main object if any
        * check permission on model and/or main object
        * retrieve the form
        * make the form process current request
        * if the form is successful and has `form_redirect` attribute
          it redirects to it.
        * otherwise it just renders the form
        """
        form = self.get_form(model, model_id=model_id, **kw)
        form.form_check_permission()
        # pass only specific extra args, to not pollute form render values
        form.form_process(extra_args={'page': kw.get('page')})
        # search forms do not need these attrs
        if getattr(form, 'form_success', None) \
                and getattr(form, 'form_redirect', None):
            # anything went fine, redirect to next url
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/303
            return werkzeug.utils.redirect(form.form_next_url(), code=303)
        # render form wrapper
        values = self.get_render_values(form, **kw)
        return request.render(
            self.get_template(form, **kw),
            values,
            headers={'Cache-Control': 'no-cache'}
        )


class CMSFormController(http.Controller, FormControllerMixin):
    """CMS form controller."""

    @http.route([
        '/cms/create/<string:model>',
        '/cms/edit/<string:model>/<int:model_id>',
    ], type='http', auth='user', website=True)
    def cms_form(self, model, model_id=None, **kw):
        """Handle a `form` route.
        """
        return self.make_response(model, model_id=model_id, **kw)


class WizardFormControllerMixin(FormControllerMixin):

    template = 'cms_form.wizard_form_wrapper'

    def make_response(self, wiz_model, model_id=None, page=1, **kw):
        """Custom response.

        The main difference w/ the base form controller is that
        we retrieve the form model via wizard step.
        """
        # init wizard 1st
        wiz = request.env[wiz_model].form_init(request, page=page, **kw)
        step_info = wiz.wiz_get_step_info(page)
        # retrieve form model for current step
        form_model = step_info['form_model']
        model = request.env[form_model]._form_model
        kw['form_model_key'] = form_model
        return super().make_response(model, model_id=model_id, page=page, **kw)


class CMSWizardFormController(http.Controller, WizardFormControllerMixin):
    """CMS wizard controller."""

    @http.route([
        '/cms/wiz/<string:wiz_model>/page/<int:page>',
    ], type='http', auth='user', website=True)
    def cms_wiz(self, wiz_model, model_id=None, **kw):
        """Handle a wizard route.
        """
        return self.make_response(wiz_model, model_id=model_id, **kw)


class SearchFormControllerMixin(FormControllerMixin):

    template = 'cms_form.search_form_wrapper'

    def form_model_key(self, model, **kw):
        return 'cms.form.search.' + model

    def get_render_values(self, form, **kw):
        values = super().get_render_values(form, **kw)
        values.update({
            'pager': form.form_search_results['pager'],
        })
        return values


class CMSSearchFormController(http.Controller, SearchFormControllerMixin):
    """CMS form controller."""

    @http.route([
        '/cms/search/<string:model>',
        '/cms/search/<string:model>/page/<int:page>',
    ], type='http', auth='public', website=True)
    def cms_form(self, model, **kw):
        """Handle a search `form` route.
        """
        return self.make_response(model, **kw)
