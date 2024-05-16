# odoo_custom_module

https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started.html

Run
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb
```

Run and update the module "test2024"
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb -u test2024
```

Run with debug
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb -u test2024 --log-level=debug
```

Run without having to reboot the server every time you do a modification to the view:
```bash
./odoo-bin --addons-path="addons, custom" -d rd-mydb -u test2024 --dev xml
```

