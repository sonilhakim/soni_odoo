
{
    'name': 'Sale Order Multipayment',
    'version': '1.1',
    'sequence': 3,
    "version"       :   "1.0.1",
    "author"        :   "CraftSync Technologies",
#     "summary"   :   """ 
#                 Add Multiple payments to Sale order. 
#                 """,

    'website': 'https://www.craftsync.com/',
    'support':'info@craftsync.com',
    'depends': [
                'sale_management','account',
                ],
    'data': [
            'view/account_journal_view.xml',
            'view/sale_order_view.xml',
            'view/account_invoice.xml',
            "security/ir.model.access.csv",
             ],
    'demo': [],
    "application"          :  True,
    "auto_install"         :  False,
}
