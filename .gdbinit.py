import gdb
import sys

class StackFold(gdb.Command):
    def __init__(self):
        super(StackFold, self).__init__("stackfold", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        # An inferior is the 'currently running applications'. In this case we only
        # have one.
        stack_maps = {}
        # This creates a dict where each element is keyed by backtrace.
        # Then each backtrace contains an array of "frames"
        #
        inferiors = gdb.inferiors()
        for inferior in inferiors:
            for thread in inferior.threads():
                try:
                    # Change to our threads context
                    thread.switch()
                    # Get the thread IDS
                    (tpid, lwpid, tid) = thread.ptid
                    gtid = thread.num
                    # Take a human readable copy of the backtrace, we'll need this for display later.
                    o = gdb.execute('bt', to_string=True)
                    # Build the backtrace for comparison
                    backtrace = []
                    gdb.newest_frame()
                    cur_frame = gdb.selected_frame()
                    while cur_frame is not None:
                        if cur_frame.name() is not None:
                            backtrace.append(cur_frame.name())

                        cur_frame = cur_frame.older()
                    # Now we have a backtrace like ['pthread_cond_wait@@GLIBC_2.3.2', 'lazy_thread', 'start_thread', 'clone']
                    # dicts can't use lists as keys because they are non-hashable, so we turn this into a string.
                    # Remember, C functions can't have spaces in them ...
                    s_backtrace = ' '.join(backtrace)
                    # Let's see if it exists in the stack_maps
                    if s_backtrace not in stack_maps:
                        stack_maps[s_backtrace] = []
                    # Now lets add this thread to the map.
                    stack_maps[s_backtrace].append({'gtid': gtid, 'tpid': tpid, 'bt': o})
                except Exception as e:
                    print(e)
        # Now at this point we have a dict of traces, and each trace has a "list" of pids that match. Let's display them
        for smap in stack_maps:
            # Get our human readable form out.
            o = stack_maps[smap][0]['bt']
            for t in stack_maps[smap]:
                # For each thread we recorded
                print("Thread %s (LWP %s))" % (t['gtid'], t['tpid']))
            print(o)


# This registers our class to the gdb runtime at "source" time.
StackFold()
