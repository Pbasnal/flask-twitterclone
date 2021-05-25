provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    storage_account_name = "pbtfstatebackend2"
    container_name       = "terraform"
    key                  = "app.terraform.tfstate"
  }
}

data "azurerm_resource_group" "rg" {
  name = "pbtfbackendrg"
}

data "azurerm_user_assigned_identity" "uid" {
  name                = "registry-uai"
  resource_group_name = data.azurerm_resource_group.rg.name
}

resource "azurerm_app_service_plan" "twittercloneserviceplan" {
  name                = "twitterclone-appserviceplan"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  kind                = "Linux"    # For Linux
  reserved            = true       # For Linux

  sku {
    tier     = "Standard"
    size     = "S1"
  }
}

resource "azurerm_app_service" "app" {
  name                = "twittercloneapp"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.twittercloneserviceplan.id

  site_config {
    linux_fx_version          = "DOCKER|twittercloneacr.azurecr.io/senti:latest" #define the images to usecfor you application
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      data.azurerm_user_assigned_identity.uid.id
    ]
  }
  app_settings = {}
}

# resource "azurerm_app_service_slot" "my_app_service_container_staging" {
#   name                    = "staging"
#   app_service_name        = azurerm_app_service.app.name
#   location                = data.azurerm_resource_group.rg.location
#   resource_group_name     = data.azurerm_resource_group.rg.name
#   app_service_plan_id     = azurerm_app_service_plan.twittercloneserviceplan.id
#   https_only              = true
#   client_affinity_enabled = true
#   site_config {
#     scm_type          = "VSTSRM"
#     always_on         = "true"
#     health_check_path = "/login"
#   }

#   identity {
#     type         = "SystemAssigned, UserAssigned"
#     identity_ids = [data.azurerm_user_assigned_identity.uid.id]
#   }

#   app_settings = {}
# }
