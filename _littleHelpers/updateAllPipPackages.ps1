# Updates all outdated packages managed by pip
# Thanks to https://www.activestate.com/resources/quick-reads/how-to-update-all-python-packages/

pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
