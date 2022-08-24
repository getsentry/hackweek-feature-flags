# Video Script

```
April 18th: Outside

Unnamed Cryptobro is on the way to his favorite Bubble Tea place.
He is wearing Airpods Max.  While walking we see him sign into 
his Fahrenheit app and check his massive gains.

        Cryptobro, mumbling to himself:
    
    "When lambo?"

May 5th 2022: Fahrenheit Networks Office

        Narrator

    "We're at the office of Fahrenheit Networks, a crypto lending
    platform by Sascha Kaminski.  Today a big stable coin crashed
    and people are panicking.  Everybody keeps hammering refresh
    to see what's happening to their portfolios.

Kaminski enters the room looking like he's on coke

        Kaminiski

    "Hey Celi, we're being crushed out there.  The app keeps
    crashing and Twitter is killing us.  Get on it now!"

Celi sits on the desk, looking at her monitor.

        Celi

    "I will have a look.  If I can't fix it for everybody, is
    there someone we care about in particular?"

        Kaminski

    "Prioritize the whales."

        Narrator

    "Celi knows that Fahrenheit Networks is prioritizing bling
    over everything else.  They are using Sentry to monitor their
    backend and frontend applications but because money at the
    company goes towards parties, private jets and other things
    rather than towards observability tools, they are having
    barely any insights.  Their Sentry installation runs at an
    abusmally low client side sample rate."

        Celi, slacks her coworker

    "@jon come over here, I need to pair up with your for a sec"

Jon enters the room

        Jon

    "Sup?"

        Celi

    "I want to increase the client side sample rate for our
    whales on the app so I can see what they are running into.
    Wanna double check what I'm doing?"

        Jon

    "Sure"

        Celi

    Navigates to the project settings page for the "hodlponzi-ios"
    app on Sentry.

    We can see her go to the feature flags page which does not
    show any settings applied.

        Celi

    "Do you know what the client side sample rate is currently set
    to?"

        Jon

    "You can see that from the dynamic sampling settings page.
    Let me check quickly."

    Jon navigates to the settings page on his phone off screen

    "Looks like it's set to under 1%"

        Celi

    "I will bump this up to 20% for all whales"

    We see Celi add a rule new toggle called "@@tracesSampleRate"
    numeric.  She adds a custom filter for "is_whale" and "true"
    with the numeric result set to 0.2.

        Jon

    "While you're at it, can we also turn on all sampling for the
    dev build?  I want to try to see what we can do on the
    testflight app."

        Celi

    Celi adds another rule to "@@tracesSampleRate" with the
    `dev` environment set to 1.0.

    Celi also adds a rule for "@@sampleRate" and bumps it up to
    1.0 for whales (tag is "is_whale" and "true" as value).

    "I am also going to bump up the errors for whales to 100%".

Celi and Jon are going to the office cafeteria

        Celi

    "Let's give it a few minutes to propagate and have a look at
    what's going on.  I'm assuming the app is actually fine and
    what's happening is that the backend services are having
    troubles with the increased load."

        Jon

    "What flags do we have on the client that we could use to
    improve the situation?"

        Celi

    "The obvious ones are the HODL mode.  When enabled it locks
    the user out of most functionality.  They can't sell any more
    tokens for instance."

        Jon

    "If we do that, won't people be super frustrated?"

        Celi

    "We don't need to remove too much load, we can just roll it
    out for a few users and make sure whales are not in HODL
    mode."

Celi and Jon are back in the office

        Celi

    Navigates to the settings page and adds a new toggle called
    "hodlModeActivated" as bool.

    She adds a rule for "is_while" "true" which returns false.

    She configures a rollout of 5% which returns true.

    "Now 5% of users are in HODL mode and no whale".

        Jon

    "Didn't we also have a way to change the UI?  Maybe we can
    turn on some calming backgrounds when opening the app."

        Celi
    
    Adds a new flag "backgroundImage" with "string" and sets
    it to "https://hdlpzicdn.com/assets/420.png" for all users.

We see Cryptobro walking outside

    He is looking at his phone showing massive losses.

    He lifts is hands and holds them to his head.

    "What is going on?"

    Cryptobro looks at his phone on a Tweet that says that
    Fahrenheit is going bankrypt and rolling out HODL mode.

Kaminski enters the room:

        Kamisnki shouts at Celi

    "ROLL OUT HODL MODE FOR EVERYBODY"

        Celi

    "Are you serious?"

    Celi removes all conditions from hodl mode and adds a
    single match setting it to true.

Cryptobro looks at his phone again and sees HODL mode

Cut to black

        Narrator

    "A day later Fahrenheit would file for Chapter 7."

    "Sadly Sentry can also be used for evil or just batshit
    stupid things.  Feature flags are still great though."
```