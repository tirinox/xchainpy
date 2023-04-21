# How it works
Typically keystore files encrypt a seed to a file, however this is not appropriate or UX friendly, since the phrase
cannot be recovered after the fact.

Crypto design:

`[entropy] -> [phrase] -> [seed] -> [privateKey] -> [publicKey] -> [address]`

Instead, XCHAIN-CRYPTO stores the phrase in a keystore file, then decrypts and passes this phrase to other clients:

`[keystore] -> XCHAIN-CRYPTO -> [phrase] -> ChainClient`

The ChainClients can then convert this into their respective key-pairs and addresses. Users can also export their
phrases after the fact, ensuring they have saved it securely. This could enhance UX onboarding since users aren't forced
to write their phrases down immediately for empty or test wallets.
