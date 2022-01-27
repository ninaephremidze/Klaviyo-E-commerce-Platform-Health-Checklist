import os

stores = {
    'shopify':'',
    'bigcommerce':'',
    'woocommerce':'',
    'magento2':'',
    'directintegration':'',
}

for store in stores.keys():

    os.system('python3 demo_checks.py {store} {key}'.format(store=store, key=stores[store]))
