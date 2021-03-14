本工程可以输入C文件中的控制结构根据提示输出成SVG格式的文件图片，此文件可供Visio等软件进一步编辑使用

## Requirements
使用此工程需要安装如下软件
1. Python 3.x, 测试使用python 3.6
2. dot: Windows下安装Graphviz即可（http://www.graphviz.org/）， 并确保安装目录的bin文件在系统Path路径下


## Usage
在当前工程源代码根目录下，运行如下命令：
```
    python .\cmt_parser.py c_source_file out_file
```

如下示例：
```
    python .\cmt_parser.py .\examples\testFunc.c testFunc
```

## Notice
1. 当前工程并不能直接生成visio文件，而是生成svg格式文件，但此svg格式文件可以直接导入到visio中编辑并使用
2. 程序控制结构提示：当前可以使用的控制结构提示符格式如下: <br>
```c
// #cond ""
// #action ""
```
使用时请注意不要忽略""， 使用事例如下：
```c
    // #cond "a > 0"
    if(a > 0) {
        // #action "do something"
    } else {
        // #action "do others"
    }
```


## Others
1. 当前不支持`else if`结构的写法，需要使用`else { if }`的形式来替换，如下示例：
```c
    if(a > 5) {
        ...
    } else {
        if(a < 3) {     // 此外不可以使用 else if(a < 3) {}
            ...
        } else {
            if (a == 1) {   // 此外不可使用 else if(a == 1) {}

            }
        }
    }

```
2. `switch`语句的条件约束提示需要放在swithc语句之前，不可包含在`switch`语句块内，即如下形式：
```
        // #cond "deal with a"
        switch(a) {
            case 1:
            case 2:
                // #action "do a == 1/2"
                break;
```
不可以写成不下形式：

```
        switch(a) {
            // #cond "deal with a, 错误形式，不能正确生成控制结构"
            case 1:
            case 2:
                // #action "do a == 1/2"
                break;

```