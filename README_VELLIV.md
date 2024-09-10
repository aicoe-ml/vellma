# We should have our own README file for Velliv-specific changes to the official Open Web UI repo

## How to run

Currently Vellma is started on the server with the following command:

```bash
docker-compose -f docker-compose.yaml -f docker-compose.gpu.yaml up -d --build
```

## How to contribute

We pull from the officiel Open Web UI repo and keep the branch `main` in sync with the official repo.
We add our Velliv-flavor to the `prod` branch.

State of 2024-09-10: The changes in `prod` is not automatically deployed to Vellma. A manual `git pull` and `docker-compose -f docker-compose.yaml -f docker-compose.gpu.yaml up -d --build`

To-be deployement pipeline: 

1. Changes are pushed to `prod`
2. This triggers Github Action pipeline that:
   1. Pulls changes
   2. Switches to the maintenance page, dev'ed by @Nicolai
   3. Restarts the Vellma service with `docker compose up ...` 
   4. Confirms that the service is back up
   5. If all is well:
      1. Take maintenance page down again
   6. If something is not well:
      1. `git rollback ...` rolls back to previous commit
      2. Restarts the Vellma service
      3. Sends mail/Teams message to AICoE team/Brian

## Notes on the vellma3.1:70b base model

I created a new model file, based on the original Llama model file (retrieved with `ollama show --modelfile llama3.1:70b`), and created a new base model using the OpenWebUI interface Admin Settings -> Models. See my comment on [this github issue](https://github.com/open-webui/open-webui/issues/3106)

I also uploaded the new modified model file to [our fork](./Velliv%20models/vellma.model)
