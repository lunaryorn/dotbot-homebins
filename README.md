# dotbot-gsettings

A [dotbot] plugin to install tools with [homebins].

This plugin bootstraps `homebins` if not already installed.

Add as submodule to your dotfiles repo and as `-p path/to/submodule/homebins.py`
to `install.bash`, then configure your `install.conf.yaml`:

```yaml
- homebins:
    # Update all installed binaries (defaults to false if omitted).
    update: true
    # Install the following binaries if not already installed.
    add:
      - bat
      - exa
      - fd
      - git-gone
      - hub
      - jq
```

[dotbot]: https://github.com/anishathalye/dotbot
[homebins]: https://github.com/lunaryorn/homebins

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v.
2.0. If a copy of the MPL was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
