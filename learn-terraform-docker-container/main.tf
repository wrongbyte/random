terraform {
  # terraform providers are basically plugins that enable interactions with a specific API. We declare them here to tell terraform which services it needs to interact with. 
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.13.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.latest
  name  = "tutorial"

  ports {
    internal = 80
    external = 8000
  }
}
