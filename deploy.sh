docker-compose run --rm invite sh -c "python3 manage.py collectstatic"
docker-compose -f docker-compose-deploy.yml run --rm gcloud sh -c "gcloud app deploy --project rpl-a12"
docker-compose down