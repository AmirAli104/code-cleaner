# code-cleaner

Maybe you have experienced that sometimes you copy a code from somewhere to paste it in your computer and run it. But in some websites they have placed the line numbers in such a way that when you copy the code the line numbers are also copied. You can remove these with this program.

You can also remove python shell prompts (`>>>` and `...`) from python codes.

command-line options
---

|option|description|
|------|------|
|`-n,--line`|files/directories to clear line numbers|
|`-s,--shell`|files/directories to clear shell prompt characters|
|`-d,--directory`|Consider the values given to '--shell' and '--line' as directories. You must give the file extentions you want to clean them to this argument. Its default is '.py' files.|
|`-t,--tree`|If the both '--directory' and '--tree' are enabled it searches all subdirectories to find files|
|`-l,--log`|enable logging|

Examples
---

```
python code-cleaner.py -s a.py b.py -n a.c
```

The above command cleans the line numbers from `a.c` and the shell prompt characters from `a.py`.


```
python code-cleaner.py -n codes_directory -d .c .py -t -l
```

The above command cleares the line numbers from the `.c` and `.py` files in the given directory and also shows the log. Because of the `-t` argument it checks all subdirectories.
