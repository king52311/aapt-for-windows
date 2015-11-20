@echo off
set scan_dir=%cd%
set base_dir=%scan_dir%\
set apk_ext=.apk

set channel_dir=META-INF
set work_path=%base_dir%%channel_dir%
set channel_list=%base_dir%channel_list
set out_dir=out\

REM 查找原APK文件
call :FIND_APK %scan_dir%\src
set dst_apk=%src_apk%
set full_dst_apk=%base_dir%%dst_apk%
REM 拷贝原APK
@echo 正在拷贝原APK...
REM 遍历渠道目录
@echo 正在查找渠道文件...
	call :CREATE_INF %channel_list% %work_path%
@echo 正在生成渠道文件...
for /f "delims=" %%b in ('dir /b/a-d/oN %work_path%')  do ( 
copy /y  %src_apk% %full_dst_apk%
echo %channel_dir%\%%b
@echo 正在打包文件...
aapt a %dst_apk% %channel_dir%\%%b
	call :MOVE_FILE %full_dst_apk% %out_dir%%src_apk_name%_%%b%apk_ext%
@echo 正在清理临时文件...
	call :DEL_FILE %base_dir%%channel_dir%\%%b
) 
@echo 打包完成...
exit




:FIND_APK

for /f "delims=" %%c in ('dir /b/a-d/oN %1\*.apk')  do ( 
	set src_apk_name=%%~nc
	set src_apk=%%c
)
GOTO :EOF


:CREATE_INF
for /f "delims=" %%f in (%1)  do (
	echo %%f > %2\%%f
) 
GOTO :EOF

:MOVE_FILE
if exist "%1" (
       move /y %1 %2
) else (
    echo %1 does not exist!
)
GOTO :EOF


:DEL_FILE
if exist "%1" (
        del %1
) else (
    echo %1 does not exist!
)
GOTO :EOF


:COPY_FILE
if exist "%1" (
        copy /y  %1 %2
) else (
    echo %1 does not exist!
)
GOTO :EOF