At this point, I'm just playing. I need to learn a lot more about Python before I can create any real code.

This code is just to get a deeper understanding of how a block chain protocol like bitcoin works. Because of this, it ignores some things that would be required to actually access bitcoin blocks and transacations:

1. The order of bits/bytes (little/big endian) is not considered. This means that hashes (or digests) of blocks, transactions, and merkle roots will NOT match those generated for the same objects in bitcoin. That is, you can't test this code using blocks from the Bitcoin block chain.

2. Where varints are used in the Bitcoin structures for blocks and transactions, this code uses a fixed length of 4 bytes for length counts. This has the same affect as ignoring little/big endian issues: this code will not work correctly if used against objects from the Bitcoin block chain.

Test sub repos
