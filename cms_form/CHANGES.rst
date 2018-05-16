=========
CHANGELOG
=========

11.0.1.4.1 (2018-04-29)
=======================

Docs
----

* Move documentation from README to `doc` folder


11.0.1.4.0 (2018-04-27)
=======================

Improvements
------------

* Include wizard name in form wrapper klass
* Add request marshallers and tests
* Search form: pass `pager` as render value

  This change is to facilitate templates that need a pager
  to generate page metadata (like links prev/next).

  A good use case is the SEO friendly `website_canonical_url`.

* Rely on `cms_info` for permission and URLs


Fixes
-----

* Fix `fake_session` helper in form tests common


11.0.1.3.1 (2018-04-22)
=======================

Improvements
------------

* Wizard: ease customization of stored values

  To customize stored values you can override `_prepare_step_values_to_store`


11.0.1.3.0 (2018-04-17)
=======================

Improvements
------------

* Add wizard support to easily create custom wizards


11.0.1.2.1 (2018-04-13)
=======================

Fixes
-----

* Fix search form regression on permission check

  In 32a662e I've moved permission check from controller to form
  but I missed the bypass for search forms.


11.0.1.2.0 (2018-04-09)
=======================

Improvements
------------

* Add error msg block for validation errors right below field
* Support multiple values for same field

  In the input markup you can set the field name as `$fname:list`.

  This will make the form transform submitted values as a list.

  Example::

      <input name="foo:list" type="checkbox" value="1" />
      <input name="foo:list" type="checkbox" value="2" />
      <input name="foo:list" type="checkbox" value="3" />

  Will be translated to: `{'foo': [1, 2, 3]}`


* Add `lock copy paste` option

  You can now pass `lock_copy_paste` to widget init via `css_klass` arg
  to set an input/text w/ copy/paste disabled.

  Example::

      def form_get_widget(self, fname, field, **kw):
          """Disable copy paste on `foo`."""
          if fname == 'foo':
              kw['css_klass'] = 'lock_copy_paste'
          return super().form_get_widget(fname, field, **kw)


* `form_get_widget` pass keyword args to ease customization
* Form controller: better HTTP status for redirect (303) and no cache
* Improve custom attributes override
* Move `check_permission` to form

  You can now customize permission check on each form.
  Before this change you had to override the controller to gain control on it.


Fixes
-----

* Fix required attr on boolean widget (was not considered)
* `_form_create` + `_form_write` use a copy of values to avoid pollution by Odoo
* Fix handling of forms w/ no form_model
  (some code blocks were relying on `form_model` to be there)


11.0.1.1.1 (2018-03-26)
=======================

Fixes
-----

* Fix date widget: default today only if empty


11.0.1.1.0 (2018-03-26)
=======================

Improvements
------------

* Delegate field wrapper class computation to form
* Add vertical fields option
* Add multi value widget for search forms
* Improve date widget: allow custom default today

Fixes
-----

* Fix fieldset support for search forms
* Fix date search w/ empty value
* Fix json params rendering on widgets


11.0.1.0.4 (2018-03-23)
=======================

Improvements
------------

* Ease override of JSON info
* Add fieldsets support
* cms_form_example: add fieldsets forms


11.0.1.0.3 (2018-03-21)
=======================

Improvements
------------

* Form controller: main_object defaults to empty recordset

Fixes
-----

* Fix x2m widget value comparison
* Fix x2m widget load default value empt^^
