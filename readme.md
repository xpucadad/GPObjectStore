At this point, I'm just playing. I need to learn a lot more about Python before I can create any real code.

The eventual intent will be to implement an general purpose object store that can be used for storing binary data indexed by the double SHA-256 digest of the data. The must include the ability to serialize and deserialize the data to and from files.

In memory, such an object would have a data field and a digest field. The digest field would not be present in the on-disk version, but would be implicit in the file name. For now, the files will be named like the objects in Git based on their digest.

There would also be a class-level string with the name of the subfolder in which all objects are stored. <object folder>

field and methods like:

  serialize():
    - generate the digest if it is not already in object
    - Sprit the digest into a subfolder name and filename, using the first 2 bytes as the subfolder name, and the remaining bytes as the file name.
    - Create <object folder>/<subfolder> if it doesn't exist.
    - in the subfolder, open a binary file for write with the file name.
    - write the contents of the data field to the file, and close it when done.
  deserialize()
    - from the hash, generate the object subfolder and the object's file name.
    - if the folder or the file don't exist - fail (for now)
    - Open the file for read as a binary file
    - Read the contents into the data field.
  setData(input_data)
    - Copy the binary input_data into the data field.
  generateDigest()
    - create the digest for the data and store in digest.
  getSubFolder()
    - generate the digest if it's not there.
    - as the folder name, use the first 2 bytes of the digest
    - return <object folder>/<folder name>
  getFilename()
    - generate the digest if it's not there
    - return [1:] of the digest as the file name.

It's not clear to me at this point how to do the instance creations. It's necessary to be able to create and empty instance when creating a brand new object, as well as to create an instance based on an object already in the file system.

There also needs to be a hash map (use the appropriate python term) that is created in memory to map digests to the binary objects. Not sure if the values should be the instance of the object class or to just the data. Probably to the instance this requiring 2 dereferences to get the actual data given the hash.
