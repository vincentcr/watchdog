#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:module: watchdog.observers
:synopsis: Observer that picks a native implementation if available.
:author: yesudeep@google.com (Yesudeep Mangalapilly)


Classes
=======
.. autoclass:: Observer
   :members:
   :show-inheritance:
   :inherited-members:

You can also import platform specific classes directly and use it instead
of :class:`Observer`.  Here is a list of implemented observer classes.:

============== ================================ ==============================
Class          Platforms                        Note
============== ================================ ==============================
|Inotify|      Linux 2.6.13+                    ``inotify(7)`` based observer
|FSEvents|     Mac OS X                         FSEvents based observer
|Kqueue|       Mac OS X and BSD with kqueue(2)  ``kqueue(2)`` based observer
|WinApi|       MS Windows                       Windows API-based observer
|Polling|      Any                              fallback implementation
============== ================================ ==============================

.. |Inotify|     replace:: :class:`.inotify.InotifyObserver`
.. |FSEvents|    replace:: :class:`.fsevents.FSEventsObserver`
.. |Kqueue|      replace:: :class:`.kqueue.KqueueObserver`
.. |WinApi|      replace:: :class:`.read_directory_changes.WindowsApiObserver`
.. |WinApiAsync| replace:: :class:`.read_directory_changes_async.WindowsApiAsyncObserver`
.. |Polling|     replace:: :class:`.polling.PollingObserver`

"""

from watchdog.observers.api import BaseObserver, DEFAULT_OBSERVER_TIMEOUT

# Ensure FSEvents is checked *before* kqueue here. Mac OS X supports
# both FSEvents and kqueue, and FSEvents is the preferred way of monitoring
# file system events on this OS.
try: # pragma: no cover
  from watchdog.observers.inotify import InotifyObserver as _Observer
except ImportError: # pragma: no cover
  try: # pragma: no cover
    from watchdog.observers.fsevents import FSEventsObserver as _Observer
  except ImportError: # pragma: no cover
    try: # pragma: no cover
      from watchdog.observers.kqueue import KqueueObserver as _Observer
    except ImportError: # pragma: no cover
      try: # pragma: no cover
        from watchdog.observers.read_directory_changes_async import WindowsApiAsyncObserver as _Observer
      except ImportError: # pragma: no cover
        try: # pragma: no cover
          from watchdog.observers.read_directory_changes import WindowsApiObserver as _Observer
        except (ImportError, AttributeError): # pragma: no cover
          from watchdog.observers.polling import PollingObserver as _Observer


Observer = _Observer
"""
Observer thread that schedules watching directories and dispatches
calls to event handlers.
"""
