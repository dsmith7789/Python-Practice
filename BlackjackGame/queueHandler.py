"""This module holds the QueueHandler class, which enqueues log records instead
of directly logging them.
"""

import logging
import queue

class QueueHandler(logging.Handler):
    """Enqueues log records instead of directly logging them.

    Args:
        log_queue (queue.Queue): The queue that log records will be placed in.
    """
    def __init__(self, log_queue: queue.Queue) -> None:
        """Set up the QueueHandler to point to a queue to hold messages.

        Args:
            log_queue (queue.Queue): The queue that log records will be placed in.
        """
        super().__init__()
        self.log_queue = log_queue
    
    def emit(self, record):
        self.log_queue.put(record)