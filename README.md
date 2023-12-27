## Inspiration
Bonsai was inspired by AI's ability to summarize things and how time-consuming it is to sift through all the emails I receive. We believe seeing a quick summary of the emails that matter will vastly improve your productivity.

## What it does
Bonsai is an app that summarizes your most important emails; and then sends a text. Users can also whitelist or blacklist topics, or translate email summaries into a language they are more familiar with.

## How we built it
Our backend utilized Python+FastAPI for its ability to quickly prototype and make software that gets the job done. Javascript+React was chosen for the front end for the same benefits. MongoDB was also very effective for us because we only needed to query by a primary key. The backend integrates with Twilio and Google Cloud Services to send text messages whenever an email is received.

## Challenges we ran into
Google cloud services suffer from overdocumentation. There is so much documented information that's superseded by newer protocols and the docs don't give you a hint that you are doing everything wrong. The client-side libraries also have code snippets but don't have any explanations of what the code in the snippets actually does.
Firefox also has rendering issues on Linux and Windows doesn't support SSL handshakes apparently. Because Bonsai relies on so many APIs, it's difficult for us to be sure your data is safe. This was difficult for us to fix during the time we had, so we decided to allow many security issues.

## Accomplishments that we're proud of
We took on a project with a big scope and accomplished every one of our non-negotiable goals.

## What we learned
It's important to read the entire documentation before you start programming. We learned that it's good to spend time on polish because you only have one first impression. Communication between team members is very crucial. We also reflected on our decision to skip pull requests so we could save time. We ended up losing time to merge conflicts.

## What's next for Bonsai
Bonsai's proof of concept is done. While developing the app, we realized it was much more useful than we imagined. A second version of Bonsai would be a game-changer for productivity. Fixing the security issues and refining the user experience is the next step in Bonsai's journey.