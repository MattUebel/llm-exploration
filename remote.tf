terraform {
  cloud {
    organization = "mattuebel-dot-org"

    workspaces {
      name = "llm-exploration"
    }
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}