# Copyright  2018 Forest and Biomass Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Romania - Fiscal Validation',
    'summary': 'Romania - Fiscal Validation',
    'version': '11.0.1.0.0',
    'category': 'Localization',
    'author': 'Forest and Biomass Romania, '
              'Odoo Community Association (OCA)',
    'website': 'https://www.forbiom.eu',
    'license': 'AGPL-3',
    'installable': True,
    'depends': ['l10n_ro_partner_create_by_vat',
                'l10n_ro_vat_on_payment'],
    'data': ['data/res_partner_vat_cron.xml'],
}
