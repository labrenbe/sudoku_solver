solve:
	gcloud functions deploy solve_sudoku \
	--source=./backend/solve_sudoku \
	--entry-point=solve_sudoku \
	--runtime=python39 \
	--trigger-http \
	--max-instances=3 \
	--memory=256MB \
	--ingress-settings=all \
	--allow-unauthenticated

generate:
	gcloud functions deploy generate_sudoku \
	--source=./backend/generate_sudoku \
	--entry-point=generate_sudoku \
	--runtime=python39 \
	--trigger-http \
	--max-instances=3 \
	--memory=256MB \
	--ingress-settings=all \
	--allow-unauthenticated

website: build_website
	gcloud app deploy ./frontend/app.yaml

build_website: generate_env
	npm run build --prefix ./frontend

generate_env:
	@echo 'VUE_APP_SOLVE_URL=${gcloud functions describe solve_sudoku --format="value(httpsTrigger.url)"}' > ./frontend/.env
	@echo 'VUE_APP_GENERATE_URL=${gcloud functions describe generate_sudoku --format="value(httpsTrigger.url)"}' > ./frontend/.env
	cat ./frontend/.env
