
import timeit

class CallTime:
    '''
    Description:

        Simple timer class.
        Time function calls and saves to CSV file.

    Usage:

        func = CallTime.Test
        args = (1, 2, 3)
        CallTime.Measure_Single( func, args, args )

        or

        func = Test # any valid function name ...
        args = (1, 2, 3)

        obj_ct = CallTime(func)
        obj_ct.Measure( args, args )
        obj_ct.Measure( args, None )
        obj_ct.Save_Append( "ct-test.txt" )

    '''

    def __init__(self, func):
        self.func = func
        self.Entries = []

    def Measure(self, args, avs):

        # Start timer
        time_start = timeit.default_timer()

        # Run function
        self.func(*args)

        # End timer
        time_end = timeit.default_timer()

        # Save run
        self.Entries.append([self.func.__name__, time_end - time_start, avs])

    def Save_Append(self, filename):

        # Open file for appending text
        # Write each entry
        with open(filename, "a") as FileObject:
            for entry in self.Entries:

                str_func = entry[0]
                str_time = str(entry[1])
                str_avs = ""

                if not entry[2] is None:
                    for av in entry[2]:
                        str_avs += ", " + str(av)

                FileObject.write( str_func + ", " + str_time + str_avs + "\n" )

    @staticmethod
    def Measure_Single( func, args, avs):

        # Start timer
        time_start = timeit.default_timer()

        # Run function
        func(*args)

        # End timer
        time_end = timeit.default_timer()

        # Build report string
        print_str = func.__name__ + ", " + str(time_end - time_start)

        if not avs is None:
            for av in avs:
                print_str += ", " + str(av)

        # Report to console
        print( print_str )
