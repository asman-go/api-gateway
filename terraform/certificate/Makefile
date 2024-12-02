init:
	@terraform init

plan:
	@terraform get -update=true
	@terraform fmt -recursive
	@terraform validate
	@terraform plan

apply:
	@terraform apply
