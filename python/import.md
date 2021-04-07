[返回目录](../README.md)
# Python Import

## Two related-imports
* from ..XXX import XXX: 拉取上一路径下的package or file
* from ...XXX import XXX: 拉取上上个路径下的package or file

## Error due to import
* ValueError: attempted relative import beyond top-level package:
**python 不会记录加载package的路径**
  
From: https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
