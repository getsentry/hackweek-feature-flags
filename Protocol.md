# Feature Flag Protocol

This is a simplified protocol for this hackweek project with known limitations.
Right now SDKs can fetch from a new endpoint that Relay provides and will retrieve
updated feature flags there.  The downside of this approach is that Relay will
block for the project configs to become available.

The preferred option for the future would be to introduce a general return channel
on the envelope submission that Relay can send up information async.

## Endpoints

``POST /api/PROJECT_ID/feature-flags/``:
    Relay endpoint that returns the configuration packet specific to the input
    parameters.  eg: optionally filtered down to what is needed for the SDK to
    do it's job.

## API Bikeshedding

```javascript
if (Sentry.isFeatureFlagEnabled("enable_profiling", {
  // use global normally, this overrides
  "user_id": 42
})) {
  // something
}

// query a feature flag
const info = Sentry.getFeatureFlagInfo("show_banner");
if (info) {
  setBackgroundImage(info.payload["url"]);
}
```

## Feature Flag Names

Feature flag names are strings and the names are shared across types.
So a boolean feature flag named `a` can also be returned when evaluating a feature flag API returning a number.

Sentry internal feature flags are prefixed with `@@` to disambiugate them from
feature flags used by customers.

## Well Known Tags

The following tags are well known for the context:

- ``environment``: the name of the environment.
- ``release``: the name of the release.
- ``stickyId``: controls the stickyiness of the flag.  By default the user id is used
  and on mobile devices the device ID in addition as fallback.
- ``userId``: client SDKs should automatically provide this if a user ID is set.
  The stringified version is used as sticky ID if no sticky ID is defined.

## Well Known Feature Flags

- ``@sampleRate``: the error sample rate
- ``@tracesSampleRate``: the transaction based trace sample rate
- ``@profileSampleRate``: the sample rate for client side profiling

All the built-in tags do not carry payload and the UI does not emit it.

## Feature Flag Kinds

- `number`: any number
- `rate`: number between 0.0 and 1.0 (shown as percentage slider in the UI)
- `boolean`: true or false, shown as switch
- `string`: can be used to pick a variant

## Feature Flag Dump

This is what the feature flag dump API returns for the client to
evaluate:

```json
{
  "feature_flags": {
    "feature_flag_name": {
      // type of the value attached to the feature flag, contained in the field "result"
      "kind": "bool",
      // first match wins
      "evaluation": [
        {
          // this is a sticky gradual rollout (RNG seeded against sticky-id)
          "type": "rollout",
          "percentage": 0.5,
          "result": true,
          "payload": {...},
          "tags": {
            "segment": "a"
          }
        },
        {
          // if the tags match, then the result is returned
          "type": "match",
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
function rollRandomNumber(group, context) {
  const stickyId = context.stickyId || context.userId || context.deviceId;
  const seed = group + "|" + stickyId;
  const hash = sha1(seed);
  // use xorshift128 as in rand.py
  const rng = Xorshift128::new(hash.bytes);
  rng.random() // returns 0.0 to 1.0
}

function isFeatureFlagEnabled(name, context = undefined): boolean | null {
  const realContext = context || GLOBAL_CONTEXT;
  const config = allFeatureFlags[name];
  const group = config.group || name;
  for (const evalConfig of config.evaluation) {
    if (!matchesTags(evalConfig.tags, realContext)) {
      continue;
    }
    if (evalConfig.type === "rollout") {
      if (rollRandomNumber(group, realContext) >= evalConfig.percentage) {
        return evalConfig.result;
      }
    } else if (evalConfig.type === "match") {
      return evalConfig.result;
    }
  }
  return null;
}
```

## Public API

This might be changed to accept a generic `T` type when calling the Public API such as:

```dart
await Sentry.getFeatureFlagInfo<T>(key, {defaultValue: false, context: {}});
```

Hub class is the same as the Sentry static class but non-static.
