provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "backendrg" {
  name     = "pbtfbackendrg"
  location = "West Us"
}

resource "azurerm_storage_account" "store" {
  name                     = "pbtfstatebackend2"
  resource_group_name      = azurerm_resource_group.backendrg.name
  location                 = azurerm_resource_group.backendrg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "terraform" {
  name                 = "terraform"
  storage_account_name = azurerm_storage_account.store.name
}
