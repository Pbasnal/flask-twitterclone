provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    storage_account_name = "pbtfstatebackend2"
    container_name = "terraform"
    key = "data.terraform.tfstate"
  }
}

data "azurerm_resource_group" "rg" {
  name = "pbtfbackendrg"
}

resource "azurerm_user_assigned_identity" "uid" {
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location

  name = "registry-uai"
}

resource "azurerm_container_registry" "acr" {
  name                = "twittercloneacr"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  sku                 = "Basic"

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.uid.id
    ]
  }
}


