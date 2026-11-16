"""Accept valid DVI output when MiKTeX crashes only while closing its denied log."""
import re
import manim.utils.tex_file_writing as tex
_original=tex.compile_tex

def compile_checked(tex_file,tex_compiler,output_format):
 try:return _original(tex_file,tex_compiler,output_format)
 except ValueError:
  result=tex_file.with_suffix(output_format);log=tex_file.with_suffix('.log')
  report=log.read_text(encoding='utf-8',errors='replace') if log.exists() else ''
  valid=result.exists() and result.stat().st_size>100 and output_format=='.dvi'
  if valid and 'Output written on ' in report and not re.search(r'^!',report,re.M):
   raw=result.read_bytes()
   if raw[0]==247 and raw[-4:]==bytes([223])*4:return result
  raise
tex.compile_tex=compile_checked
