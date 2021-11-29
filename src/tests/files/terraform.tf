resource "test" "test" {
    name = "${var.group_name}-test"
    users = var.test
    group = var.test
  }
