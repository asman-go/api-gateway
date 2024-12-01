plan:
	@terraform get -update=true
	@terraform fmt -recursive
	@terraform validate
	@terraform plan -var-file ./secrets.tfvars

apply:
	@terraform apply -var-file ./secrets.tfvars
