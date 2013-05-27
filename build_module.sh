 


#f2py3.2 -m libforbdf -c --fcompiler='gfortran' --f90flags=-ffixed-line-length-none libforbdf.f95  #--verbose


f2py3.2 -m libforbdf -c --fcompiler='gnu95' --f90flags=-ffixed-line-length-none libforbdf.f95 
#f2py3.2 -m libforbdf2 -c --fcompiler='gnu95' --f90flags=-ffixed-line-length-none libforbdf2.f95 
#f2py -h libforbdf.pyf -m libforbdf libforbdf.f95 --verbose --overwrite-signature