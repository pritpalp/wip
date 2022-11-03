# tfplan.py

## Requirements
 * Python 3
 * Text file containing a list of modules
 * Terraform 0.12+

## Description
This script uses a list of modules to run targeted "terraform plan" on those modules.

It was found that certain resources, once created, caused the terraform plan/apply to take a very long time to process (blob storage in this case). Targetting the required modules makes this process much faster by only looking at the resources that we know we are going to change.

But the Terraform 0.12.x introduced a nicer view of the differences, but as our modules contained ARM templates as well - the output produced for them requires a lot of scrolling around to visually check the changes being applied.

This script extracts the actual changes in the modules to make the output easier to read.

## How to Use

The file containing the list of modules:
``` text
➜  master git:(master) cat text.txt
lpg-ui
notification-service
➜  master git:(master)
```
Running tfplan.py (when we add resources):
``` bash
➜  master git:(master) python3 tfplan.py test.txt
Running the plan for these modules:
['lpg-ui', 'notification-service']

-----------------


  # module.lpg-ui.azurerm_template_deployment.lpg-ui-app-service will be created

  # module.notification-service.azurerm_template_deployment.notification-service-app-service will be created

Plan: 2 to add, 0 to change, 0 to destroy.

➜  master git:(master)
```
Running tfplan.py (when we modify resources):
``` bash

```
