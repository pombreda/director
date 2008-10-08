Examples
=========

Example 'Binary'
----------------
::

   #!/usr/bin/env python

   import exceptions
   import sys

   from director import ActionRunner
   from director.filter import ExceptionFilter
   from director.filter import Filter


   if __name__ == '__main__':
       # Create and use exception filters
       # Note you don't have to use filters. If you don't pass filter in
       # to ActionRunner.run filters won't be used.
       filter = Filter()
       filter.register_filter(ExceptionFilter(exceptions.IOError, "TEST %s"))
       filter.register_filter(ExceptionFilter(exceptions.TypeError, "NO! %s"))

       # 'actions.package' is the package that holds the allowed plugin actions
       ar = ActionRunner(sys.argv, 'actions.package')
       ar.run(filter)


Example 'Action'
----------------
::

   from director import Action
   from director import decorators


   class Bucket(Action):
       """
       Thor bucket action.
       """

       description_txt = "Managers buckets"

       @decorators.help("\nOptions:\n\tNone")
       def list(self):
           """
           Prints all buckets.
           """
           pass

       @decorators.help("\nOptions:\tadd:\tName of the bucket to add")
       def add(self, name):
           """
           Adds a new bucket.
           """
           print name

       @decorators.help("\nOptions:\tname:\tName of the bucket to delete")
       def delete(self, name):
           """
           Deletes a bucket.
           """
           pass


Defining Help Text
------------------
As you can see above, help text defined via a decorator in the decorators module called help. You can put whatever formatted string you want ...
just make sure to be consistent for the sake of the user!


Calling Actions
---------------
The format is :command:`application action verb --option=val --anotheroption=val2`.... For example ...
::

   $ myteam roster list --filter=steve
   Steve Milner
   Steven Carzy
   Steven "BigDawg" Salezkuy
   $ myteam roster list --filter=steve --lastname=milner
   Steve Milner
   $
