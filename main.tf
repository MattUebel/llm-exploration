variable "location" {
  type    = string
  default = "eastus"
}

variable "sku_name" {
  type    = string
  default = "S0"
}

resource "azurerm_resource_group" "openai_rg" {
  name     = "openai-resource-group"
  location = var.location
}

resource "azurerm_cognitive_account" "openai" {
  name                = "my-openai-account"
  location            = azurerm_resource_group.openai_rg.location
  resource_group_name = azurerm_resource_group.openai_rg.name
  kind                = "OpenAI"
  sku_name            = var.sku_name
}

resource "azurerm_cognitive_deployment" "completion_model" {
  name                 = "gpt-4o"
  cognitive_account_id = azurerm_cognitive_account.openai.id
  model {
    format = "OpenAI"
    name   = "gpt-4o"
  }
  scale {
    type = "Standard"
  }
}

output "openai_endpoint" {
  value = azurerm_cognitive_account.openai.endpoint
}

output "openai_primary_key" {
  value     = azurerm_cognitive_account.openai.primary_access_key
  sensitive = true
}