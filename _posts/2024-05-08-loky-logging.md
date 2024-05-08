---
title:  "Standard Python Logging with the Joblib Loky Backend"
tags: [python,logging,loky, multiprocessing]
---

The main issue with python logging and joblib multiprocessing is that the loky backend on joblib does not offer a way to set up the worker processes where the loggers can be set up. While your code might call a logger, the log record just goes into a black hole, and you will not see any output.

The issue has beed discussed on [github](https://github.com/joblib/joblib/issues/1017) and there are also generic solutions to python multiprocessing in the [logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html) that can be used. I also commented on that in [a previous post](/2022/11/30/sklearn-logging) how to use Dask when using the joblib to enable logging of scikit-learn.

This time, I don't use scikit-learn, and I really don't want to use Dask, so I have to make do with joblib.

The solution is to set up a logger with a handler in the worker process. The handler just places the log records on a queue. 
The main process runs a queue listener, that dispatches the log records to a different handler that prints to std out using some formatter.
The simplest way (to me) to create that main process handler and formatter is via the root logger.

You may also watch this [video by mCoding](https://www.youtube.com/watch?v=9L77QExPmI0) on modern python logging. It provides some background on how python logging works with loggers, handlers and formatters.


```python
import logging
import joblib
import logging.handlers
import multiprocessing

def f(x,queue):
    """
    setting up the logger in the work function like this is not perfect. the call `getLogger` will find the 
    process-unique instance of the logger, and reuse it. so we cannot configure the logger in the main 
    process every time since, for exampe, it might get multiple handlers cloning every log message again and 
    again. the simplest workaround is to check if there are any handlers on the logger, indicating set up
    """
    logger_ = logging.getLogger(__name__)
    if not logger_.hasHandlers():
        logger_.setLevel(logging.DEBUG)
        handler = logging.handlers.QueueHandler(queue)
        logger_.addHandler(handler)
        
    out = x * x
    logger_.debug(f"f({x})={out}")
    return out

def main():
    # configure some logger to make sure output is observable
    logging.basicConfig(level=logging.DEBUG, format="%(processName)s %(levelname)s %(message)s") 

    # one must use Manager().Queue() to pass as argument in loky backend, multiprocessing.Queue() will not work
    # https://stackoverflow.com/questions/3217002/how-do-you-pass-a-queue-reference-to-a-function-managed-by-pool-map-async
    queue = multiprocessing.Manager().Queue(-1) 
    listener = logging.handlers.QueueListener(queue, *logging.getLogger().handlers) 
    listener.start()

    joblib.Parallel(n_jobs=2,backend='loky')(joblib.delayed(f)(i,queue) for i in range(10))
    
    # if you don't stop the listener, the program might crash and you might have unprocessed log records
    listener.stop() 

if __name__ == "__main__":
    main()
```
