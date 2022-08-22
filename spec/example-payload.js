function getStyle() {
  const banner = Sentry.getFeatureFlagInfo("loginBanner");
  if (banner) {
    console.log("Using banner", banner.result);
    return {backgroundImage: "url(" + banner.payload.imageUrl + ")"};
  }
  return {};
}