# odoo_custom_module

https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started.html

Run
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb
```

Run and update the module "estate"
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb -u estate
```

Run with debug
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb -u estate --log-level=debug
```

Run without having to reboot the server every time you do a modification to the view:
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb -u estate --dev xml
```

