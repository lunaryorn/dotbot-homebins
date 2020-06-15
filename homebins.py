# Copyright 2020 Sebastian Wiesner <sebastian@swsnr.de>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import hashlib
from pathlib import Path
from subprocess import run
from urllib.request import Request, urlopen

from dotbot import Plugin

VERSION = '0.0.3'
CHECKSUM = '463d2be5de1fb82476c4ada98e862a51cd21f514cf41329117a1f0c02cdfb7247274bd6b2b879255d1de960347efeda5f413b134f874742f1871a59dd7792ab1'


class Homebins(Plugin):
    _directive = 'homebins'

    homebins = Path.home() / '.local' / 'bin' / 'homebins'

    def can_handle(self, directive):
        return self._directive == directive

    def _bootstrap_homebins(self):
        self._log.info('Installing homebins')
        download = f'https://github.com/lunaryorn/homebins/releases/download/v{VERSION}/homebins'
        run(['curl', '-sSL', '--output', str(self.homebins), download], check=True)
        contents = self.homebins.read_bytes()
        if hashlib.blake2b(contents).hexdigest() != CHECKSUM:
            self.homebins.unlink()
            self._log.error('Checksum validation of homebins failed!')
            raise ValueError('Invalid checksum')
        else:
            self.homebins.chmod(0o700)

    def _ensure_homebins(self):
        if not self.homebins.exists():
            self._bootstrap_homebins()
            # Install the full homebins
            run([str(self.homebins), 'install', 'homebins'], check=True)

    def _get_installed_manifests(self):
        output = run([str(self.homebins), 'installed'],
                     capture_output=True, text=True, check=True)
        return set(line.split('=')[0].strip() for line in output.stdout.splitlines())

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError(directive)

        self._ensure_homebins()

        installed_manifests = self._get_installed_manifests()
        to_install = [m for m in data['add'] if m not in installed_manifests]
        if to_install:
            run([str(self.homebins), 'install'] + to_install, check=True)

        if data.get('update', False):
            run([str(self.homebins), 'update'], check=True)

        return True
