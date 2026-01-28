# `[visual]` Configuration

## `clean_description`

> Default: `false`

Controls whether project (`+`) and context (`@`) tags are stripped from the task description when displayed.

### When to use: `false`

If you use tags inline as part of your sentence structure, you should keep this disabled.

_Raw todo.txt:_

```todotxt
(A) 2026-01-27 Do +laundry at @home
```

If `clean_description` is enabled (`true`), the output becomes incoherent:

```text
Do at
```

But if the `clean_description` is disabled (`false`), the output becomes readable:

```
Do laundry at home
```

### When to use: `true`

Enable this setting _only_ if you append metadata to the end of your tasks and want to hide the redundancy.

_Raw todo.txt:_

```todotxt
(A) 2026-01-27 Do laundry at home +laundry @home
```

_Output:_

```text
Do laundry at home
```

## `date_format`

> Default: `%Y-%m-%d`

Sets the display string for dates in the output. This setting accepts any standard [C `strftime` placeholders](<https://www.google.com/search?q=%5Bhttps://man7.org/linux/man-pages/man3/strftime.3.html%23DESCRIPTION%5D(https://man7.org/linux/man-pages/man3/strftime.3.html%23DESCRIPTION)>).

| Value        | Output       |
| ------------ | ------------ |
| `"%Y-%m-%d"` | `2026-01-28` |
| `"%d/%m/%Y"` | `28/01/2026` |
| `"%m/%d/%Y"` | `01/28/2026` |
