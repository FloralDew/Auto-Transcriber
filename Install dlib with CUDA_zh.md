本教程提供windows安装方法

### 设置vs版本(2022仅能编译cuda>12.4. 此电脑为cuda12.1, 需要2019)

```cmd
set CMAKE_GENERATOR=Visual Studio 16 2019
```

环境变量. 如果之前使用2022编译过, 需要使用`python setup.py clean`清空缓存

### 为vs2019装载CUDA toolset

把

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\extras\visual_studio_integration\MSBuildExtensions

之中的所有文件复制到

<vs路径>\MSBuild\Microsoft\VC\v160\BuildCustomizations\

### 提高MSVC编译器内存限制

本步骤解决报错

```markdown
fatal error C1060: compiler is out of heap space
```

```cmd
set CL=/bigobj /Zm300
```

- `/bigobj` → 允许更多 section

- `/Zm300` → 增加编译器堆(默认 100)

### 新版CUDNN目录结构变了, 需要保留原来的结构

- 将 include\12.9\\* 复制到 include\
- 将 lib\12.9\x64\\* 复制到 lib\x64\
- 将 bin\12.9\\* 复制到 bin\

### 判断是否成功

```python
import dlib
print(dlib.DLIB_USE_CUDA)
```

True则为成功