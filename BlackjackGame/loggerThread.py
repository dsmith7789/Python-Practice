""" This module contains the LoggerThread class, which continuously monitors
a queue for log records and processes them using a handler, to actually write
the log records to a destination ("game.log").
"""

import threading
import logging
import queue

class LoggerThread(threading.Thread):
    """The LoggerThread continuously monitors a queue for log records and writes 
    them to the destination.
    """
    def __init__(self, log_queue: queue.Queue, formatter: logging.Formatter) -> None:
        """Set up the LoggerThread to monitor the specified queue for log records.

        Args:
            log_queue (queue.Queue): The queue the LoggerThread will watch for log records.
            formatter (logging.Formatter): The formatter used to write the log messages.
        """
        super().__init__(daemon=True)
        self.log_queue = log_queue
        self.handler = logging.FileHandler("game.log")
        self.handler.setFormatter(formatter)
        self.running = True
    
    def run(self):
        while self.running:
            try:
                record = self.log_queue.get(timeout=1)
                self.handler.emit(record)
            except queue.Empty:
                continue
    
    def stop(self):
        self.running = False