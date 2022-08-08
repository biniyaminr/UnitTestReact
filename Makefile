help:
	@echo "| ------------------------------------------------------------------------------------------------------- |"
	@echo "|    CITEC ECOSYSTEM"
	@echo "| ------------------------------------------------------------------------------------------------------- |"
	@echo "make build_citec_app_docker_l"
	@echo "make run_citec_app_docker_l"
	@echo "make build_citec_app_docker_p"
	@echo "make run_citec_app_docker_p"


build_citec_app_docker_l:
	@( cd citec_app && docker build -t citec_app . )

run_citec_app_docker_l:
	@( cd citec_app && docker run -p 3000:3000 --env-file .env citec_app)

build_citec_app_docker_p:
	@( cd citec_app && docker build -t citec_app . )

run_citec_app_docker_p:
	@( cd citec_app && docker run -p 80:80 --env-file .env citec_app)