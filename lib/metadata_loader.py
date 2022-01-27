import json
import zipfile
import os

def collect_mods(folder):
  mod_metadatas = []
  for file in os.listdir(folder):
    if file.endswith(".zip"):
      path = os.path.join(folder, file)
      mod_metadatas.append(collect_mod_metadata(path))
  return mod_metadatas

def collect_mod_metadata(zip_file_path):
  metadata = ModMetadata()
  with zipfile.ZipFile(zip_file_path) as mod_zip:
    for info in mod_zip.infolist():
      if os.path.basename(info.filename).lower() == "manifest.json":
        with mod_zip.open(info) as file:
          metadata.from_json(file)
          #todo replace all in manifest and check files
          return metadata

class ModMetadata:
  def __init__(self):
    self.title = ""
    self.author = ""
    self.mods_required = []
    self.levels = []
    self.other_mst_files = []
    self.non_mst_files = []

  def __str__(self):
    retstring = ""
    retstring += f'Title: {self.title}\n'
    retstring += f'Author: {self.author}\n'
    retstring += f'Mods_required:\n'
    for mod in self.mods_required:
      retstring += f'\t{mod}\n'
    retstring += f'Levels:\n'
    for level in self.levels:
      retstring += f'\t{level}\n'
    retstring += f'Other MST Files:\n'
    for other_mst_file in self.other_mst_files:
      retstring += f'\t{other_mst_file}\n'
    retstring += f'Non MST Files:\n'
    for non_mst_file in self.non_mst_files:
      retstring += f'\t{non_mst_file}\n'
    return retstring

  def from_json(self, json_file):
    mod_dict = json.load(json_file)

    if "title" in mod_dict:
      if not isinstance(mod_dict['title'], str):
        raise ValueError('title')
      self.title = mod_dict['title']
    else:
      # Required field
      raise KeyError('title')

    if "author" in mod_dict:
      if not isinstance(mod_dict['author'], str):
        raise ValueError('author')
      self.author = mod_dict['author']
    else:
      # Required field
      raise KeyError('author')

    self.mods_required = []
    if "mods_required" in mod_dict:
      if not isinstance(mod_dict['mods_required'], list):
        raise ValueError('mods_required')
      index = 0
      for mod in mod_dict['mods_required']:
        #TODO check mod valid
        if not isinstance(mod, str):
          raise ValueError('mods_required[' + str(index) + ']')
        self.mods_required.append(mod)
        index += 1

    self.other_mst_files = []
    if "other_mst_files" in mod_dict:
      if not isinstance(mod_dict['other_mst_files'], list):
        raise ValueError('other_mst_files')
      index = 0
      for other_mst_file in mod_dict['other_mst_files']:
        if not isinstance(other_mst_file, str):
          raise ValueError('other_mst_files[' + str(index) + ']')
        self.other_mst_files.append(other_mst_file)
        index += 1

    self.non_mst_files = []
    if "non_mst_files" in mod_dict:
      if not isinstance(mod_dict['non_mst_files'], list):
        raise ValueError('non_mst_files')
      index = 0
      for non_mst_file in mod_dict['non_mst_files']:
        if not isinstance(non_mst_file, str):
          raise ValueError('non_mst_files[' + str(index) + ']')
        self.non_mst_files.append(non_mst_file)
        index += 1

    self.levels = []
    if "levels" in mod_dict:
      if not isinstance(mod_dict['levels'], list):
        raise ValueError('levels')
      index = 0
      for level in mod_dict['levels']:
        new_level = {}
        if not isinstance(level, dict):
          raise ValueError('levels[' + str(index) + ']')
        if "type" in level:
          if not isinstance(level['type'], str):
            raise ValueError('levels[' + str(index) + ']["type"]')
          #TODO verify type
          new_level['type'] = level['type']
        else:
          # Required field
          raise KeyError('levels[' + str(index) + ']["type"]')

        if "title" in level:
          if not isinstance(level['title'], str):
            raise ValueError('levels[' + str(index) + ']["title"]')
          new_level['title'] = level['title']
        else:
          # Required field
          raise KeyError('levels[' + str(index) + ']["title"]')

        if "location" in level:
          if not isinstance(level['location'], str):
            raise ValueError('levels[' + str(index) + ']["location"]')
          new_level['location'] = level['location']

        if "wld" in level:
          if not isinstance(level['wld'], str):
            raise ValueError('levels[' + str(index) + ']["wld"]')
          new_level['wld'] = level['wld']
        else:
          # Required field
          raise KeyError('levels[' + str(index) + ']["wld"]')

        if "csv" in level:
          if not isinstance(level['csv'], str):
            raise ValueError('levels[' + str(index) + ']["csv"]')
          new_level['csv'] = level['csv']
        else:
          # Required field
          raise KeyError('levels[' + str(index) + ']["csv"]')

        if "gt" in level:
          if not isinstance(level['gt'], str):
            raise ValueError('levels[' + str(index) + ']["gt"]')
          new_level['gt'] = level['gt']

        self.levels.append(new_level)
        index += 1

