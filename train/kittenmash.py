#! /usr/bin/env python

"""
Kitten Trainer
Trains the kittens that walk on the keyboard.
"""

from config import config
from recorder import Recorder
from trainer import Trainer

import atexit, os, time, sys, json
from threading import Thread, Lock
from optparse import OptionParser

options = None

def record(*args):
  """
  records a kitten walking on the keyboard and outputs it into specified file
  """
  recorder = Recorder(options.output)
  recorder.start()

def train(*args):
  """
  trains the model based on files in the input folder
  """
  input_folder = args[0][0]
  if not input_folder:
    print "Must specify a directory of models"
    return

  trainer = Trainer(input_folder, options.output)
  trainer.train()


def convert(*args):
  """
  converts the trained model to a jQuery readable format (json)
  """
  pass

def create_cli_parser():
  usage = (
    "%prog method [options]",
    __doc__,
    """Arguments: METHOD: (record | train | convert)"""
  )

  usage = "\n".join(usage)

  cli_parser = OptionParser(usage)

  # Add the CLI options
  cli_parser.add_option('-v', '--verbose', action='store_true',
    help="print the weather section headers",
    default=False
  )

  cli_parser.add_option('-o', '--output', action='store',
    help="output results to a specified file name",
    default="output"
  )

  return cli_parser

def main(argv):
  global options

  cli_parser = create_cli_parser()
  options, args = cli_parser.parse_args(argv)

  # Check that an argument was passed.
  if len(args) < 1:
    cli_parser.error("Not enough arguments supplied.")

  method = args[0]

  if method in globals():
    globals()[method](args[1:])
  else:
    cli_parser.error("Method %s does not exist" % method)

if __name__ == "__main__":
    main(sys.argv[1:])

@atexit.register
def goodbye():
   print "Kittenmash says goodbye."
