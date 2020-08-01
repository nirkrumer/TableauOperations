# TableauOperation

This project uses Tableau Python SDK in order to perform several operations on Tableau server & application:
1. Creates Tableau report snapshot and injects it in a mail, which is sent to the management.
2. Finds Tableau report by name and runs its extract.

These operations are maintained in jenkins space and can be called by an api call, using CURL
