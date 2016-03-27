import logging
import queue
import threading

from blocks import Block, BlockFactory
from blockchain import BlockChain

class ProcessContent(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        # Call parent's __init__
        super().__init__(group=group, target=target, name=name)

        # Save the thread name and keyword arguments
        self.name = name
        self.content_queue = kwargs['content_queue']
        self.block_queue = kwargs['block_queue']
        self.block_chain = kwargs['blockchain']
        self.factory = BlockFactory()

    def run(self):
        logging.debug('ProcessContent thread starting')

        while True:
            msg = self.content_queue.get()
            if msg is None:
                self.block_queue.put(None)
                break
            logging.debug(msg)

            # Generate and farm a block from the content
            block = self.factory.createNew(msg)
            pbhd = self.block_chain.getLastBlockDigest()
            hd = block.farm(pbhd)

            # Return the the block as raw bytes
            self.block_queue.put(block.toBytes())

            self.content_queue.task_done()

        logging.debug('ProcessContent thread ending')
