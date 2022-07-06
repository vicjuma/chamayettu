import time

def windows_diagnostics():
  print("Looking for problems")
  time.sleep(20)
  print("Unable to fix the issue")

while(
  bool(
    input(
      "Do you want to try other windows version configurations? 1 or 0"))):
  windows_diagnostics()