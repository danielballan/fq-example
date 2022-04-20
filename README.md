# Specialized CSV variants

Tiled's directory server has built-in support for several common formats
including CSV, Excel, HDF5, TIFF, and some others. For those, this just works:

```
tiled serve directory my_data/
```

If you have file types it doesn't know about, you can configure it by using
a configuration file. This is equivalent to the above:

```yaml
# config.yml
trees:
- path: /
  tree: files
  args:
    directory: my_data/
```

```
tiled serve config config.yml
```

Now we can extend `config.yml` to customize.

When Tiled finds a `.csv` file, it uses `pandas.read_csv` to read it.
If you have CSVs with a different extension `.xyz` whose contents are
essentially CSV files, you can teach tiled to treat those files like CSV files
like so. This says ".xyz is just a CSV file by another name".

```yaml
# config.yml
trees:
- path: /
  tree: files
  args:
    directory: my_data/
    mimetypes_by_file_ext:
      .xyz: text/csv
```

But if you have files that can't be read by `pandas.read_csv` out of the box,
you need to define a custom reader and then tell tiled above that reader.

```yaml
# config.yml
trees:
- path: /
  tree: files
  args:
    directory: my_data/
    # Teach Tiled about .fq files.
    mimetypes_by_file_ext:
      .fq: application/x-fq
    readers_by_mimetype:
      application/x-fq: custom_readers:read_fq
```

This tells Tiled:

* `.fq` files are file type you haven't heard of that we'll refer to as `application/x-fq`.
* When you find `application/x-fq` files, use the function `read_fq` in the module
  `custom_readers.py` to read them.

