gateway-docker-image = "cr.yandex/crpnqn6joccbivjbkb27/api-gateway:1.4"

gateway-config = {
  environment = "testing"
  local-host  = "app"
  local-port  = 3000
}

postgres-config = {
  local-host  = "postgres"
  local-port  = 5432
  remote-port = 62467
}
