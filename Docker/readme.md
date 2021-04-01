# Agent setup
This readme will explain how to setup an agent for the VON-Network.

There are a few steps to follow before we are up and running.
- Step 1 (Optional): Setup a VON-Network
- Step 2 : Update the .env file 
  - Update the LEDGER_URL variable to point to the URL of the ledger (this could be a local ledger (192.168.65.3:9000), or a public ledger (http://greenlight.bcovrin.vonx.io/))
  - Update the Seed to a random 32 byte value
  - Update the Alias to something you can recognize (eg. Test_Patient_MNNU)
- Step 3: Run `docker-compose -f docker-compose.yml up --build`

After running the docker-compose command and all the correct images are pulled from the internet,
the docker compose will first register a "DID" (Account) on the ledger you specified with the SEED variable.

Then, an agent will be connected to that Account that has just been created on the ledger.

If everything was setup properly, the terminal will show you something similar to this screen:

![Good Setup](../Resources/proper_setup.png "Proper Setup")
