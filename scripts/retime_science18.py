"""Retime optogenetics narration and captions using the shared episode utility."""
from pathlib import Path
import retime_science17 as shared
shared.EP=Path(__file__).resolve().parents[1]/'episodes/science18_optogenetics'
if __name__=='__main__':
 shared.main()

