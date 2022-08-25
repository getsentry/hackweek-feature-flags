# Hackweek: Feature Flags

You got features? We got flags!

```python
import sentry_sdk

sentry_sdk.init(
    environment="prod",
    _experiments={"feature_flags_enabled": True},
)

# this blocks until flags are fetched
sentry_sdk.wait_until_ready()

my_feature_flag = sentry_sdk.is_feature_flag_enabled("myFeatureFlag")
print(f"{my_feature_flag=}")
```

# Draft PRs

* [Dart SDK](https://github.com/getsentry/sentry-dart/pull/984)
* [Python SDK](https://github.com/getsentry/sentry-python/pull/1581)
* [Relay](https://github.com/getsentry/relay/pull/1433)
* [Sentry](https://github.com/getsentry/sentry/pull/38086)
