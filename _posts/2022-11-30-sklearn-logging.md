---
title:  "How to Log, with Scikit-Learn"
tags: [machine-learning,python,dask,logging]
---

I recently dug deep in to logging and scikit-learn. It lead to a [SO question](https://stackoverflow.com/questions/74631614/catch-sklearn-joblib-output-to-python-logging), and a few hours later, noone but me has attempted a solution. I thought I would add more motivational text and explain my reasoning here. 

## Motivation - and the catch

I really like the python standard library [`logging`](https://docs.python.org/3/library/logging.html) module. You can use it to decorate your output with useful things such as timestamps, the name of the logging function name and so on. While being quite rudimentary, it is always available and has the most important functions included.

Another thing I really like is `scikit-learn`. You have easy access to many standard machine learning algorithms and simple APIs for boring-to-implement stuff such as hyperparameter tuning, feature engineering and so on. It even parallellizes many algorithms with a simple `n_jobs` parameter. See, for example, [sklearn.model_selection.GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) and [sklearn.ensemble.RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html). Whenever scikit-learn reports training progress (by setting the `verbose` parameter in suitable models) it uses the  standard output and standard error streams. It does not use the python `logging` module!

## Redefining the output streams

Python is a fun and strange language. Just about anything can be monkey patched! So a "standard" thing to do is to redefine the stdin and stdout streams to a custom object, intercepting all print statements.

```python
import sys
import logging

class LogAdapter:
    def __init__(self,logger):
        self.logger = logger
    def write(self,msg):
        self.logger.info(msg)
    def flush(self):
        pass

print("Hello")
logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)])
sys.stdout = LogAdapter(logging.getLogger("\"stdout\""))
sys.stderr = LogAdapter(logging.getLogger("\"stderr\""))
print("world")
```
The logging config must be defined before we patch `stdout` reference in `sys`, otherwise we get infinite recursion as `LogAdapter` calls logging, which would call `sys.stdout`, which calls `LogAdapter` infinitely. 

This solution is well known and you find references to it all over the internet. There are also variants where you redirect `stdout` and `stderr` to a open file.

## Context management solves the restoration issues

Great, all output goes via logging. But what if that breaks some other code you did not think about? You should set up a context manager, which restore the patch when the important code is done.

```python
import contextlib 
import sys
import logging

class LogAdapter:
    def __init__(self,logger):
        self.logger = logger
    def write(self,msg):
        self.logger.info(msg)
    def flush(self):
        pass

@contextlib.contextmanager
def redirect_to_log(logger):
    originals = sys.stdout, sys.stderr
    sys.stdout = LogAdapter(logging.getLogger("\"stdout\""))
    sys.stderr = LogAdapter(logging.getLogger("\"stderr\""))
    yield
    sys.stdout, sys.stderr = originals
```

## Using the context manager for logging, and its limitations

We are in the position to try the code out. A naïve application of the above context manager *will* work for parallellization via threading. 

```python
import contextlib 
import sys
import logging

class LogAdapter:
    def __init__(self,logger):
        self.logger = logger
    def write(self,msg):
        self.logger.info(msg)
    def flush(self):
        pass

@contextlib.contextmanager
def redirect_to_log():
    originals = sys.stdout, sys.stderr
    sys.stdout = LogAdapter(logging.getLogger("\"stdout\""))
    sys.stderr = LogAdapter(logging.getLogger("\"stderr\""))
    yield
    sys.stdout, sys.stderr = originals

if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.utils import parallel_backend

    logging.basicConfig()
    with parallel_backend('threading'),redirect_to_log():
        clf = RandomForestClassifier(2, verbose=4)
        X = [[0, 0], [1, 1]]
        Y = [0, 1]
        clf = clf.fit(X, Y)
```

Unfortunately, changing the backend from `threading` to `loky` or `multiprocessing` will just about almost work. All output to `stdout` and `stderr` is redirected as it should. But it fails in one way. All subprocesses spawned will **not** have the stdout and stderr redefined. 
A worker process will be spawned, and some task in terms of machine learning is sent to the child process for processing. The child process does has its own I/O streams, and the context manager does not automatically apply to the spawned child processes. So what now?

## Proper logging is possible via the dask backend

To do patch I/O in worker processes we must send some extra tasks to the workers, so they apply the context manager logic. I did not understand how to do this with `loky`, and [one issue on github](https://github.com/joblib/joblib/issues/1017) claims that the joblib interface sits in the way of doing this for `loky`. So I turn to the `dask` backend. One must 

1. Install the `dask` library
1. Define a `WorkerPlugin`. The WorkerPlugin must make sure to initialize the logging for the worker so it logs in an appropriate way (probably indentically with the parent process).
1. Initialize a dask `Client`
1. Register the plugin with the `Client`
1. Ask `joblib` to use the `dask` backend

We still need the context manager to capture all output from joblib and scikit-learn in the main process, so that code stays.

```python
import contextlib 
import sys
import logging
import dask.distributed

class LogAdapter:
    def __init__(self,logger):
        self.logger = logger
    def write(self,msg):
        self.logger.info(msg)
    def flush(self):
        pass

@contextlib.contextmanager
def redirect_to_log():
    originals = sys.stdout, sys.stderr
    sys.stdout = LogAdapter(logging.getLogger("\"stdout\""))
    sys.stderr = LogAdapter(logging.getLogger("\"stderr\""))
    yield
    sys.stdout, sys.stderr = originals

class LogPlugin(dask.distributed.WorkerPlugin):
    def __init__(self,init_logging: Callable) -> None:
        self.init_logging = init_logging

    def setup(self, worker: dask.distributed.Worker):
        self.originals = sys.stdout, sys.stderr
        self.init_logging()
        sys.stdout = LogAdapter(logging.getLogger("\"stdout\""))
        sys.stderr = LogAdapter(logging.getLogger("\"stderr\""))

    def teardown(self, worker: dask.distributed.Worker):
        sys.stdout, sys.stderr = self.originals

if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.utils import parallel_backend
    def init_logging():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(process)6d | %(asctime)s | %(name)14s | %(levelname)7s | %(message)s",
        )

    client = dask.distributed.Client()
    client.register_worker_plugin(LogPlugin(init_logging))
    logging.basicConfig()
    with parallel_backend('dask'),redirect_to_log():
        clf = RandomForestClassifier(2, verbose=4)
        X = [[0, 0], [1, 1]]
        Y = [0, 1]
        clf = clf.fit(X, Y)
```