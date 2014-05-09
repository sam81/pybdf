
subroutine read_channels(filename, starttime, endtime, nChannels, nSampRec, statusChanIdx, dats, statchan)
  implicit none
  character(256), intent(in) :: filename
  integer   :: ch, k, m, openerror, startpos, cpos, nChan, nRec
  integer*4 :: bitstr, bitstr1, bitstr2, bitstr3, int32
  integer*2 :: int16
  character :: datchar(0:(nChannels*nSampRec*3*(endtime-starttime))-1)
  character :: onechar
  integer, intent (in) :: endtime, starttime, nChannels, nSampRec, statusChanIdx
  integer, intent(out) :: dats(0:(nChannels-2), 0:(nSampRec*(endtime-starttime))-1)
  integer*2, intent(out) :: statchan(0:2, 0:(nSampRec*(endtime-starttime))-1)

  
  Open(Unit=10,Form='unformatted', File=filename, action ='read', &
       Status='OLD',iostat=openerror, access='stream')
  
  if (openerror /= 0) STOP "***Error opening file***"
  
  !!skip header and jump to starttime
  nRec = endtime - starttime
  startpos = (nChannels+1)*256 + starttime*nSampRec*3*nChannels

  CALL FSEEK(UNIT=10, OFFSET=startpos, WHENCE=1)  ! move to OFFSET
  read(unit=10) datchar
  close(unit=10)
  onechar = CHAR(0)

  cpos = 0
  do k=0,(nRec-1)
     do ch=0,(nChannels-1)
        if (ch .NE. statusChanIdx) then
           do m=0,(nSampRec-1)
              bitstr1 = TRANSFER(SOURCE=onechar//datchar(cpos)//datchar(cpos+1)//datchar(cpos+2), MOLD=int32)
              bitstr = RSHIFT(bitstr1, 8)
              dats(ch, (k*nSampRec)+m) = bitstr 
              cpos = cpos+3
           end do
        else
           do m=0,(nSampRec-1)
              bitstr1 = TRANSFER(SOURCE=datchar(cpos)//onechar, MOLD=int16)
              bitstr2 = TRANSFER(SOURCE=datchar(cpos+1)//onechar, MOLD=int16)
              bitstr3 = TRANSFER(SOURCE=datchar(cpos+2)//onechar, MOLD=int16)
              statchan(0, (k*nSampRec)+m) = bitstr1
              statchan(1, (k*nSampRec)+m) = bitstr2
              statchan(2, (k*nSampRec)+m) = bitstr3
              cpos = cpos+3
        end do
     end if
  end do
end do
  
end subroutine read_channels


