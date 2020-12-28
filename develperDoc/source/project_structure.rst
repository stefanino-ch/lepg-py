.. lepg_proj_struc

Project structure
=================

.. toctree::
   :maxdepth: 2
   
.. highlight:: none

The project structure is build as shown below::

  developerDoc          -> All files needed to build the developer doc you're looking currently at;-)
  
  importTestFiles       -> Test files for development. Some are fully compliant to spec.
                           Others do have errors to check the error handling.
  
  installer             -> pyinstaller files
  
  src                   -> the project sources. 
  
  userHelp              -> All files needed to build the html help files displayed from lepg
  |- _build             -> Herein the complete help files will be generated
  |- _static		
  |- _templates         -> Specific template files used by Sphinx
  |- _themes            -> The theme is defining the look and feel of the user help
  |- de                 -> The original text of all help files in german
     |- preproc         -> All files to create the pre-processor doc in german
     |- deutsch.rst     -> Provides the german toc for the user doc
  |- en                 -> The original text of all help files in german
     |- preproc         -> All files to create the pre-processor doc in englis
     |- english.rst     -> Provides the english toc for the user doc
  |- buildUserHelp.bat  -> Little helper doing all the repetive stuff to create, copy, ... the help files to the final location
  |- conf.py            -> Sphinx config file
  |- contents.rst       
  |- index.rst
  |- make.bat           -> see Sphinx doc
  |- Makefile           -> see Sphinx doc

