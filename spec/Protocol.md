# Feature Flag Protocol

The idea is to allow both client and server side validation of feature flags.
We prioritize client side evaluation for now.

## Endpoints

``POST /api/PROJECT_ID/feature-flags/``:
    Relay endpoint that returns the configuration packet specific to the input
    parameters.  eg: optionally filtered down to what is needed for the SDK to
    do it's job.

## API Bikeshedding

```javascript
if (Sentry.isFeatureEnabled("enable_profiling", {
  // use global normally, this overrides
  "user_id": 42
})) {
  // something
}

// for future, ignore for now.
const info = Sentry.getVariant("show_banner");
if (info) {
  setBackgroundImage(info.payload["url"]);
}
```

## Feature Flag Dump

```json
{
  "feature_flags": {
    "feature_flag_name": {
      "tags": {
        "key": "value"
      },
      "evaluation": [
        {
          "type": "rollout",
          "percentage": 0.5,
          "result": true,
          "tags": {
            "segment": "a"
          }
        },
        {
          "type": "rollout",
          "percentage": 0.1,
          "result": true,
          "tags": {
            "segment": "b"
          }
        },
      ]
    }
  }
}
```

```javascript
function isFeatureEnabled(name, context) {
  const realContext = context || GLOBAL_CONTEXT;
  const config = allFeatureFlags[name];
  if (!matchesTags(config.tags, realContext)) {
    return false;
  }
  for (const evalConfig of config.evaluation) {
    if (!matchesTags(evalConfig.tags, realContext)) {
      continue;
    }
    if (evalConfig.type === "rollout") {
      if (rollRandomNumber(realContext) >= evalConfig.percentage) {
        return true;
      }
    }
  }
  return false;
}
```