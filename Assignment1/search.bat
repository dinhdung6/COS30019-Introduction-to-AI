@echo off
setlocal enabledelayedexpansion

set "search_methods=DFS BFS GBFS AS CUS1 CUS2"
set "test_files=test1.txt test2.txt test3.txt test4.txt test5.txt test6.txt test7.txt test8.txt test9.txt test10.txt"

for %%f in (%test_files%) do (
    for %%m in (%search_methods%) do (
        echo Running %%f with %%m
        python search.py %%f %%m
    )
)

endlocal
pause
