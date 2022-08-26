# Hackweek: Feature Flags

You got features? We got flags!

This hackweek project implements client side feature flags for
Sentry.  It's supported in the Python and Dart SDK on branches.

Looks like this:

```python
import sentry_sdk

sentry_sdk.init(
    environment="prod",
    _experiments={"feature_flags_enabled": True},
)

# this blocks until flags are fetched
sentry_sdk.wait_until_ready()

if sentry_sdk.is_feature_flag_enabled("myFeatureFlag"):
    print("Feature flag enabled!")
```

<img src="https://github.com/getsentry/hackweek-feature-flags/blob/main/screenshots/overview.png?raw=true" width="100%" alt="screenshot">

# How does it work?

There is a Sentry UI where basic rules can be defined for feature flags.
Multiple feature flags can be defined with multiple segments within each
flag to control how they are rolled out.  Each segment is matched against
the provided tags and the first segment that matches defines the result.

Feature flags can be numeric, boolean or string types and additionally
they can carry arbitrary JSON payload though this is currently not yet
exposed throughout the UI.

Additionally special internal feature flags are used and directly
influence the SDK.  This way the sample rate for erros and transactions
can be remotely reconfigured.  The same is also true for the experimental
profiling on the Python SDK.

Feature flags that are active are pushed out via Relay to client SDKs and
evaluated there.

Feature flags are sticky by user or device and multiple feature flags can
be grouped together to ensure that they are rolled out together if wanted.

# Draft PRs

* [Dart SDK](https://github.com/getsentry/sentry-dart/pull/984)
* [Python SDK](https://github.com/getsentry/sentry-python/pull/1581)
* [Relay](https://github.com/getsentry/relay/pull/1433)
* [Sentry](https://github.com/getsentry/sentry/pull/38086)

# Nice-to-have Features

* Force random stickiness (disabled by default), useful for non-user-facing features
* Date and Time expiration, enable HTTP payload for errors directly from the Issues page for only 1h
* Built-in feature flag to SDKs to enable verbose reporting (attachments for full outgoing HTTP requests and their responses)
* Basic reusable segments (list of VIP orgs) that can be referenced.
