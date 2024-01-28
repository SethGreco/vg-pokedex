# Makefile

run-tests: 
	docker exec -it vg-pokedex-fast-api-1 bash -c "pytest"

run-lint: 
	docker exec -it vg-pokedex-fast-api-1 bash -c "flake8"
