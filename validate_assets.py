#!/usr/bin/env python3
"""Offline resource checks; does not replace Gradle compilation or in-game testing."""
import json
import shutil
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
RES = ROOT / 'src/main/resources'
errors = []
json_data = {}
for path in RES.rglob('*.json'):
    try:
        json_data[path.relative_to(RES).as_posix()] = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'{path.relative_to(ROOT)}: invalid JSON: {exc}')

geo_path = RES / 'assets/goblin/geo/goblin.geo.json'
anim_path = RES / 'assets/goblin/animations/goblin.animation.json'
bones = set()
try:
    geo = json.loads(geo_path.read_text(encoding='utf-8'))
    anim = json.loads(anim_path.read_text(encoding='utf-8'))
    bones = {b['name'] for g in geo['minecraft:geometry'] for b in g['bones']}
    for anim_name, data in anim['animations'].items():
        for bone in data.get('bones', {}):
            if bone not in bones:
                errors.append(f'{anim_name}: animation references missing bone {bone}')
except Exception as exc:
    errors.append(f'geometry/animation validation failed: {exc}')

for rel in ['assets/goblin/textures/entity/goblin.png', 'assets/goblin/textures/item/goblin_spawn_egg.png']:
    p = RES / rel
    try:
        raw = p.read_bytes()
        if raw[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('not a PNG file')
        w, h = struct.unpack('>II', raw[16:24])
        if not w or not h:
            raise ValueError('zero-sized image')
    except Exception as exc:
        errors.append(f'{rel}: {exc}')

sound_names = ('idle', 'alert', 'attack', 'hurt', 'death')
sounds_json = json_data.get('assets/goblin/sounds.json', {})
for name in sound_names:
    rel = f'assets/goblin/sounds/goblin_{name}.ogg'
    p = RES / rel
    if not p.exists() or not p.read_bytes().startswith(b'OggS'):
        errors.append(f'{rel}: missing or invalid Ogg container')
    if f'goblin_{name}' not in sounds_json:
        errors.append(f'sounds.json: missing goblin_{name} event')
    if shutil.which('ffprobe') and p.exists():
        probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'default=nw=1:nk=1', str(p)], capture_output=True, text=True)
        if probe.returncode or 'vorbis' not in probe.stdout.lower():
            errors.append(f'{rel}: ffprobe could not decode a Vorbis audio stream')

model = json_data.get('assets/goblin/models/item/goblin_spawn_egg.json', {})
if model.get('textures', {}).get('layer0') != 'goblin:item/goblin_spawn_egg':
    errors.append('Spawn Egg item model does not point to the supplied icon texture')

if errors:
    print('VALIDATION FAILED')
    print('\n'.join(errors))
    raise SystemExit(1)
print('PASS: all resource JSON files parse')
print(f'PASS: {len(bones)} geometry bones; all animation bone references exist')
print('PASS: entity texture and Spawn Egg icon are valid PNG files')
print('PASS: five OGG sound files and sound event declarations exist')
if shutil.which('ffprobe'):
    print('PASS: ffprobe decoded all five OGG/Vorbis streams')
print('PASS: Spawn Egg model references the supplied icon texture')
print('NOTE: Java/NeoForge compilation and in-game testing are not performed by this script')
