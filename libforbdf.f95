
subroutine read_channels(filename, starttime, endtime, nChannels, nSampRec, statusChanIdx, dats, statchan)
  implicit none
  character(256), intent(in) :: filename
  integer   :: ch, k, m, openerror, startpos, cpos, nChan, nRec, mypos, iofuz
  integer*4 :: bitstr, bitstr1, bitstr2, bitstr3, int32
  !integer*2 :: int16
  character :: datchar(0:(nChannels*nSampRec*3*(endtime-starttime))-1)
  character :: onechar
  character*2 :: twochar
  character*3 :: threechar
  integer, intent (in) :: endtime, starttime, nChannels, nSampRec, statusChanIdx
  integer, intent(out) :: dats(0:(nChannels-2), 0:(nSampRec*(endtime-starttime))-1)
  integer*4, intent(out) :: statchan(0:1, 0:(nSampRec*(endtime-starttime))-1)

  
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
  twochar = onechar//onechar
  threechar = twochar//onechar
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
           bitstr1 = TRANSFER(SOURCE=twochar//datchar(cpos)//datchar(cpos+1), MOLD=int32)
           bitstr1 = RSHIFT(bitstr1, 16)
           bitstr2 = TRANSFER(SOURCE=threechar//datchar(cpos+2), MOLD=int32)
           bitstr2 = RSHIFT(bitstr2, 24)
           statchan(0, (k*nSampRec)+m) = bitstr1+256
           statchan(1, (k*nSampRec)+m) = bitstr2+256
           cpos = cpos+3
        end do
     end if
  end do
end do
  
end subroutine read_channels


