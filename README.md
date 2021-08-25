# report-build

---

## 🔴 This is a public repository 🔴

---
### Description
This is a Bitrise step to collect certain Bitrise build information and send it to EZDeploy

### Prerequisites
- `DEV_EZDEPLOY_API_URL` and `PROD_EZDEPLOY_API_URL` need to be set as env vars
This can be done as such:
```yaml
- app:
     envs:
        - opts:
              is_expand: false
          DEV_EZDEPLOY_BUILD_URL: "https://INSERT_DEV_API_ROUTE_HERE"
        - opts:
              is_expand: false
          PROD_EZDEPLOY_BUILD_URL: "https://INSERT_PROD_API_ROUTE_HERE"
```
- `EZDEPLOY_AUTH_TOKEN` is needed to authenticate with EZDeploy while sending the build.
This can be added via the desired apps secrets tab on Bitrise
  
### Usage
- Add a step call within the desired workflow of your `bitrise.yml` to report to dev as such:
```yaml
- git::https://github.com/WhoopInc/bitrise-step-report-build.git@master:
     title: Send build to dev ez-deploy
     inputs:
        - url: $DEV_EZDEPLOY_BUILD_URL
     is_always_run: true
     is_skippable: true
```
and to report to prod as such:
```yaml
- git::https://github.com/WhoopInc/bitrise-step-report-build.git@master:
     title: Send build to prod ez-deploy
     inputs:
        - url: $PROD_EZDEPLOY_BUILD_URL
     is_always_run: true
     is_skippable: true
```

- The only required input is the url input, however the step implicitly takes in other environment variables. 
  A full list can be found [here](https://github.com/WhoopInc/bitrise-step-report-build/blob/master/step.yml#L34).
  Out of all the listed variables, only `$STARTED_AT`, `$COMPLETED_AT`, `$TOTAL_DURATION` and `$EZDEPLOY_AUTH_TOKEN`
  are not part of the bitrise environment by default. These variables will have to be exported as environment variable
  in your `bitrise.yml` prior to calling the step. Examples of doing so are listed here:
  ```yaml
  - script@1:
     title: Get time started at
     inputs:
        - content: |
            #!/usr/bin/bash
            envman add --key STARTED_AT --value $(date  +"%Y-%m-%dT%H:%M:%S.%3N%z")
     is_always_run: true
     is_skippable: true
  ```
  ```yaml
  - script@1:
     title: Get time completed at
     inputs:
        - content: |
            #!/usr/bin/bash
            envman add --key COMPLETED_AT --value $(date  +"%Y-%m-%dT%H:%M:%S.%3N%z")
     is_always_run: true
     is_skippable: true
  ```
  ```yaml
  - script@1:
     title: Get total duration of build in ms
     inputs:
        - content: |
            #!/usr/bin/bash
            if [ ! -z $STARTED_AT ]
            then
              envman add --key TOTAL_DURATION --value $(($(date -d "$COMPLETED_AT" "+%s%N")/1000000 - $(date -d "$STARTED_AT" "+%s%N")/1000000))
            fi
     is_always_run: true
     is_skippable: true
  ```
  - The `started_at` step should be the first step to run in the workflow in order to accurately measure build duration.
  - Conversely, he `completed_at` and `total_duration` step should be the last step in the workflow.
- Setting both `is_always_run` and `is_skippable` to `true` is recommended to report failing tests to EZDeploy
as well as preventing reporting failures from failing the overall build as a whole.