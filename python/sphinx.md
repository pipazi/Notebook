[返回目录](../README.md)
# sphinx

1.execute blew command:
```bash
sphinx-quickstart
```

2. during quickstart set language to "zh_CN"

3. add blew to extensions
```
sphinx.ext.napoleon
```

4. sphinx-apidoc -f -o ./source ../ubd

5. tar -czvf test.tar.gz build/