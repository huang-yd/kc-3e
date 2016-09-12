set obj=createobject("wscript.shell")
do
    flag=obj.popup("click [yes] to run update.bat, [no] to do nothing, [cancel] to quit this script.",30,"autoRun",vbyesnocancel)
    if flag=6 or flag=-1 then
    	obj.run "update.bat"
    end if
    if flag=2 then
    	wscript.quit
    end if
    wscript.sleep 259200000
loop