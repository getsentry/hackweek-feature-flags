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

## Feature Flag Names

Feature flag names are strings and the names are shared across types.
So a boolean feature flag named `a` can also be returned when evaluating a feature flag API returning a number.

Sentry internal feature flags are prefixed with `@@` to disambiugate them from
feature flags used by customers.

## Well Known Tags

The following tags are well known for the context:

- ``stickyId``: when this exists it's used as the primary ID for stickiness on rollouts.
- ``userId``: client SDKs should automatically provide this if a user ID is set.
  The stringified version is used as sticky ID if no sticky ID is defined.
- ``deviceId``: client SDKs should automatically provide this on mobile.

## Feature Flag Dump

This is what the feature flag dump API returns for the client to
evaluate:

```json
{
  "feature_flags": {
    "feature_flag_name": {
      // type of the value attached to the feature flag, contained in the field "result"
      "kind": "bool",
      // global tags that need to match for this flag to be considered at all
      "tags": {
        "key": "value"
      },
      // first match wins
      "evaluation": [
        {
          // this is a sticky gradual rollout (RNG seeded against sticky-id)
          "type": "rollout",
          "percentage": 0.5,
          "result": true,
          "payload": "optional extra payload",
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

function isFeatureEnabled(name, context = undefined): boolean | null {
  const realContext = context || GLOBAL_CONTEXT;
  const config = allFeatureFlags[name];
  const group = config.group || name;
  if (!matchesTags(config.tags, realContext)) {
    return null;
  }
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
await Sentry.getFeatureFlag<bool>(key, {defaultValue: false, context: {}});
```

Current state:

Sentry static class

```dart
static Future<bool> isFeatureFlagEnabled(
    String key, {
    bool defaultValue = false,
    FeatureFlagContextCallback? context,
  });
```

```dart
static Future<FeatureFlagInfo?> getFeatureFlagInfo(
    String key, {
    FeatureFlagContextCallback? context,
  });
```

Hub class is the same as the Sentry static class but non-static.

SentryClient class

```dart
Future<bool> isFeatureFlagEnabled(
    String key, {
    Scope? scope,
    bool defaultValue = false,
    FeatureFlagContextCallback? context,
  });
```

```dart
Future<FeatureFlagInfo?> getFeatureFlagInfo(
    String key, {
    Scope? scope,
    FeatureFlagContextCallback? context,
  });
```

Transport class

```dart
Future<Map<String, FeatureFlag>?> fetchFeatureFlags();
```
