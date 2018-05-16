.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

========================
QWeb for email templates
========================

This module was written to allow you to write email templates in QWeb instead
of jinja2. The advantage here is that with QWeb, you can make use of
inheritance and the ``call`` statement, which allows you to reuse designs and
snippets in multiple templates, making your development process simpler. 
Furthermore, QWeb views are easier to edit with the integrated ACE editor.

Usage
=====

To use this module, you need to:

#. Select `QWeb` in the field `Body templating engine`
#. Select a QWeb view to be used to render the body field
#. Apart from QWeb's standard variables, you also have access to ``object`` and ``email_template``, which are browse records of the current object and the email template in use, respectively.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/205/11.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/social/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://odoo-community.org/logo.png>`_.

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>
* Dave Lasley <dave@laslabs.com>
* Carlos Lopez Mite <celm1990@gmail.com>

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
